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

12/10/13

For the audit files, it would be helpful having a comment id or a way of actually finding the comment in the thread
on the site

memory is the main bottleneck at the moment

some of these subreddits are not helping


/r/adviceanimals
/r/AskReddit
/r/aww
/r/bestof
/r/books
/r/earthporn
/r/explainlikeimfive
/r/funny
/r/gaming
/r/gifs
/r/IAmA
/r/movies
/r/music
/r/news
/r/pics
/r/science
/r/technology
/r/television
/r/todayilearned
/r/videos
/r/worldnews
/r/wtf

Im going to narrow things down to:
/r/adviceanimals
/r/AskReddit
/r/funny
/r/gifs
/r/IAmA
/r/pics
/r/todayilearned
/r/videos
/r/wtf

Seems like CPU isn't an issue so I'm going to calculate as much as I can at runtime e.g. score = ups - downs

09/11/13

Two types of reference; a submission reference, which is composed of a combination of title + content + selftext,
and a comment reference, which is likely to be just text, and therefore probably easier to analyse.

examples:

submission reference: http://www.reddit.com/r/pics/comments/1q4i4e/i_miss_my_phone/,

referring to http://www.reddit.com/r/pics/comments/1q3tfu/i_miss_my_phone/

comment reference: http://www.reddit.com/r/IAmA/comments/1o5ndh/iama_guy_who_went_from_430_pounds_to_170_pounds/ccp40hs

referring to http://www.reddit.com/r/AskReddit/comments/1nzfg3/what_is_the_weirdest_thing_money_can_legally_buy/ccnjg1i

Like with references, there are submission and comment referees. It seems like comment referees are likely to be
crazy stories in a sub like ask reddit, usually a top level comment.
