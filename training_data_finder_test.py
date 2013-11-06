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

# for s in submissions:

#     ## HIJACKING WITH TEST THREAD
#     #s = REDDIT.get_submission("http://www.reddit.com/r/todayilearned/comments/1n1bpc/til_a_study_gave_lsd_to_26_scientists_engineers/")

#     audit_strings = audit_submission(s)

#     if(audit_strings):

#         name = ""
#         if (s.author):
#             name = s.author.name
#         else:
#             name = "deleted"

#         filename = name + "_" + s.id + ".txt"

#         for a in audit_strings:
#             f = open(OUTPUT_DIR + filename, 'w', encoding='utf8')
#             print(a.encode('cp1252','ignore'))
#             f.write(a)
#             f.close()

    # DEBUG
    # break


## Checking audit file, if the line starts with "AUDITED" then skip over it
fileloc = 'auditlist.txt'

def get_next_sub_from_file():
    """
    Returns the next sub in the list if there are any left unaudited, otherwise
    returns the last line which is 'END'"""
    with open(fileloc, "r+", encoding='utf8') as f:
        line = f.readline()
        print(line)
        while(line[0:len("AUDITED")] == "AUDITED"):
            line = f.readline()

        if line == 'END':
            print(line)
            print('done')
            return "END"
        else:
            id = get_sub_id_from_file_line(line)
            assert isinstance(id, str), "Id is not string"
            return id

def get_sub_id_from_file_line(fileline):
    assert len(fileline) > 5, "Fileline is suspiciously short."
    """parses submission ID from line of auditlist.txt"""
    pattern = re.compile('\s+(\w+).*')
    match = pattern.match(fileline)
    id = match.group(1)

    assert id is not None, "Regex failed to find submission ID inline"
    return id

def write_auditlist(lines):
    """Accepts lists of auditlist lines, writes them to file, ensuring
    one more lines has AUDITED at the start than there is currently"""

    ## This reads the file, checks if a post has been audited,
    # if it hasnt then changes its status to audited until END


    with open(fileloc, "r+", encoding='utf8') as f:
        line = f.readline()
        print(line)

        while(line &&line[0:len("AUDITED")] == "AUDITED"):
            print(line)
            line = f.readline()

        if line == 'END':
            print(line)
            print('done')

        print(f.tell)

        f.seek(f.tell() - len(line) - 1)
        f.write("AUDITED")

def check_next_sub_in_auditlist(auditlist):
    for line in auditlist:
        if line == "END":
            exit()
            
        if line[0:len("AUDITED")] != "AUDITED":


def read_in_auditlist():
    lines = []
    with open(fileloc, "r+", encoding='utf8') as f:
        line = f.readline()

        while line:
            lines.append(line)
            line = f.readline()

    return lines

get_next_sub_from_file()
check_off_next_site()
get_next_sub_from_file()


    # this needs unfucking but has the general tools in place

# a = multi_reddit.get_top_from_all(limit=200)
# for i in a:
#     f.write(i.id)
#     f.write("\t")
#     f.write(i.subreddit.display_name)
#     f.write(" - ")
#     f.write(i.title)
#     f.write("\n")