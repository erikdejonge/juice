from nevow import loaders
from nevow import tags as T
from nevow import livepage
from nevow import appserver
from nevow import rend

from twisted.internet import reactor

import random, time

class Blaster: 
    def __init__(self, client, tenths): 
        self.client = client
        self.tenths = tenths
        self.now = 0.0
    def __call__(self): 
        self.client.set('head', str(self.now))
        self.now = self.now + self.tenths/10.0
        if self.now < 10:
            reactor.callLater(self.tenths/10.0, self)
            
def ping(client, payload): 
    try: 
        Blaster(client, float(payload))()
    except ValueError: 
        client.set('head', payload)
        reactor.callLater(1, client.set, 'head', "Do it again!")

ping = livepage.handler(ping, 
            livepage.document.getElementById('payload').value)

class Twister(livepage.LivePage):
    addSlash = True

    def render_form(self, context, data): 
        return context.tag(onsubmit=ping) # livepage.handler(ping))
    
    docFactory = loaders.xmlfile('twist.html')

class FakeFeed: 
    def __init__(self, name, url): 
        self.name = name
        self.url = url
        self.episodes = []

class FakeEpisode: 
    def __init__(self, title, timestamp): 
        self.title = title
        self.timestamp = timestamp

class FakeEnvironment: 
    """A fake environment for the renderer to work on."""
    def __init__(self): 
        """Initialise the environment, using the shared state Borg pattern."""
        att = '__shared_dict'
        if hasattr(FakeEnvironment, att): 
            self.__dict__ = getattr(FakeEnvironment, att)
        else: 
            setattr(FakeEnvironment, att, self.__dict__)
            self.feeds = []
            self.stock()

    def stock(self): 
        """Stock the environment."""
        rand = random.Random()
        for i in range(rand.randint(5, 10), rand.randint(15, 20)): 
            feed = FakeFeed("Fake Feed %d" % i, 
                            "http://fakefeed%d.com/rss.xml" % i)
            self.feeds.append(feed)
            begin = rand.randint(10, 20)
            end = rand.randint(begin, begin+10)
            for j in range(begin, end): 
                episode = FakeEpisode("Fake Episode %d" % (j+1), 
                        time.time() - rand.randint(1, 3600*24*31))
                feed.episodes.append(episode)

class FeedsPage(livepage.LivePage): 
    addSlash = True
    docFactory = loaders.xmlfile('feeds.html')

    def data_feeds_list(self, context, data): 
        return FakeEnvironment().feeds
        
    def data_episodes_list(self, context, data): 
        for feed in FakeEnvironment().feeds: 
            for episode in feed.episodes: 
                yield episode

    def render_feeds_row(self, context, data): 
        context.fillSlots('feed_title', data.name)
        return context.tag

    def render_episodes_row(self, context, data): 
        context.fillSlots('episode_title', data.title)
        context.fillSlots('episode_pubdate', time.ctime(data.timestamp))
        return context.tag


class RootPage(rend.Page):
    addSlash = True

    child_twist = Twister('twist')
    child_feeds = FeedsPage('feeds')

    docFactory = loaders.stan(
        T.html[
            T.body[
                T.p[
                    T.a(href='twist') ["Twist me, baby"],
                    "!",
                    ], 
                T.p[ 
                    T.a(href='feeds') ["Play with feeds"],
                    ".",
                    ]
                ]
            ])

if __name__ == '__main__':
    reactor.listenTCP(7080, appserver.NevowSite(RootPage()))
    reactor.run()

