package com.alexremedios.subredditfinderservice;

import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.ImmutableMap;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.extern.log4j.Log4j;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

import java.io.IOException;
import java.util.List;
import java.util.Map;

@RestController
@Log4j
public class SubmissionController {

    private final static String QUEUE_NAME = "request queue";
    private final Channel channel;
    private static final JedisPoolConfig config;
    static {
        config = new JedisPoolConfig();
        config.setMaxTotal(8);
    }
    private static final JedisPool pool = new JedisPool(config, "localhost");
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public SubmissionController() throws IOException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        channel = connection.createChannel();
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);

    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value = "/search", method = RequestMethod.POST)
    public RetrieveSubmissionDataResponse search(final @RequestBody SearchRequest req) throws IOException {
        final ImmutableMap.Builder<String, List<SubmissionData>> mapBuilder = new ImmutableMap.Builder<>();
        try (Jedis jedis = pool.getResource()) {

            for (final String url : req.urls) {
                try {
                    final String searchDataJson = jedis.get(url);
                    System.out.println(" [x] Read '" + searchDataJson + "' from cache");

                    if (searchDataJson == null) {
                        channel.basicPublish("", QUEUE_NAME, null, url.getBytes());
                        System.out.println(" [x] Sent '" + url + "'");
                        continue;
                    }

                    final JavaType type = objectMapper.getTypeFactory().constructCollectionType(List.class, SubmissionData.class);
                    final List<SubmissionData> submissionData = objectMapper.readValue(searchDataJson, type);
                    mapBuilder.put(url, submissionData);
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

    @Data
    @AllArgsConstructor
    public static class RetrieveSubmissionDataResponse {
        private Map<String, List<SubmissionData>> submissions;
    }
}
