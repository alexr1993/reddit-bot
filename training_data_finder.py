# This file is a part of ref_bot
#
#
#
#

from abc import ABCMeta
from abc import abstractmethod

"""
Contains code created to aid the procurement of training data for ref_bot

"""

class SnapshotTree:
    """Snapshot tree objects hold 3 levels of comments

    Top level is the root, which contains just one comment.

    The second level contains the comment which the snapshot is focusing on,
    along with all of its siblings.

    The bottom level contains all first generation descendents of the second
    level, essentially giving a well-defined, uniform slice into potenetially
    huge comment trees.

    The idea is that when a comment has "reference" in it, we want to check
    if its parent is a reference, so we use the parent as the starting
    point, look at the siblings for more support and then check the children
    for corroboration. 

    """

    def __init__(self, root, tier2, tier3):
        # TODO essentially implement what I tried to put in ref_bot but do it
        # with better OO and less memory intensive
        self.root  = root
        self.tier2 = tier2
        self.tier3 = tier3



class Post:

    __metaclass__ = ABCMeta

    def __init_(self, data):

        if data.author:
            self.author  = data.author.name
        else:
            self.author  = "DELETED"

        self._id         = data.id # id is private as mongo likes that
        self.name        = data.name

    def ToString(self):
        print("all the info")

class Comment(Post):

    def __init__(self, data):

        super().__init__(data)

        self.parent_id = data.parent_id
        self.body = data.body

class Submission(Post):

    def __init__(self, data):

        super().__init__(data)

        self.title = data.title
        self.selftext = data.selftext
        self.url = data.url




