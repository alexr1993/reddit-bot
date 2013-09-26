import praw

class Node(object):
    """http://stackoverflow.com/questions/2482602/a-general-tree-implementa
    tion-in-python"""

    def __init__(self, comment):
        self.comment = comment
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def to_string(self, depth = 0):
        """Return a string representation of the tree starting from self"""
        output = str(self.comment.body)

        if(self.children == []):
            return output

        else:
            depth += 1
            for c in self.children:
                output += '\n\n' + depth * '\t' + c.to_string(depth)

            return output

class CommentTree:
    """A Hierarchy of nodes"""

    def __init__(self, root):
        """Initiates tree with all comments descending from (comment) root"""
        self.root = Node(root.body)



## code for cleaning comments for printing
    # for r in replies:
    #     if not isinstance(r, praw.objects.MoreComments):

    #         cleaned = r.body[0:100].replace('\n', "")
    #         reply_bodies.append(cleaned)

    # return reply_bodies