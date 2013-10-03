import praw
import math
import copy

## TODO: updgrade to use abc (abstract base claseses)

class Post(object):
    """Abstract Base class for submission and comment"""

    ## constructor accepts post.Comment object
    def __init__(self, data):

        # if an account is removed from the post...
        if data.author:
            self.author  = data.author.name
        else:
            self.author  = "DELETED"
        self.created_utc = data.created_utc
        self.ups         = data.ups
        self.downs       = data.downs
        self._id         = data.id # id is private as mongo likes that
        self.name        = data.name
        self.score       = data.score
        self.subreddit   = data.subreddit.title # (the subreddit name)
        self.permalink   = data.permalink

        if isinstance(data, praw.objects.Comment):
            self.children = self.get_all_direct_children(data.replies)

        elif isinstance(data, praw.objects.Submission):
            self.children = self.get_all_direct_children(data.comments)

        else:
            assert False, "Invalid object handed to Post constructor"


    def get_all_direct_children(self, replies):
        """Get all top level replies for a given comment"""
        # accepts first replies or commetns object, returns entire tree of descendaents
        # as Post objects
        output = []

        while True:

            # list for the more comments so we can tell when there have been two in the same set
            more = []

            for r in replies:

                # append child comments to output
                if r.parent_id == self.name and isinstance(r, praw.objects.Comment):
                    output.append(Comment(r))

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
            replies = []

            # keep pumping in more comments
            for m in more:
                replies += m.comments()

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

    def to_disk_format(self):
        """Essentially just swap out the references to child objects with their comment ids"""
        # make copy of object
        cpy = copy.deepcopy(self) # deep copy in case we still want to use the object while its in memory (unlikely)

        for i in range(len(cpy.children)):
            temp_id = cpy.children[i]._id
            cpy.children[i] = temp_id

        return cpy.__dict__






class Comment(Post):
    """Contains whatever I need from PRAW's comment object"""
    # comment must be a praw.objects.Comment
    def __init__(self, comment):

        super().__init__(comment)

        self.body     = comment.body



    # code for cleaning comments for printing
    def to_string(self, depth = 0):
        
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