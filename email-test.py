from gmailModule import Gmail

def main():
    g = Gmail()
    g.login("hllbck7@gmail.com", "l0ll02013")
    unreadEmails = g.inbox().mail(unread = True)
    link = False
    for email in unreadEmails:
        email.fetch()
        if "a(" in str(email.subject):
            email.read()
            print "found and read"
        else:
            print "skipping"

while True:
    main()

