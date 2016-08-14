package hello;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.io.IOException;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.google.common.base.Joiner;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;
import lombok.Data;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.ImmutableMap;
import com.fasterxml.jackson.databind.JavaType;
@RestController
public class SampleController {
    private final static String QUEUE_NAME = "request queue";
    private final Channel channel;
    private static final JedisPool pool = new JedisPool(new JedisPoolConfig(), "localhost");
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public SampleController() throws IOException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        channel = connection.createChannel();
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);

    }

    @RequestMapping(value = "/search", method = RequestMethod.POST)
    public RetrieveSubmissionDataResponse search(@RequestBody SearchRequest req) throws IOException {
        final Jedis jedis = pool.getResource();
        final ImmutableMap.Builder<String, List<SubmissionData>> mapBuilder = new ImmutableMap.Builder<>();

        for (final String url : req.urls) {
            final String searchDataJson = jedis.get(url);
            System.out.println(" [x] Read '" + searchDataJson + "' from cache");

            if (searchDataJson == null) {
                final String message = url;
                channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
                System.out.println(" [x] Sent '" + message + "'");
                continue;
            }

            final JavaType type = objectMapper.getTypeFactory().constructCollectionType(List.class, SubmissionData.class);
            final List<SubmissionData> submissionData = objectMapper.readValue(searchDataJson, type);
            mapBuilder.put(url, submissionData);
        }
        final Map<String, List<SubmissionData>> map = mapBuilder.build();
        return new RetrieveSubmissionDataResponse(map);
    }


    @RequestMapping(value = "/retrieve", method = RequestMethod.GET)
    public RetrieveSubmissionDataResponse retrieve(@RequestParam("urls") String urls) throws IOException {
        final String[] urlArr = urls.split(",");
        final Jedis jedis = pool.getResource();
        final ImmutableMap.Builder<String, List<SubmissionData>> mapBuilder = new ImmutableMap.Builder<>();

        for (final String url : urlArr) {

            final String searchDataJson = jedis.get(url);
            System.out.println(" [x] Read '" + searchDataJson + "' from cache");
            final JavaType type = objectMapper.getTypeFactory().constructCollectionType(List.class, SubmissionData.class);
            final List<SubmissionData> submissionData = objectMapper.readValue(searchDataJson, type);
            mapBuilder.put(url, submissionData);
        }
	    // cache miss? return unhappy response
        final Map<String, List<SubmissionData>> map = mapBuilder.build();
        return new RetrieveSubmissionDataResponse(map);

	    // cache hit? return obj
    }

    @Data
    @AllArgsConstructor
    public static class RetrieveSubmissionDataResponse {
        private Map<String, List<SubmissionData>> submissions;
    }
}
