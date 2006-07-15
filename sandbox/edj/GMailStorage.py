

import libgmail

ga = libgmail.GmailAccount("podcasting.test@gmail.com", "qwerty")
ga.login()
folder = ga.getMessagesByFolder('inbox')

def KnownGuid(guid):
    print "not implemented"
    return False

# check against the rss to prevent downloading spam
def GuidInRss(guid):
    #lookup
    if guid=="rwaudio20041202.mp3":
        return True
    else :
        return False
    
for thread in folder:
  #print thread.id, len(thread), thread.subject
  for msg in thread:
    print "  ", msg.id, msg.number, msg.subject
    if KnownGuid(msg.subject)==False:
      if GuidInRss(msg.subject):
        print "downloading: ", msg.subject
        show = open(msg.subject, "w")
        show.write(msg.attachments[0]._getContent())
        show.close()