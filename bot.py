# Bot which catches people making references to front page articles in
# comments of other (front page) comments

import praw
import re     # regex
import time
import tree
import marshal

global reddit

#############################################################################
#
# INIT
#
#############################################################################

user_agent = "let alexr1993@gmail.com know if I'm breaking the rules"
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

# def print_strings(strlist):

#     print('-' * 77)
#     print('\n')
    
#     for s in strlist:
#         print(s)
#         print('-' * 35 + '\n')

#     print('-' * 77)

## seems like sometimes people will implicitly carry on the reference into
## the first level of comments but somewhere deeper somebody will actually
## say "reference" and possibly link to it

def get_all_direct_replies(comment):
    """Drills through all the MoreComments objects to get the complete
    list of replies - returns list of comments objects"""

    all_replies = []
    
    replies     = comment.replies
    last_reply = replies[-1]

    while isinstance(last_reply, praw.objects.MoreComments):

        all_replies += replies[:-1] # gather the comments

        replies = last_reply.comments() # request more

        # Sometimes requesting more comments returns None :/
        if replies is None:
            replies = []
            break

        last_reply = replies[-1] # update variant

    all_replies += replies # get final/only reply list

    return all_replies



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

## part 1: Get all front page posts and start sifting through the comments

submissions = reddit.get_front_page()

# front_page_audit()

## Get the top comment tree for a submish - these will have the best data

#sub = next(submissions)

#print(sub.title)



perm = 'http://www.reddit.com/r/todayilearned/comments/1n1bpc/til_a_study_gave_lsd_to_26_scientists_engineers/ccejp5c'
##
reference = read_permalink(perm)


replies = get_all_direct_replies(reference)[0]

replies = [replies, 2]

print(replies)



f = open("marshaldcomments.obj", "wb")
marshal.dump(replies, f)

f.close()




g = open("marshaldcomments.obj", "rb")
print("sdfasd")

openedreplies = marshal.load(g)
g.close()


print("DEmarshalD")
print(openedreplies[0])
print("DONE")

#print_strings(replies)

# root = tree.Node(reference.body)

# for r in replies:
#     root.add_child(tree.Node(r))


# child1 = tree.Node("loloolol")
# child2 = tree.Node("omg repost")
# child3 = tree.Node("If you like it then just upvote and stfu")

# root.add_child(child1)
# root.add_child(child2)

# child1.add_child(child3)
# child2.add_child(tree.Node("i kno rite"))
# child3.add_child(child2)


# rootstring = root.to_string()

# print(rootstring)

















