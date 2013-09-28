import praw
import math

class Node(object):
    """http://stackoverflow.com/questions/2482602/a-general-tree-implementa
    tion-in-python"""

    ## constructer accepts tree.Comment object
    def __init__(self, comment):
        assert type(comment) == Comment

        self.comment = comment
        self.children = []

    def add_child(self, obj):
        assert type(obj) == Node
        self.children.append(obj)

    def to_string(self, depth = 0):
        """Return a string representation of the tree starting from self"""
        output = self.comment.to_string(depth)

        # base case
        if(self.children == []):
            return output

        # recursive case
        else:
            depth += 1
            for c in self.children:
                output += '\n\n' + c.to_string(depth)

            return output

    def tree_size(self):
        """Returns number of nodes in tree starting from self"""
        size = 1

        if len(self.children) == 0:
            return size

        for c in self.children:
            size += c.tree_size()

        return size

# class CommentTree:
#     """A Hierarchy of nodes"""

#     def __init__(self, root):
#         """Initiates tree with all comments descending from (comment) root"""
#         self.root = Node(root.body)

class Comment:
    """Contains whatever I need from PRAW's comment object"""
    # comment must be a praw.objects.comment
    def __init__(self, comment):
        self.body = comment.body


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