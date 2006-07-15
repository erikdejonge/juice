
# python can reload modules on the fly, this prevents rebooting the application everytime :)
# - downloads can't update the hidden spotlighted items
# - spotlight should work on al fields

def OnPaste(self, event):
    print self.OnPaste(event)

import urlparse
import time

def self_test(self, event):
    self.numFeedScanThreads.SetValue("2")
    self.numDownloadThreads.SetDefaultItem(3)

STRIPE_ODD_COLOR = '#EDF3FE'
STRIPE_EVEN_COLOR = '#FFFFFF'
        
def trimurl(url): 
    method, site, path, ign1, ign2 = urlparse.urlsplit(url)
    sitesplit = site.split('.')
    if len(sitesplit) and sitesplit[0].startswith('www'): 
        site = '.'.join(sitesplit[1:])
    return "%s%s" % (site, path)
    
class FeedBuffer:
    pass

import threading
class KeyWatchingCaller(threading.Thread):
    def __init__(self, themethod, param, currenttable, duration):
        threading.Thread.__init__(self) 
        self.m_method = themethod
        self.m_param = param
        self.m_table = currenttable
        self.m_duration = duration
    def run(self):
        import time
        time.sleep(self.m_duration)
        if len(self.m_table)==1:
            self.m_method(self.m_param)
        self.m_table.remove(self)
        
def timed_search_subs(self):
    query = self.searchboxfeeds.GetValue()
    
    self.feedslist.DeleteAllItems()
    self.episodes.DeleteAllItems() 
 
    if len(query)==0:
        self.toolbarSubscr.EnableTool(self.toolCheckAllId,True)
        self.toolbarSubscr.EnableTool(self.toolCatchupId,True)
        self.PopulateFeedsList()
        return 
 
    fds = self.ipodder.feeds

    import wx
    count = 0
    self.feedsdict = {}

    for feedinfo in fds:
        if feedinfo.title:
            search_title = feedinfo.title
        else:
            search_title = feedinfo.url
        #print dir(feedinfo)
        if (query.lower() in search_title.lower())|(query.lower() in feedinfo.url.lower())|(query.lower() in feedinfo.sub_state.lower()):
            self.toolbarSubscr.EnableTool(self.toolCheckAllId,False)
            self.toolbarSubscr.EnableTool(self.toolCatchupId,False)
            
            if feedinfo.sub_state in ['unsubscribed', 'disabled'] \
                and not self.ipodder.config.debug:
                continue
            #if sub_state == 'preview':
            #    continue
            id = wx.NewId()
            self.feedsdict[id] = feedinfo

            if feedinfo.title:
                index = self.feedslist.InsertImageStringItem(0,feedinfo.title,self.lemon_idle_idx)
            else:
                index = self.feedslist.InsertImageStringItem(0,feedinfo.url,self.lemon_idle_idx)
            for i in range(0,2):
                self.feedslist.SetStringItem(0,1,feedinfo.sub_state)
                self.feedslist.SetStringItem(0,2,'%4.1f' % feedinfo.mb_on_disk())
                self.feedslist.SetStringItem(0,3,trimurl(feedinfo.url))
                self.feedslist.SetItemData(0,id)
    self.mainpanel.ResetSortMixin()        

def PopulateDownloadsTab(self):
    try:
        encinfolist = self.ipodder.state['tmp_downloads']
    except KeyError:
        return
    
    for encinfo in encinfolist:
        self.DownloadTabLog(encinfo,prune=False)

    self.DownloadTabPrune()

def search_subs(self):
    kwc = KeyWatchingCaller(timed_search_subs, self, self.m_sptl_subs_threads, 0.75)
    self.m_sptl_subs_threads.append(kwc)
    kwc.start()
    return

def timed_search_downloads(self):
    query = self.searchboxdownloads.GetValue()
    self.downloads.DeleteAllItems()
    for encinfo in self.m_encinfolist:
        if (query.lower() in str(encinfo.feed).lower())|(query.lower() in str(encinfo.url).lower())|(query.lower() in str(encinfo.GetStatus())):
            self.DownloadTabLog(encinfo,prune=False)
    self.DownloadTabPrune()
    
def search_downloads(self):
    kwc = KeyWatchingCaller(timed_search_downloads, self, self.m_sptl_dwnl_threads, 0.75)
    self.m_sptl_dwnl_threads.append(kwc)
    kwc.start()
    return
