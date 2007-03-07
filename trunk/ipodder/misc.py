# 
# iPodder miscellaneous methods
#

import os
import logging
import time
import datetime
import stat
from sgmllib import SGMLParser
import locale

try: 
    import win32api
except ImportError: 
    win32api = None
    
log = logging.getLogger('Juice')

def rfc822date(dt,tz):
    """convert a datetime into an RFC 822 formatted date

    Input date is assumed to be GMT if tz is None.
    To get the local timezone, call localTimezone().
    tz should be a string preferably representing a GMT offset (+dddd or -dddd)
    """
    # Looks like:
    #   Sat, 07 Sep 2002 00:00:01 GMT
    # Can't use strftime because that's locale dependent
    #
    # Isn't there a standard way to do this for Python?  The
    # rfc822 and email.Utils modules assume a timestamp.  The
    # following is based on the rfc822 module.
    if tz == None:
        tz = '+0000'
        
    return "%s, %02d %s %04d %02d:%02d:%02d %s" % (
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()],
            dt.day,
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month-1],
            dt.year, dt.hour, dt.minute, dt.second, tz)

def localTimezone():
    curtz = time.timezone # tz offset in seconds
    curtz = int(curtz/60) # tz offset in minutes
    curtz = "%+03d%02d" % (int(curtz/-60) , int(curtz%60)) # convert to +HHMM
    return curtz
    
def freespace(path): 
    "Return free disk space in MB for the requested path; -1 if unknown."
    if win32api is not None: 
        cwd = os.getcwd()
        try: 
            os.chdir(path)
            sps, bps, freeclusters, clusters = win32api.GetDiskFreeSpace()
            return sps * bps * freeclusters
        finally: 
            os.chdir(cwd)
    if not freespace.warned: 
        freespace.warned = True
        log.warn("Can't determine free disk space.")
    return -1
    
freespace.warned = False

def rename(old,new,backup=False):
    """Like os.rename, but first clears the new path so Windows
    won't throw Errno 17.  Optionally backs up the new location
    if something is there."""
    if not os.path.exists(old):
        raise Exception, "File %s doesn't exist" % old
    try:
        if backup:
            os.rename(new,"%s-%d" % (new,int(time.time())))
        else:
            os.remove(new)
    except OSError, ex:
        errno, message = ex.args
        if errno != 2: # ENOFILE
            raise OSError, ex

    os.rename(old,new)

def get_fileinfos(filenames, min_age=None):
    """Return a list of files and timestamps in the format
    (shortfilename, fullfilename, ctime, size), 
    
    min_age -- return only files last changed over min_age days ago."""
    files = []
    if min_age: # convert it from days to seconds
        now = time.time()
        min_age = min_age * 24 * 60 * 60
    for pathname in filenames:
        if not (pathname and os.path.isfile(pathname)):
            continue
        f = os.path.split(pathname)[-1]
        info = os.stat(pathname)
        ctime = info[stat.ST_CTIME]
        size = info[stat.ST_SIZE]
        if not min_age or (now - ctime > min_age):
            files.append((f, pathname, ctime, size))                    
    return files

def unique(sequence): 
    """Returns only the unique members of `sequence`. 
    
    Uses **is** rather than ==, much like `list.count`"""
    results = []
    resultmap = {}
    for item in sequence: 
        if not resultmap.has_key(item): 
            resultmap[item] = True
            results.append(item)
    return results

def url_cmdline_extract(url):
    if url.startswith("http:") or url.startswith("https:"):
        return url

    #Pseudo-protocol or protocol missing.    
    parts = url.split(":")
    if len(parts) == 1:
        #url is of form example.com/rss.xml
        return "http://%s" % url
    else:
        if parts[1].startswith("//"):
            #url is of form protocol://
            return "http:%s" % ":".join(parts[1:])
        else:
            if len(parts) > 2 and parts[2].startswith("//"):
                #url is of form protocol:http://example.com/rss.xml
                return ":".join(parts[1:])

    #url is of form example.com:8000/rss.xml
    #or something we don't recognize.
    return "http://%s" % url

def url_rssfile_extract(path):
    "Return a channel link with rel=self or empty string."
    from ipodder.contrib import feedparser
    feed = feedparser.parse(path)
    if hasattr(feed,"channel") and hasattr(feed.channel,"links"):
        for link in feed.channel.links:
            if hasattr(link,"rel") and link.rel == "self":
                return link.href

    #If we got here we didn't find a match.
    return ""

def coralize_url(url):
    if "nyud.net:8090" not in url.lower():
        class C:
          def __init__(self):
            self.m_cnt = 0
          def f(self, x):
            if self.m_cnt == 0: 
              if "http" not in x:
                if len(x)!=0:
                  self.m_cnt += 1
                  x = x + ".nyud.net:8090"
            return x
        
        c = C()
        coral_url =  map(c.f, url.split("/"))
        sb = ""
        frst = True
        for i in coral_url:
            if not frst:
                sb += "/"
            frst = False
            sb += i 
        
        return sb
    
# Code for extracting .pcast file links
class BasePcastProcessor(SGMLParser):
    def reset(self):
        self.tagstack = []
        SGMLParser.reset(self)
        self.href = ""

    def unknown_starttag(self, tag, attrs):
        self.tagstack.append(tag)
        if self.tagstack == ['pcast','channel','link']:
            rel = None
            type = None
            href = ""
            for (key,val) in attrs:
		if key == 'rel': rel = val
		if key == 'href': href = val
		if key == 'type': type = val
            if rel == 'feed' and type == 'application/rss+xml':
               self.href = href

    def unknown_endtag(self, tag):
        self.tagstack.pop()
        
def url_pcast_file_extract(path):
    "Return a channel link with rel=feed from a .pcast file."
    fh = open(path,'r')
    str = fh.read()
    fh.close() 
    p = BasePcastProcessor()
    p.feed(str)
    return p.href    

locale_preferred_encoding = locale.getpreferredencoding()

def encode(msg, encoding=None, replace=True, replacement=None): 
    """Encode a string to ascii.
    
    msg      -- the string to encode
    
    encoding -- the encoding to use; defaults to the locale's preferred
                encoding
                
    replace  -- replace un-encodable characters; default=True
    
    replacement -- what to replace them with; default='?'
    """
                
    if encoding is None:
        encoding = locale_preferred_encoding
    if replace: 
        if not isinstance(replace, basestring): 
            replace = 'replace'
        msg = msg.encode(encoding, replace)
    else: 
        msg = msg.encode(encoding) # might fail
    # TODO: come up with a version that doesn't screw up strings 
    # that genuinely contain question marks. 
    if replacement is not None: 
        msg = msg.replace('?', replacement)
    return msg

if __name__ == '__main__': 
    path = r'C:\Documents and Settings\aegrumet\Desktop\test.pcast'
    print url_pcast_file_extract(path)

    
