Reddit-Bot - GPL 3.0
==========

Finds references made about popular threads

We have references people make in comments to posts either popular recently or
possibly a post which is famous/infamous in Reddit history. The first part of
this problem is finding the most simple references, i.e. those which can be 
linked using the title text, after that it will get weird with references to
images and references made using images.

To start off I am going to cheat by using references people have pointed out
already, perhaps by text or by posting that captain america "I get that 
reference" gif


01/10/13:

I'm storing a load of comments in the hope of finding out more about
the references people make - i.e. which subreddit's these witty people comment
on, which sorts of posts references are made on, which sorts of posts references are
made about, and what kinds of responses these references get in terms of up/downvotes
and replies.

After systematically mining a load of comments I'm going to get these audit scripts
to feed me comments which triggered replies in which people have remarked that a
reference has been made.

I never knew there were so many ways of storing trees http://docs.mongodb.org/manual/tutorial/model-tree-structures/

I have no idea which is best at the moment, but the array of ancestors one would
be useful for reading conversations. Most of the time sibling comments don't interact
with each other...that might not matter though.

From comments I am taking...

- body
- createdutc
- ups
- downs
- id
-- permalink
-- score
---children
---submission
---subreddit

From submissions I am taking

- author
- created_utc
- subreddit.title (the subreddit name)
- ups
- downs
- permalink
- title
- selftext
- url
-- direct comments
--score
--- all comments
-- I am not sure wheter I want to store less data and synthesis at runtime things such as
permalinks to comments (submission permalink + comment id) and overall scores (ups - downs)

--- Things marked next to "---" are things which I am hoping the structure of my objects/db
will tell me.


05/10/13

Thought on classification: The title of a post will be the most important way of identifying
if a reference has been made to it during classification, but the comments could help build up
a profile of what it is really about.

