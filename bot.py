# Bot which catches people making references to front page articles in
# comments of other (front page) comments

import praw
import re     # regex
import time
import ref_bot
import sys
import pymongo

from pymongo import MongoClient


global REDDIT
global SUBREDDITS


# TODO make it less memory intensive - keep one comment tree in memory
# at a time rather than a whole submission worth of comments.
# find the best way of crawling submissions for training data. I.e
# keeping trees which have reference in them

#############################################################################
#
# INIT
#
#############################################################################

user_agent = "let alexr1993@gmail.com know if I'm breaking the rules, I am having trouble understanding what constitutes 1 api request "
REDDIT = praw.Reddit(user_agent)

mongo = MongoClient() # start client for default mongo config
db = mongo.ref_bot

collection = db.comments


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

# get subreddit objects for all the subs we are using
SUBREDDITS = (r.get_subreddit(sub) for sub  in SUBREDDIT_NAMES)

#############################################################################
#
# FUNCTIONS
#
#############################################################################

## this won't be used for a long time... only when I start pointing out refs
def login_Ref_Bot():
    """Logs in my bot: Ref_Bot"""
    user  = "Ref_Bot"

    # Keeping password safe on my PC as code is free on GitHub
    pword_file = open("C:\\redditbotpassword.txt", 'r')
    pword = pword_file.read()
    pword_file.close()

    REDDIT.login(user, pword)

    print("Logged in as " + user)

    print('=' * 77)

def log_post(filename, post):
    """quick function to write a posttree to a file"""
    f = open(filename, 'w', encoding='utf8')
    f.write(post.tree_to_string())
    f.close()


#############################################################################
#
# IN DEV
#
#############################################################################



## part 1: Get all front page ref_bots and start sifting through the comments

# submissions = REDDIT.get_front_page()

# front_page_audit()

## Get the top comment tree for a submish - these will have the best data

#sub = next(submissions)

#print(sub.title)


# when you use get_submission it will always return the submission object even when it is a permalink t o a comment


# Default Subreddits: Not all are being used now as the content doesn't support this in-joke detection well, e.g.
# because comments are generally more serious or posts tend to be longer and therefore will waste resources

# /r/adviceanimals
# /r/AskReddit
# /r/aww
# /r/bestof
# /r/books
# /r/earthporn
# /r/explainlikeimfive
# /r/funny
# /r/gaming
# /r/gifs
# /r/IAmA
# /r/movies
# /r/music
# /r/news
# /r/pics
# /r/science
# /r/technology
# /r/television
# /r/todayilearned
# /r/videos
# /r/worldnews
# /r/wtf


# topsubmissions = SUBREDDITS[0].get_hot() # gives the top 25 submissions for a subreddit

# encoded = post.tree_to_string().encode('cp1252','ignore')


def analyse_submission(sub):
    """accepts praw.objects.Submission"""
    post = ref_bot.Submission(sub) # triggers recursive creation of comment tree

    loc = "transcripts"
    name = post.author + ".txt"
    log_post(loc + "\\" + name, post)

    post.write_tree_to_disk(collection)


#print(encoded)
#print(post.tree_to_string())

def audit_submission(sub):
        # make sure thread is not in db already
    if not (list(db.comments.find( {"type": 'submission', "_id": sub.id}, {"title":1, "body":1, "author":1}))):
        analyse_submission(sub)

    else:
        print("seen before")  

# sub = REDDIT.get_submission("http://www.REDDIT.com/r/AskReddit/comments/1nzfg3/what_is_the_weirdest_thing_money_can_legally_buy/")




# print(post_disk)

front_page = REDDIT.get_front_page()



for sub in front_page:

    if sub.subreddit.display_name in SUBREDDIT_NAMES:
        print("Auditing thread in: " + sub.subreddit.display_name)
        audit_submission(sub)
    else:
        print("Ignoring thread in: " + sub.subreddit.display_name)

 




## Write comment tree to disk...

#TODO: http://www.REDDIT.com/r/redditdev/comments/1ijb3m/error_when_running_a_praw_script/

#############################################################################
#
# AUTOMATICALLY FIND POTENTIAL REFERENCES
#
#############################################################################



if re.match(".*\Wreference.*","omg a reference lol"):
    print("ref found")









