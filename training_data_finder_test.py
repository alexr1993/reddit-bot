import training_data_finder


"""Finds areas of comment trees where there may be references made to either
pop culture or Reddit in-jokes"""


import praw
import re
import time

global NUM_SUBMISSIONS
global REDDIT

REDDIT = praw.Reddit("alexr1993@gmail.com classifier project")
NUM_SUBMISSIONS = 4

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
multi_reddit = REDDIT.get_subreddit(multi_string)

# get_top_from_year / day / month / all
# get_hot
# get_rising


submissions = multi_reddit.get_top_from_week(limit=NUM_SUBMISSIONS)





def audit_submission(post):

    """
    Do an exaustive depth-first search of the submission, recording comment trees
    one level above and below any comment where the regex ".*\Wreference.* matches

    In the case of adjacent comments containing a reference i.e. siblings or
    parent/child, record the comment tree as large as necessary.

    Returns None if no reference found
    """

    children = training_data_finder.PRAWUtil.get_all_direct_children(post)

    # print(child_ids)

    # examine tier of comments
    for c in children:

        # make a snapshot if there's "reference"
        if re.match(".*\Wreference.*",c.body):

            print("=" * 150)
            print(c.body.upper())
            # write snapshot tree to file

            # children = [] # DEBUG

            grandchildren = []

            for c2 in children:
                grandchildren.append(training_data_finder.PRAWUtil.get_all_direct_children(c2))

            # create snapshot tree with the potential reference at the root, the
            # comment containing "reference" and its siblings in the middle and
            # all of their replies as the leaves

            fac = training_data_finder.SnapshotTreeFactory(post, children, grandchildren)

            snapshot_tree = fac.CreateSnapshotTree()
            
            ## In reality we want to return a whole post's worth of snapshot trees,
            #  but for the moment one is good for dev

            return snapshot_tree.ToString()

            # snapshot made, so we are done with this level
            break

        # otherwise keep looking
        else:
            print("-" * 150)

            print(c.body)







#############################################################################
#
# MAIN
#
#############################################################################

for s in submissions:

    ## HIJACKING WITH TEST THREAD
    #s = REDDIT.get_submission("http://www.reddit.com/r/movies/comments/1obptu/do_we_really_need_daily_update_pictures_of_the/")

    audit_string = audit_submission(s)

    filename = s.author.name + "_" + s.id

    print(audit_string)

    if(audit_string):

        f = open(filename, 'w', encoding='utf8')
        f.write(audit_string)
        f.close()
