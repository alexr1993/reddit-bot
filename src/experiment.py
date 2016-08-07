import praw
r = praw.Reddit(user_agent='my_cool_application')
# submissions = r.get_subreddit('opensource').get_hot(limit=5)
# [str(x) for x in submissions]
matches = r.search("https://streamable.com/e7e0")
[print(m.subreddit.url) for m in matches]