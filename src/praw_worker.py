#!/usr/bin/env python
import pika
import praw
import redis
import json
import datetime
import time

r = praw.Reddit(user_agent='subreddit finder chrome extension')
cache = redis.StrictRedis(host='localhost', port=6379, db=0)
queue_name = "request queue"

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue_name)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    cached = cache.get(body)
    # TODO check timestamp is older than x (also do this frontend)
    if cached is not None:
        return

    matches = r.search(body)

    iterator = iter(matches)
    output = []
    while True:
        try:
            match = next(iterator)

            submissionData = {
                "subredditName": str(match.subreddit),
                "cache_timestamp_utc": int(time.mktime(datetime.datetime.utcnow().timetuple())),
                "permalink": match.permalink,
                "score": match.score,
                "url": match.url,
                "author": str(match.author),
                "created_utc": match.created_utc 
            }
            output.append(submissionData)
            print("    " + str(submissionData))
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
while True:
    try:
        channel.start_consuming()
    except Exception as ex:
        print(ex)
        print("wtf")
