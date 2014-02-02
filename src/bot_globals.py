## This file is a part of the ref bot project
#  to be used as "from globals import *"

"""
Contains global values to be used across modules in the ref bot project such
as file locations, subreddit objects and the praw.Reddit object
"""

import praw

global REDDIT
global SUBREDDIT_NAMES
global MULTI_REDDIT
global RAW_DATA_DIR
global GENERIC_FOLDER
global BANANA_FOLDER

## Initialise Globals
REDDIT = praw.Reddit('reddit.com/u/topic_bot')
SUBREDDITS = (
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
# accepts "funny+askreddit+wtf" etc
MULTI_REDDIT = REDDIT.get_subreddit('+'.join(SUBREDDITS))
RAW_DATA_DIR = '/media/alex/Hitachi/raw_data/'
GENERIC_FOLDER = RAW_DATA_DIR + 'generic_corpora/'
BANANA_FOLDER = RAW_DATA_DIR + 'banana_for_scale_corpora/'