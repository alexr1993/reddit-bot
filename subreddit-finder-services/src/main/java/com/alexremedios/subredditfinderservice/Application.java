package com.alexremedios.subredditfinderservice;

import org.apache.log4j.Logger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;


@SpringBootApplication
public class Application {

    private static final Logger log = Logger.getLogger(Application.class);

    public static void main(String[] args) {
        System.setProperty("logging.file", "logs/service.log");


        log.info("Starting Application");
        ApplicationContext ctx = SpringApplication.run(Application.class, args);
        log.info("Application Context Created");
    }
}
