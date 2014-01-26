## This file is a part of ref bot project

## need to look at writing a corpus tools module, with support for
#  normalising words and manipulating the corpus until it represents a
#  feature vector or something that can easily be transformed into one

import collections
import json
from pprint import pprint
import praw
import re
from start_interactive_shell import start_interactive_shell
from stemming.porter2 import stem
import training_data_finder
from os import listdir


global REDDIT
global SUBREDDIT_NAMES
global MULTI_REDDIT
global RAW_DATA_DIR
global GENERIC_FOLDER
global BANANA_FOLDER

def normalise_word(word):
	'''Processes word so it can be inserted into text corpus'''

	# don't strip chars out of hyperlinks/subreddit links
	if not re.match('https?://|/r/|www', word):
		word = re.sub('\W', '', word) # remove non word characters
		word = stem(word) # don't want to stem if giving to nltk

	word = word.lower()
	return word

def get_thread(url, timelimit=20):
	'''
	Returns list of praw comment objects

	Can be passed an URL to a whole thread, or a specific comment, only
	issue is when given a comment URL only returns the comment, not the
	comment + all its children

	Timelimit in seconds is roughly assured as praw will only send requests
	every 2s, so if the limit is 20 there will be maximum 10 extra requests
	sent.
	'''
	thread = REDDIT.get_submission(url)
	max_calls = int(timelimit / 2)


	if len(thread.comments) == 1:
		print("Fetching children for comment!")

		comment = thread.comments[0]

		print(type(comment))

		thread = training_data_finder.PRAWUtil\
			.get_all_child_comments(comment, max_calls)

	# When it is a single comment (probably meaning a permalink has been)
	# supplied
	else:
		print("Fetching children for submission!")
		## replace_more_comments will replace limit morecomments objects, remove
		# the rest of the morecomments objects and return them from the method
		#
		# Every morecomments that is replaced with take an additional 2s at least
		thread.replace_more_comments(limit=max_calls, threshold=0)
		thread = thread.comments # ditch everything but comments

		print("got comments")

	#for comment in thread:
	#	assert(isinstance(comment, praw.objects.Comment)), type(comment)

	return thread

def normalise_corpus(corpus):
	'''Accepts list of strings. Feeds each word to normalise_word'''
	normalised_corpus = []

	# need to clean up corpus
	for i in range(len(corpus)):
		normalised_corpus.append(normalise_word(corpus[i]))

	return normalised_corpus

def create_corpus(thread):
	'''Accepts list of praw.comments and returns list of words'''
	thread_string = ""

	for comment in thread:
		thread_string += comment.body + ' '

	## must ensure that words are separated correctly before they are passed
	#  on to be individually normalised

	# remove square and round brackets as they are used for embedding image
	# links in quotes
	thread_string = re.sub('[\[\]\(\)]', ' ', thread_string)

	# split on any form of whitespace
	corpus = re.split('\s+', thread_string)

	return normalise_corpus(corpus)

def write_corpus_to_file(corpus, path):
	'''Accepts list of strings and a path *.txt'''
	f = open(path, 'w')

	for word in corpus:
		f.write(word)
		f.write(' ')
	f.close()

def scrape_thread_to_file(url, dir):
	'''
	Accepts an URL, fetches praw comments from it, converts them into a
	corpus, then writes the corpus to a file in directory dir, with a
	generated unique name
	'''

	thread = get_thread(url)
	root = thread[0]

	# unique idenditifer for a comment tree/thread
	if root.author:
		thread_id = root.author.name
	else:
		thread_id = 'deleted'
	thread_id += '_' + root.name

	corpus = create_corpus(thread)

	write_corpus_to_file(corpus, dir + thread_id + '.txt')
	# no return, just write to file

def scrape_threads_to_folder(urls, dir):
	for url in urls:
		scrape_thread_to_file(url, dir)

#############################################################################

if __name__ == "__main__":

	## Initialise Globals
	REDDIT = praw.Reddit('alexr1993@gmail.com')

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

	multi_string = '+'.join(SUBREDDIT_NAMES)

	# accepts "funny+askreddit+wtf" etc
	MULTI_REDDIT = REDDIT.get_subreddit(multi_string)

	RAW_DATA_DIR = '/media/alex/Hitachi/raw_data/'
	GENERIC_FOLDER = RAW_DATA_DIR + 'generic_corpora/'
	BANANA_FOLDER = RAW_DATA_DIR + 'banana_for_scale_corpora/'

	###########################################################################
	## Main

	# banana for scale urlsf = open('corpus.txt', 'w')

	# for word in corpus:
	# 	f.write(word)
	# 	f.write(' ')

	# f.close()

	# these 5 banana for scale urls have my peel of approval
	#saving these for test data
	banana1 = 'http://www.reddit.com/r/worldnews/comments/1qluvy/indian_train_strikes_herd_of_40_elephants/cde4vvv'
	banana2 = 'http://www.reddit.com/r/pics/comments/1rcx07/caught_a_little_octopus_in_costa_rica/cdm6mj2'
	banana3 = 'http://www.reddit.com/r/funny/comments/1reeuf/we_bought_a_big_ass_pizza_today_my_wife_asked_me/'
	banana4 = 'http://www.reddit.com/r/funny/comments/1rj8l8/reddit_right_now_fixed/'
	banana5 = 'http://www.reddit.com/r/aww/comments/1rkij9/my_girlfriend_works_at_an_animal_shelterso_when/'


	bananaposts = REDDIT.search('banana for scale', limit=40)

	banana_for_scale_urls = [banana1, banana2, banana3, banana4, banana5]


	threads = []
	corpora = []

	# for url in urls:
	# 	print(url)/media/alex/Hitachi
	# 	threads += get_thread(url)

	front_page = MULTI_REDDIT.get_top(limit=25)

	# these links are the threads which will be scraped
	links = [submission.permalink for submission in bananaposts]

	scrape_threads_to_folder(links, BANANA_FOLDER)


	## Read in all downloaded corpora
	files = [f for f in listdir(BANANA_FOLDER) if re.match('.*.txt', f)]




	# want a text corpus of everything said in the thread
	#master_corpus = create_corpus(threads)



	#counter = collections.Counter(master_corpus)

	#most_common = counter.most_common(200) # returns n most common, all if none

	# sorted set of words, values are the quanitity
	#dictionary = dict(counter)

	#word_count = sum(dictionary.values())
	#vocabulary_size = len(dictionary)

	# f = open('corpus.txt', 'w')

	# for word in corpus:
	# 	f.write(word)
	# 	f.write(' ')

	# f.close()



	#############################################################################
	#start_interactive_shell()

	import readline # optional, will allow Up/Down/History in the console
	import code
	vars = globals().copy()
	vars.update(locals())
	shell = code.InteractiveConsole(vars)
	shell.interact()