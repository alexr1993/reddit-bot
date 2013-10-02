import praw
import math

## KEEPING POSTS STORED IN A BIG LIST IN POSTTREE CLASS

## TODO: updgrade to use abc (abstract base claseses)
#
# Post objects are either comments or submissions,
# it is important submissions can be treated like 
# comments as when they are self posts they essentially
# are comments... although they will never really be
# references to other posts as meta stuff isn't
# generally allowed
#



class Post(object):
    """Abstract Base class for submission and comment"""

    ## constructor accepts post.Comment object
    def __init__(self, data):

        self.author      = data.author.name
        self.created_utc = data.created_utc
        self.ups         = data.ups
        self.downs       = data.downs
        self.id          = data.id
        self.name        = data.name
        self.score       = data.score
        self.subreddit   = data.subreddit.title # (the subreddit name)
        self.permalink   = data.permalink

        ## populate chilren array with the id's of replies
        if isinstance(data, praw.objects.Comment):
            self.children = self.get_all_direct_children(data.replies)

        elif isinstance(data, praw.objects.Submission):
            self.children = self.get_all_direct_children(data.comments)

        else:
            assert False, "Invalid object handed to Post constructor"



    def tree_to_string(self, depth = 0):
        """Return a string representation of the tree starting from self"""
        output = self.to_string(depth)

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
        """Returns number of Posts in tree starting from self"""
        size = 1

        if len(self.children) == 0:
            return size

        for c in self.children:
            size += c.tree_size()

        return size

    def to_string(self):

        raise NotImplementedError("Please Implement to_string!")


class Comment(Post):
    """Contains whatever I need from PRAW's comment object"""
    # comment must be a praw.objects.Comment
    def __init__(self, comment):

        super().__init__(comment)

        self.body     = comment.body



    # code for cleaning comments for printing
    def to_string(self, depth):
        
        TAB_LENGTH = 4
        OUTPUT_WIDTH = 128

        text_width = OUTPUT_WIDTH - TAB_LENGTH * depth

        num_output_lines = math.ceil(len(self.body) / text_width)

        no_nls = self.body.replace('\n', '//')
        
        formatted = ""

        for i in range(num_output_lines):

            start = text_width * i

            if i > len(no_nls) - 1:
                end = len(no_nls) - 1

            else:
                end = start + text_width - 1

            formatted += '\n' + (' ' * TAB_LENGTH * depth) + '|' + no_nls[start:end]

        return formatted



class Submission(Post):
    """Everyting i need from praw.objects.Submission"""

    def __init__(self, submission):

        super().__init__(submission)

        self.title    = submission.title
        self.selftext = submission.selftext
        self.url      = submission.url # the content, not the comments - the comments is permalink


        # also need comments list-  maybe subclass Post

class PostTree():
    """Composed of nodes, manipulates from the root."""

    ## give it a post object as a root, it will make a tree
    ## stores a list of nodes containing their data and children
    def __init__(self, root):



        if isinstance(root, praw.objects.Submission):

            self.root = Submission(root)
            self.reply_queue = root.comments

        elif isinstance(root, praw.objects.Comment):

            self.root = Comment(root)
            self.reply_queue = root.replies

        else:
            raise TypeError("Post Tree initialiser must be praw comment or submission")


        self.child_objects = self.get_all_direct_children()

        ## base case
        if child_objects == []:
            return root

        else:
            for child in self.child_objects:
                # initiate child
                # initiate childs children instance variable using our call to get all direct children

    ## We have a tree in memory - we can use this method to
    ## take a subtree from it
    def crop():
        print("implement me")


    def get_all_direct_children(self):
        """Get all top level replies for a given comment"""

        output = []

        while True:

            # list for the more comments so we can tell when there have been two in the same set
            more = []

            for r in self.reply_queue:

                # append child comments to output
                if r.parent_id == self.name and isinstance(r, praw.objects.Comment):
                    output.append(r)

                # there should only be one morecomments object for each parent per reply set
                # set more comments variable
                elif r.parent_id == self.name and isinstance(r, praw.objects.MoreComments):
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
            self.reply_queue = []

            # keep pumping in more comments
            for m in more:
                self.reply_queue += m.comments()
# Inititialisation of a PostTree:

# Initialise the root

# Trigger initialisation of direct children

# repeat