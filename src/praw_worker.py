#!/usr/bin/env python
import pika
import praw
import redis
import json

r = praw.Reddit(user_agent='subreddit finder chrome extension')
cache = redis.StrictRedis(host='localhost', port=6379, db=0)
queue_name = "request queue"

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue_name)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    matches = r.search(body)

    iterator = iter(matches)
    output = []
    while True:
        try:
            match = next(iterator)
            sub = str(match.subreddit)
            submissionData = {"subredditName": sub}
            output.append(submissionData)
            print("    " + sub)
        except StopIteration:
            break
        except praw.errors.RedirectException:
            continue
            
    # todo insert link => output into the cache
    searchData = json.dumps(output)
    print("caching: " + searchData)
    cache.set(body, searchData)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
