## This file is a part of ref bot project

## need to look at writing a corpus tools module, with support for
#  normalising words and manipulating the corpus until it represents a
#  feature vector or something that can easily be transformed into one

import collections
import json
import praw
import re
from start_interactive_shell import start_interactive_shell
from stemming.porter2 import stem

global REDDIT
REDDIT = praw.Reddit('alexr1993@gmail.com')

def normalise_word(word):
	'''Processes word so it can be inserted into text corpus'''
	word = re.sub('\W', '', word) # remove non word characters
	word = word.lower()
	word = stem(word)
	return word

def get_thread(url):
	'''Returns list of praw comment objects'''
	thread = REDDIT.get_submission(url)

	## replace_more_comments will replace limit morecomments objects, remove
	# the rest of the morecomments objects and return them from the method
	thread.replace_more_comments(limit=5, threshold=0)

	return thread

## Main

url = "http://www.reddit.com/r/pics/comments/1q3tfu/i_miss_my_phone"
url = "http://www.reddit.com/r/pics/comments/1q56q3/i_miss_my_printer/"

thread = get_thread(url)

# want a text corpus of everything said in the thread
thread_string = ""

for comment in thread.comments:
	thread_string += comment.body + "\n"

corpus = thread_string.split(' ')

# need to clean up corpus
for i in range(len(corpus)):
	corpus[i] = normalise_word(corpus[i])


counter = collections.Counter(corpus)

most_common = counter.most_common(200) # returns n most common, all if none

# sorted set of words, values are the quanitity
dictionary = dict(counter)




#############################################################################
#start_interactive_shell()

import readline # optional, will allow Up/Down/History in the console
import code
vars = globals().copy()
vars.update(locals())
shell = code.InteractiveConsole(vars)
shell.interact()