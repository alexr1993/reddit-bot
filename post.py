import praw
import math

class Node(object):
    """Built from http://stackoverflow.com/questions/2482602/a-general-tree-implementa
    tion-in-python"""


    ## need to turn this into a superclass for comment and submission
    ## 




    ## constructor accepts post.Comment object
    def __init__(self, comment):
        assert type(comment) == Comment

        self.comment = comment
        self.children = []

    def add_child(self, obj):
        assert type(obj) == Node

        self.children.append(obj)


    def tree_to_string(self, depth = 0):
        """Return a string representation of the tree starting from self"""
        output = self.comment.to_string(depth)

        # base case
        if(self.children == []):
            return output

        # recursive case
        else:
            depth += 1
            for c in self.children:
                output += '\n\n' + c.tree_to_string(depth)

            return output

    def tree_size(self):
        """Returns number of nodes in tree starting from self"""
        size = 1

        if len(self.children) == 0:
            return size

        for c in self.children:
            size += c.tree_size()

        return size



class Comment():
    """Contains whatever I need from PRAW's comment object"""
    # comment must be a praw.objects.Comment
    def __init__(self, comment):

        self.body        = comment.body
        self.created_utc = comment.created_utc
        self.ups         = comment.ups
        self.downs       = comment.downs
        self.id          = comment.id
        self.score       = comment.score
        self.replies     = self.get_all_direct_replies(comment)


    # code for cleaning comments for printing
    def to_string(self, depth):
        
        TAB_LENGTH = 4
        OUTPUT_WIDTH = 128

        text_width = OUTPUT_WIDTH - TAB_LENGTH * depth

        num_output_lines = math.ceil(len(self.body) / text_width)

        no_nls = self.body.replace('\n', "//")
        
        formatted = ""

        for i in range(num_output_lines):

            start = text_width * i

            if i > len(no_nls) - 1:
                end = len(no_nls) - 1

            else:
                end = start + text_width - 1

            formatted += '\n' + (' ' * TAB_LENGTH * depth) + '|' + no_nls[start:end]

        return formatted


    def get_all_direct_replies(self, comment):
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



class Submission():
    """Everyting i need from praw.objects.Submission"""

    def __init__(self, submission):

        self.author = submission.author.name
        self.created_utc = submission.created_utc
        self.subreddit = submission.subreddit.title # (the subreddit name)
        self.ups = submission.ups
        self.downs = submission.downs
        self.permalink = submission.permalink
        self.title = submission.title
        self.selftext = submission.selftext
        self.url = submission.url
        self.score = submission.score

        # also need comments list-  maybe subclass node
