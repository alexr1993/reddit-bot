import praw
import re
import time

r = praw.Reddit("alexr1993@gmail.com classifier project")

## Crawls through old submissions and stores permalinks and snapshots to comments
# containing the word reference

SUBREDDIT_NAMES = (
    "adviceanimals",
    "AskReddit",
    "funny",
    "gifs",
    "IAmA",
    "pics",
    "todayilearned",
    "videos",
    "wtf"
)

multi_string = ""

for s in SUBREDDIT_NAMES:
    multi_string += s
    multi_string += "+"

multi_string = multi_string[:len(multi_string) - 1] # cut off trailing +


# accepts "funny+askreddit+wtf" etc
multi_reddit = r.get_subreddit(multi_string)

a = multi_reddit.get_top_from_year(limit = 25)

