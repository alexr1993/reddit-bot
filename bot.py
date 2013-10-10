# Bot which catches people making references to front page articles in
# comments of other (front page) comments

import praw
import re     # regex
import time
import ref_bot
import sys
import pymongo

from pymongo import MongoClient


global reddit


#############################################################################
#
# INIT
#
#############################################################################

user_agent = "let alexr1993@gmail.com know if I'm breaking the rules, I am having trouble understanding what constitutes 1 api request "
reddit = praw.Reddit(user_agent)

mongo = MongoClient() # start client for default mongo config
db = mongo.ref_bot

collection = db.comments


#############################################################################
#
# FUNCTIONS
#
#############################################################################

def login_Ref_Bot():
    """Logs in my bot: Ref_Bot"""
    user  = "Ref_Bot"

    # Keeping password safe on my PC as code is free on GitHub
    pword_file = open("C:\\redditbotpassword.txt", 'r')
    pword = pword_file.read()
    pword_file.close()

    reddit.login(user, pword)

    print("Logged in as " + user)

    print('=' * 77)



#############################################################################
#
# IN DEV
#
#############################################################################

#login_Ref_Bot()

## part 1: Get all front page ref_bots and start sifting through the comments

# submissions = reddit.get_front_page()

# front_page_audit()

## Get the top comment tree for a submish - these will have the best data

#sub = next(submissions)

#print(sub.title)



perm = 'http://www.reddit.com/r/todayilearned/comments/1n1bpc/til_a_study_gave_lsd_to_26_scientists_engineers/ccejp5c'
##
perm2 = 'http://www.reddit.com/r/todayilearned/comments/1n1bpc/til_a_study_gave_lsd_to_26_scientists_engineers/ccenomo'

perm = 'http://www.reddit.com/r/pics/comments/1nbahc/jcpenneys_is_having_another_sale/cch2n4d'

perm = 'http://www.reddit.com/r/explainlikeIAmA/comments/1n8jc0/explain_why_wizards_should_adopt_some_of_muggle'

perm = 'http://www.reddit.com/r/soccer/comments/1nsw7i/crazy_idea_compile_gifs_of_the_best_dives_and/'

perm = 'http://www.reddit.com/r/tifu/comments/1nojh9/tifu_by_sneezing_while_driving/'

# when you use get_submission it will always return the submission object even when it is a permalink t o a comment


# Default Subreddits:

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



# encoded = post.tree_to_string().encode('cp1252','ignore')

def log_post(filename, post):
    f = open(filename, 'w', encoding='utf8')
    f.write(post.tree_to_string())
    f.close()

def analyse_submission(sub):
    """accepts praw.objects.Submission"""
    post = ref_bot.Submission(sub) # triggers recursive creation of comment tree

    name = post.author + "thread.txt"
    log_post(name, post)

    post.write_tree_to_disk(collection)


#print(encoded)
#print(post.tree_to_string())




# print(post_disk)

front_page = reddit.get_front_page()

for sub in front_page:
 
    # make sure thread is not in db already
    if not (list(db.comments.find( {"type": 'submission', "_id": sub.id}, {"title":1, "body":1, "author":1}))):
        analyse_submission(sub)

    else:
        print("seen before")    




## Write comment tree to disk...

#TODO: http://www.reddit.com/r/redditdev/comments/1ijb3m/error_when_running_a_praw_script/














