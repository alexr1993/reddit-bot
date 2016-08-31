package com.alexremedios.subredditfinderservice;

import com.rabbitmq.client.ConnectionFactory;
import org.springframework.boot.actuate.autoconfigure.ExportMetricWriter;
import org.springframework.boot.actuate.metrics.repository.redis.RedisMetricRepository;
import org.springframework.boot.actuate.metrics.writer.MetricWriter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.jedis.JedisConnectionFactory;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

@Configuration
public class AppConfig {

    private static final JedisPoolConfig config;
    static {
        config = new JedisPoolConfig();
        config.setMaxTotal(128);
    }

    @Bean
    JedisPool jedisPool() {
         return new JedisPool(config, "localhost");
    }

    @Bean
    ConnectionFactory connectionFactory() {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        return factory;
    }
}