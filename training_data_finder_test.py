import training_data_finder


"""Finds areas of comment trees where there may be references made to either
pop culture or Reddit in-jokes"""


import praw
import re
import time

global NUM_SUBMISSIONS
global REDDIT
global OUTPUT_DIR

REDDIT = praw.Reddit("alexr1993@gmail.com classifier project")
NUM_SUBMISSIONS = 5
OUTPUT_DIR = r"/transcripts/"

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


submissions = multi_reddit.get_top_from_month(limit=NUM_SUBMISSIONS)

def audit_comment(comment):
    """Checks a PRAW comment's children for "reference", returns a snaphshot
    tree printout if a single comment has "reference", otherwise returns nothing
    (actually anything starting in 'refer' will trigger a snapshot) """

    assert isinstance(comment, praw.objects.Comment), type(comment)

    children = training_data_finder.PRAWUtil.get_all_direct_children(comment)

    for c in children:
        # make a snapshot if there's "reference"
        if re.match(".*\Wrefer.*",c.body):

            print("=" * 150)
            print(c.body.upper().encode('cp1252','ignore'))
            # write snapshot tree to file

            # children = [] # DEBUG

            grandchildren = []

            for c2 in children:
                grandchildren.append(training_data_finder.PRAWUtil.get_all_direct_children(c2))

            # create snapshot tree with the potential reference at the root, the
            # comment containing "reference" and its siblings in the middle and
            # all of their replies as the leaves

            fac = training_data_finder.SnapshotTreeFactory(comment, children, grandchildren)

            snapshot_tree = fac.CreateSnapshotTree()
            
            ## In reality we want to return a whole post's worth of snapshot trees,
            #  but for the moment one is good for dev

            return snapshot_tree.ToString()

            # snapshot made, so we are done with this level
            break

        # otherwise keep looking
        else:
            print("-" * 150)

            print(c.body.encode('cp1252','ignore'))

        # nothing found



def audit_submission(post):

    """
    Search all 2nd level comments for the word reference, as they may be
    somebody pointing out a reference a top level comment has made.

    Returns list of snapshot trees, if there are any.
    """

    children = training_data_finder.PRAWUtil.get_all_direct_children(post)

    # print(child_ids)

    output = []

    # examine tier of comments
    for c in children:
        snapshot = audit_comment(c)
        
        if snapshot:
            output.append(snapshot)

    return output






#############################################################################
#
# MAIN
#
#############################################################################

for s in submissions:

    ## HIJACKING WITH TEST THREAD
    #s = REDDIT.get_submission("http://www.reddit.com/r/todayilearned/comments/1n1bpc/til_a_study_gave_lsd_to_26_scientists_engineers/")

    audit_strings = audit_submission(s)

    if(audit_strings):

        name = ""
        if (s.author):
            name = s.author.name
        else:
            name = "deleted"

        filename = name + "_" + s.id + ".txt"

        for a in audit_strings:
            f = open(OUTPUT_DIR + filename, 'w', encoding='utf8')
            print(a.encode('cp1252','ignore'))
            f.write(a)
            f.close()

    # DEBUG
    # break
