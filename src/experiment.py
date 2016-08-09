from flask import Flask
from flask import request
app = Flask(__name__)

from flask.ext.cors import CORS
CORS(app)

import json
import praw

r = praw.Reddit(user_agent='my_cool_application')

cache = {}

@app.route("/")
def hello():
    link = request.args.get("url")
    if link in cache:
        return cache[link]

    matches = r.search(link)

    iterator = iter(matches)
    output = []
    while True:
        try:
            match = next(iterator)
            url = match.subreddit.url
            output.append(url)
            print("    " + url)
        except StopIteration:
            break
        except praw.errors.RedirectException:
            url = thread.getSubredditUrl()
            output.append(url)
            print("    " + url)
            
    response =  json.dumps(output)
    cache[link] = response
    return response

if __name__ == "__main__":
    app.run()


# # submissions = r.get_subreddit('opensource').get_hot(limit=5)
# # [str(x) for x in submissions]

# sub = "soccer"
# subreddit = r.get_subreddit(sub)
# posts = subreddit.get_top_from_day(limit=10)

# output = [sub]

# def log(line):
#     output.append(line)
#     print(line)

# for p in posts:
#     link = p.url
#     log(link)
#     log(p.title)
#     matches = r.search(link)

    # iterator = iter(matches)
    # while True:
    #     try:
    #         match = next(iterator)
    #         url = match.subreddit.url
    #         log("    " + url)
    #     except StopIteration:
    #         break
    #     except praw.errors.RedirectException:
    #         url = thread.getSubredditUrl()
    #         log("    " + url)

# #print('\n'.join(output))
# # matches = r.search("https://streamable.com/e7e0")
# # [print(m.subreddit.url) for m in matches]