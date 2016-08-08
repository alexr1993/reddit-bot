import praw

r = praw.Reddit(user_agent='my_cool_application')

# submissions = r.get_subreddit('opensource').get_hot(limit=5)
# [str(x) for x in submissions]

sub = "soccer"
subreddit = r.get_subreddit(sub)
posts = subreddit.get_top_from_day(limit=10)

output = [sub]

def log(line):
    output.append(line)
    print(line)

for p in posts:
    link = p.url
    log(link)
    log(p.title)
    matches = r.search(link)

    iterator = iter(matches)
    while True:
        try:
            match = next(iterator)
            url = match.subreddit.url
            log("    " + url)
        except StopIteration:
            break
        except praw.errors.RedirectException:
            url = thread.getSubredditUrl()
            log("    " + url)

#print('\n'.join(output))
# matches = r.search("https://streamable.com/e7e0")
# [print(m.subreddit.url) for m in matches]