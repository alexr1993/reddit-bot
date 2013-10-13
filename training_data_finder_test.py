import training_data_finder


"""Finds areas of comment trees where there may be references made to either
pop culture or Reddit in-jokes"""


import praw
import re
import time

global NUM_SUBMISSIONS
global REDDIT

REDDIT = praw.Reddit("alexr1993@gmail.com classifier project")
NUM_SUBMISSIONS = 1

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


submissions = multi_reddit.get_top_from_year(limit=NUM_SUBMISSIONS)



## actually get all comment objects to be efficient
def get_all_direct_children(post):
    """Get all top level replies for a given comment post"""


    assert isinstance(post, praw.objects.Comment) or \
           isinstance(post, praw.objects.Submission)

    permalink = post.permalink
    name = post.name

    if isinstance(post, praw.objects.Comment):
        replies = post.replies
    else:
        replies = post.comments

    output = []

    while True:

        # list for the more comments so we can tell when there have been two in the same set
        more = []

        for r in replies:

            # append child comments to output
            if r.parent_id == name and isinstance(r, praw.objects.Comment):
                output.append(r) # Recursively instantiate children... possibly needs to be changed.

            # there should only be one morecomments object for each parent per reply set
            # set more comments variable
            elif r.parent_id == name and isinstance(r, praw.objects.MoreComments):
                more.append(r)

            # non-direct children are to be discarded
            else:
                continue

        # sometimes there are multiple more comments for one parent, feature or bug?
        # assert len(more) <= 1

        # no more replies
        if more == []:

            print(str(len(output)) + " replies found for " + permalink + "\n")
            return output

        # update variant
        replies = []

        # keep pumping in more comments
        for m in more:

            # This true/false stuff is to prevent MoreComments.comments (praw\objects.py ln6 00)
            # from crashing the script
            update = False

            # if submission does not exist we must request it again
            if not m.submission:
                update = True

            try:    
                replies += m.comments(update)

            except Exception:
                error_string = ""
                error_string += "After " + str(len(output)) + " comments were collected, morecomments.comments()"
                error_string += " failed for " + permalink + "\n"
                error_string += "See http://www.reddit.com/r/redditdev/comments/1ijb3m/error_when_running_a_praw_script/\n"

                print(error_string)
                continue

def get_comment_by_id(permalink, id_):
    """Return a PRAW.Comment objects for a given permalink"""
    comment_permalink = permalink + id_

    # The submission returned will have the permalinked comment as its first
    return REDDIT.get_submission(comment_permalink).comments[0]

def audit_submission(post):

    """
    Do an exaustive depth-first search of the submission, recording comment trees
    one level above and below any comment where the regex ".*\Wreference.* matches

    In the case of adjacent comments containing a reference i.e. siblings or
    parent/child, record the comment tree as large as necessary.
    """

    children = get_all_direct_children(post)

    # print(child_ids)

    # examine tier of comments
    for c in children:

        # make a snapshot
        if re.match(".*\Wreference.*",c.body):

            print("=" * 150)
            print(c.body.upper())
            # write snapshot tree to file

            grandchildren = []

            for c2 in children:
                grandchildren.append(get_all_direct_children(c2))

            # create snapshot tree with the potential reference at the root, the
            # comment containing "reference" and its siblings in the middle and
            # all of their replies as the leaves
            snapshot_tree = training_data_finder.SnapshotTree(post, children, grandchildren)

        # otherwise keep looking
        else:
            print("-" * 150)

            print(c.body)

            continue

        # snapshot made, so we are done with this level
        break




#############################################################################
#
# MAIN
#
#############################################################################

for s in submissions:

    ## HIJACKING WITH TEST THREAD
    s = REDDIT.get_submission("http://www.reddit.com/r/movies/comments/1obptu/do_we_really_need_daily_update_pictures_of_the/")

    audit_string = audit_submission(s)

    filename = s.author.name + "_" + s.id

    #f = open(filename, 'w', encoding='utf8')
    # f.write(audit_string)
    #f.close()

