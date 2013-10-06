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


## seems like sometimes people will implicitly carry on the reference into
## the first level of comments but somewhere deeper somebody will actually
## say "reference" and possibly link to it

def read_permalink(perm):
    """Returns comment object for comment specified by input permalink"""
    return reddit.get_submission(perm).comments[0]



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

perm4 = 'http://www.reddit.com/r/explainlikeIAmA/comments/1n8jc0/explain_why_wizards_should_adopt_some_of_muggle/ccgeh0l'

perm = 'http://www.reddit.com/r/soccer/comments/1nsw7i/crazy_idea_compile_gifs_of_the_best_dives_and/'

root = read_permalink(perm)



post = ref_bot.Comment(root)
#replies = get_all_direct_replies(reference)


encoded = post.tree_to_string().replace("\\n", u"00D").encode('ascii','ignore')

print(encoded)
#print(post.tree_to_string())

print()

post_disk = post.tree_to_disk_format()

# print(post_disk)


## Write comment tree to disk...

mongo = MongoClient() # start client for default mongo config
db = mongo.ref_bot

collection = db.comments

post_id = collection.insert(post_disk)

print(post.tree_size())
print()

print(len(post_disk))






