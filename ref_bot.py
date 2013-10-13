import praw
import math
import copy
import time

# THIS CLASS IS FOR SCRAPING AND STORING ENTIRE POSTS
# WHICH WILL BE GOOD FOR BUILDING THE CLASSIFIER BUT 
# FIRST I NEED TO FIND A MEMORY EFFICIENT WAY OF JUST FINDING
# REFERENCES FOR TRAINING DATA

## TODO: updgrade to use abc (abstract base claseses)
## python does not have abstract classes by default

# TODO, let nodes be created on their own... let a tree class
# create and manipulate groups of nodes

global TAB_LENGTH
global OUTPUT_WIDTH
global NEWLINE

TAB_LENGTH = 4
OUTPUT_WIDTH = 128
NEWLINE      = u"\u000A" 

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
        #self.ups         = data.ups
        #self.downs       = data.downs
        self._id         = data.id # id is private as mongo likes that
        self.name        = data.name
        #self.score       = data.score
        self.subreddit   = data.subreddit.display_name # (the subreddit name)
        self.permalink   = data.permalink


        if isinstance(data, praw.objects.Comment):
            self.children = self.get_all_direct_children(data.replies)

        elif isinstance(data, praw.objects.Submission):
            self.children = self.get_all_direct_children(data.comments)

        else:
            assert False, "Invalid object handed to Post constructor"


    def get_all_direct_children(self, replies, throttle = 2):
        """Get all top level replies for a given comment, due to API rules throttle as many
        seconds as necessary - probably 2 to be reasonable"""
        # accepts first replies or commetns object, returns entire tree of descendaents
        # as Post objects
        # TODO, this should only really get a list of children ids, move the instantiation
        # of children to another method
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

                time.sleep(throttle)

                # This true/false stuff is to prevent MoreComments.comments (praw\objects.py ln6 00)
                # from crashing the script
                update = False

                # if submission does not exist we must request it again
                if not m.submission:
                    update = True

                try:    
                    replies += m.comments(update)

                except:
                    print("\nSAME OLD PROBLEM WITH MORECOMMENTS.COMMENTS() FOR " + str(self.permalink))
                    print("TRY USING THIS GUY'S CODE http://www.reddit.com/r/redditdev/comments/1ijb3m/error_when_running_a_praw_script/")
                    continue

    # TODO: Fix this by returning a list of lines which are good for printing as
    # encoding \n is messing up. Or find out how to actually fix it.
    def tree_to_string(self, depth = 0):
        """Return a string representation of the tree starting from self"""
        output = self.post_to_string(depth)

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

    def post_to_string(self):
        """abstract method"""
        raise NotImplementedError("Please Implement post_to_string!")

    def post_to_disk_format(self):
        """Essentially just swap out the references to child objects with their comment ids"""
        # make copy of object
        cpy = copy.deepcopy(self) # deep copy in case we still want to use the object while its in memory (unlikely)

        for i in range(len(cpy.children)):
            temp_id = cpy.children[i]._id
            cpy.children[i] = temp_id

        return cpy.__dict__

    def tree_to_disk_format(self):
        """does what post_to_disk_format does recursively through the descendents returning a list"""

        tree = []

        tree.append(self.post_to_disk_format())

        for c in self.children:
            tree += c.tree_to_disk_format()

        return tree

    def write_tree_to_disk(self, collection):

        post_disk = self.tree_to_disk_format()

        assert self.tree_size() == len(post_disk), "Size of the tree in memory is not the same as size of the list of docs being inserted to DB!"
        
        for p in post_disk:
            assert isinstance(p, type({}) ), "A post disk element is not a dictionary, %" % p


        post_id = collection.insert(post_disk, continue_on_error = True)

        print(str(len(post_disk)) + "records inserted to MongoDB")

        return post_id


class Comment(Post):
    """Contains whatever I need from PRAW's comment object"""
    # comment must be a praw.objects.Comment
    def __init__(self, comment):

        super().__init__(comment)

        self.body     = comment.body
        self.type     = "comment"

    # code for cleaning comments for printing
    def post_to_string(self, depth = 0):
        


        text_width = OUTPUT_WIDTH - TAB_LENGTH * depth

        num_output_lines = math.ceil(len(self.body) / text_width)

        no_nls = self.body.replace('\n', "//")
        
        formatted = ""
        formatted += NEWLINE + (' ' * TAB_LENGTH * depth) + '|' + "Post ID: " + self._id

        for i in range(num_output_lines):

            start = text_width * i

            if i > len(no_nls) - 1:
                end = len(no_nls) - 1

            else:
                end = start + text_width - 1


            formatted += NEWLINE + (' ' * TAB_LENGTH * depth) + '|' + no_nls[start:end]

        return formatted



class Submission(Post):
    """Everyting i need from praw.objects.Submission"""

    def __init__(self, submission):

        super().__init__(submission)

        self.title    = submission.title
        self.selftext = submission.selftext
        self.url      = submission.url # the content, not the comments - the comments is permalink
        self.type     = "submission"

    def post_to_string(self, depth = 0):
        
        output = self.title + '(/r/' + self.subreddit + ')' + NEWLINE * 2

        return output


        # also need comments list-  maybe subclass Post

