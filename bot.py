# Bot which catches people making references to front page articles in
# comments of other (front page) comments

user_agent = "reference-getter bot by OfficeGuyChillin"

user  = "Ref_Bot"

# Keeping password safe on my PC as code is free on GitHub
pword_file = open("C:\\redditbotpassword.txt", 'r')
pword = pword_file.read()

print(pword)
