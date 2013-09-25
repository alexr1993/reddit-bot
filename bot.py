# Bot which catches people making references to front page articles in
# comments of other (front page) comments

import praw
import re     # regex





user_agent = "let alexr1993@gmail.com know if I'm breaking the rules"

user  = "Ref_Bot"


# Keeping password safe on my PC as code is free on GitHub
pword_file = open("C:\\redditbotpassword.txt", 'r')
pword = pword_file.read()




reddit = praw.Reddit(user_agent)
reddit.login(user, pword)
print("Logged in as " + user)


## part 1: Get all front page posts and start sifting through the comments

submissions = reddit.get_front_page()

i = 0
num_of_comments = []

for submission in submissions:
    j = 0
    
    print(submission.title)
    print(submission.subreddit)
    print (str(i) + "th Submission")


    i = i + 1
    sub_comments = submission.comments

    for comment in sub_comments:
        
        if not isinstance(comment, praw.objects.MoreComments): #"reference" in comment.body:
            cond = re.search("\sreference", comment.body)
            if (cond):
                print (comment.body)
            
        else: # must be end of first page of comments
            num_of_comments.append(j)
            print(str(j) + " Comments")

        j = j + 1


    print("\n")
    print("#" * 80)
    print("\n")


rolling_total = 0

for com in num_of_comments:
    rolling_total += com

print("Total comments: " + str(rolling_total))
