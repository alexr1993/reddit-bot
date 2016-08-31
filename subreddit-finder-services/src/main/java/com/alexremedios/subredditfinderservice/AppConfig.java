package com.alexremedios.subredditfinderservice;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
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
}