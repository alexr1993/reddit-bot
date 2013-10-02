# Bot which catches people making references to front page articles in
# comments of other (front page) comments

import praw
import re     # regex
import time
import ref_bot
import sys
import pymongo

from pymongo import MongoClient
client = MongoClient() # start client for default mongo config

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

def get_all_direct_replies_old(comment):
    """Drills through all the MoreComments objects to get the complete
    list of replies - returns list of comments objects"""



    all_replies = []
    
    replies     = comment.replies

    # No replies? Return empty list
    if replies == []:
        return replies

    last_reply  = replies[-1]

    while isinstance(last_reply, praw.objects.MoreComments):


        all_replies += replies[:-1] # gather the comments

        # when you expand more comments (like in linke below) the tree
        # is flattened, so you gotta che3ck parent_id
        temp_replies = last_reply.comments() # request more


        # I'm using temp list because removing from list was being weird

        replies = []

        # make sure parent is correct
        for tr in temp_replies:
            if tr.parent_id == comment.name:
                assert type(tr) == praw.objects.Comment
                replies.append(tr)



        # # Sometimes requesting more comments returns None :/
        # if replies is None:
        #     replies = []
        #     break

        last_reply = replies[-1] # update variant

    all_replies += replies # get final/only reply list

    return all_replies



def get_all_direct_replies(comment):
    """Get all top level replies for a given comment"""

    output = []

    # initialise variant
    replies = comment.replies

    while True:

        # list for the more comments so we can tell when there have been two in the same set
        more = []

        for r in replies:

            # append child comments to output
            if r.parent_id == comment.name and isinstance(r, praw.objects.Comment):
                output.append(r)

            # there should only be one morecomments object for each parent per reply set
            # set more comments variable
            elif r.parent_id == comment.name and isinstance(r, praw.objects.MoreComments):
                more.append(r)

            # non-direct children are to be discarded
            else:
                continue

        # sometimes there are multiple more comments for one parent, feature or bug?
        # assert len(more) <= 1

        # no more replies
        if more == []:
            return output

        # update variant
        replies = []

        # keep pumping in more comments
        for m in more:
            replies += m.comments()




def read_permalink(perm):
    """Returns comment object for comment specified by input permalink"""
    return reddit.get_submission(perm).comments[0]

def front_page_audit():
    """ Summarises what is on the front page and quanitities of comments"""
    i = 1
    num_of_comments = []

    for submission in submissions:
        j = 0
        
        print(submission.title)
        print(submission.subreddit)
        print(str(i) + "th Submission")


        i += 1
        sub_comments = submission.comments

        for comment in sub_comments:
            
            if not isinstance(comment, praw.objects.MoreComments):

                # "reference" in comment.body
                cond = re.search("\sreference", comment.body)
                if (cond):
                    print (comment.body)
                
            else: # must be end of first page of comments
                num_of_comments.append(j)
                print(str(j) + " Comments")

            j += 1


        print("\n")
        print("#" * 80)
        print("\n")

        time.sleep(2) # don't want to punish the servers


    rolling_total = 0

    for com in num_of_comments:
        rolling_total += com

    print("Total comments: " + str(rolling_total))

    return

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

perm3 = 'http://www.reddit.com/r/pics/comments/1nbahc/jcpenneys_is_having_another_sale/cch2n4d'

perm = 'http://www.reddit.com/r/GetMotivated/comments/1nksrb/having_recently_suffered_from_an_entirely/'

comm = read_permalink(perm)

root = ref_bot.Comment(comm)

subobj = reddit.get_submission(perm)

sub = ref_bot.Submission(subobj)

print(root.children)

print("")
print(sub.children)

#replies = get_all_direct_replies(reference)





#comment = ref_bot.ref_bot(ref_bot.Comment(reference))


def populate_tree(root):
    """Accepts comment object of root, returns tree of descendents + itself"""


    # try:
    #     user = root.author.name
    # except:
    #     user = "DELETED"
    # print('\n' + user)
    # print('\n' + str(root.body.encode('utf-8')) )
    # Get layer 0 replies for this root comment
    replies = get_all_direct_(root)
    # print(replies)
    # print('-' * 80)

    # base case
    if replies == []:

        return root

    # recursive case
    for r in replies:
        child_ref_bot = ref_bot.ref_bot(ref_bot.Comment(r))


        child_tree = populate_tree(r)
        ref_bot.add_child(child_tree)

    return ref_bot



#tree = populate_tree(root)

# child1 = ref_bot.ref_bot("loloolol")
# child2 = ref_bot.ref_bot("omg reref_bot")
# child3 = ref_bot.ref_bot("If you like it then just upvote and stfu")

# root.add_child(child1)
# root.add_child(child2)

# child1.add_child(child3)
# child2.add_child(ref_bot.ref_bot("i kno rite"))
# child3.add_child(child2)


# rootstring = tree.tree_to_string()

# print(rootstring)
# print(tree.tree_size())









# f = open("pickledcomments.obj", "wb")
# pickle.dump(replies, f)
# f.close()




# g = open("pickledcomments.obj", "rb")
# openedreplies = pickle.load(g)
# g.close()









