package com.alexremedios.subredditfinderservice;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import com.google.common.collect.ImmutableMap;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

import java.io.IOException;
import java.time.Clock;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@Slf4j
public class SubmissionController {
    private final static String QUEUE_NAME = "request queue";
    private final Channel channel;
    private static final JedisPoolConfig config;
    static {
        config = new JedisPoolConfig();
        config.setMaxTotal(8);
    }
    private static final JedisPool pool = new JedisPool(config, "localhost");
    private static final ObjectMapper objectMapper = new ObjectMapper().setPropertyNamingStrategy(
                PropertyNamingStrategy.CAMEL_CASE_TO_LOWER_CASE_WITH_UNDERSCORES)
            .setSerializationInclusion(JsonInclude.Include.NON_NULL);

    public SubmissionController() throws IOException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        channel = connection.createChannel();
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);

    }
    private static final JavaType type = objectMapper.getTypeFactory().constructType(SubmissionCacheData.class);

    @CrossOrigin(origins = "*")
    @RequestMapping(value = "/search", method = RequestMethod.POST)
    public RetrieveSubmissionDataResponse search(final @RequestBody SearchRequest req) throws IOException {
        final ImmutableMap.Builder<String, List<SubmissionData>> mapBuilder = new ImmutableMap.Builder<>();
        try (Jedis jedis = pool.getResource()) {

            for (final String url : req.urls.stream().distinct().collect(Collectors.toList())) {
                if (url == null || url.isEmpty()) {
                    continue;
                }
                try {
                    final String searchDataJson = jedis.get(url);
                    log.info(" [x] Read '" + searchDataJson + "' from cache");

                    if (searchDataJson == null) {
                        enqueue(url, jedis);
                        continue;
                    }

                    final SubmissionCacheData cacheData = objectMapper.readValue(searchDataJson, type);

                    if (isPending(cacheData)) {
                        log.info("Url is pending in queue");
                        continue;
                    }

                    mapBuilder.put(url, cacheData.getSubmissionDataList());
                } catch (final Exception exception) {
                    log.error("Failed to process URL " + url, exception);
                }
            }
        } catch (final Exception exception) {
            log.error("Failed to obtain Jedis pool resource", exception);
            throw exception;
        }
        final Map<String, List<SubmissionData>> map = mapBuilder.build();
        return new RetrieveSubmissionDataResponse(map);
    }


    private void enqueue(final String url, final Jedis jedis) throws IOException {
        try {
            channel.basicPublish("", QUEUE_NAME, null, url.getBytes());
            log.info(" [x] Sent '" + url + "'");
        } catch (final IOException exception) {
            log.error("Failed to publish to queue: '" + url + "'");
            throw exception;
        }

        final SubmissionCacheData pendingSubData = SubmissionCacheData.builder()
                .cacheTimestampUtc(String.valueOf(Instant.now(Clock.systemUTC()).getEpochSecond()))
                .build();

        try {
            jedis.set(
                    url.getBytes(),
                    objectMapper.writeValueAsBytes(pendingSubData),
                    "NX".getBytes(),
                    "EX".getBytes(),
                    10
                    );
            log.info(" [x] Cached pending object for '" + url + "'");
        } catch (final Exception exception) {
            log.error("Failed to create pending data object: '" + url + "'");
        }
    }

    @Data
    @AllArgsConstructor
    public static class RetrieveSubmissionDataResponse {
        private Map<String, List<SubmissionData>> submissions;
    }

//    private boolean isOlderThan(final SubmissionCacheData cacheData, final int ageSeconds) {
//        final long nowSeconds = Instant.now(Clock.systemUTC()).getEpochSecond();
//        final long cacheTimeSeconds = Long.parseLong(cacheData.getCacheTimestampUtc());
//        return Math.abs(nowSeconds - cacheTimeSeconds) < ageSeconds;
//    }

    private boolean isPending(final SubmissionCacheData cacheData) {
        return cacheData.getSubmissionDataList() == null;
    }
}
