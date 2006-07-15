import twist
from twisted.application import service, strports
from nevow import appserver, livepage
livepage.DEBUG = True

application = service.Application("twist")
strports.service("7080", appserver.NevowSite(twist.Twister(), logPath="web.log")).setServiceParent(application)
