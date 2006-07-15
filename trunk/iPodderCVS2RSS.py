#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import os

class CVS2RSS:
    def handle_file(self, scl, cvsfile):
        class P:
            def __init__(self, max):
                self.i = 0
                self.m = max
            def p(self, x):
                if self.i<self.m:
                    if type(x)==type([]):
                        print "list"
                        for i in x:
                            print "  "+i
                    else:
                        print x
                self.i = self.i + 1
        
        class C:
            def __init__(self):
                self.m_items = []
                self.m_data = ""
            def f(self, x):
                def new():
                    #print self.m_data
                    self.m_items.append(self.m_data)
                    self.m_data = ""
                
                if "----------------------------" in x:
                    new()
                    return True;
                else:
                    if x=="\n":
                        new()
                    self.m_data += "\n" + x;
                    return False;
        c = C();
        filter(c.f, scl)
        
        class Header:
            def __init__(self):
                self.m_pos=0
                self.m_data = ""
            def add(self, x):
                if self.m_pos ==1:
                    self.m_data = str(x)
                self.m_pos = self.m_pos + 1
    
        class Split:
            def __init__(self, sep):
                self.sep = sep
            def parse(self, x):
                return x.split(self.sep)
                
        class Items:
            def __init__(self):
                self.m_pos=0
                self.m_data = []
            def add(self, x):
                if self.m_pos > 0:
                    li = str(x).split("\n")           
                    li2 = (filter(lambda x2: len(x2)!=0, li))
                    if len(li2)==0:
                        return
                    self.m_data.append(li2)
                self.m_pos = self.m_pos + 1
    
        h = Header()
        i = Items()
        
        filter (h.add, c.m_items)
        filter (i.add, c.m_items)
        from cgi import escape
        class RSSDoc:
            def __init__(self, file):
                self.m_items = 20
                self.m_diffs = self.m_items + 1
                self.m_file = file
                self.m_xml = "<rss version=\"2.0\">\n"; 
                self.m_xml += "<channel>\n"
                self.m_xml += "<title>" + escape(file) + "</title>\n"
                self.m_xml += "<link>http://sourceforge.net/projects/ipodder</link>\n"
            def AddElement(self, description, diff, author, date, version, previous_version):
                #print author, date
                
                title_len = 60
                title = author + ": " + description[0:title_len]
                if len(description)>title_len:
                     title += "..."
                description = description + diff                     
                d = escape(description)+"&lt;br /&gt;\nauthor:"+author+"&lt;br /&gt;\nfile:"+self.m_file+"&lt;br /&gt;\nversion:"+version+"&lt;br /&gt;\n"+date
                dt = date[6:len(date)]
                                
                self.m_xml += "<item>\n"
                self.m_xml += "<title>" + escape(dt) + " - " + escape(title) + "</title>\n"
                self.m_xml += "<description>" + d + "</description>\n"
                self.m_xml += "<pubDate>" + escape(dt) + "</pubDate>\n"
                link = "http://cvs.sourceforge.net/viewcvs.py/ipodder/iSpider/" + self.m_file + "?r1="+ previous_version + "&amp;r2=" + version            
                self.m_xml += "<link>" + escape(link) + "</link>\n"
                self.m_xml += "</item>\n"

            def GetDiff(self, v, vp):
                if self.m_diffs > 0:
                    self.m_diffs -= 1
                    os.system("cvs diff -kk -u -r "+str(v)+" -r "+str(vp)+" "+self.m_file+" > diffbuff.txt")
                    db = open("diffbuff.txt", "r")
                    scstr = ""
                    for l in db:
                        scstr+=(str(l))
                    db.close
                    html = scstr.replace(" ", "&nbsp;")
                    html = html.replace("\n", "<br/>")
    
                    print self.m_file, v, vp
                    return "<code>" + html + "</code>"
                else:
                    return "diff omitted"
                    
            def Parse(self, x):
                try:
                    if len(x)==0:
                        return
                    desc = x[2]
                    version = x[0][9:]
                    previous_version = "1."+str(int(float(version.split(".")[1])-1))
                    #print version, previous_version
                    author = ""
                    
                    for l in x:
                        if "date" in l:
                            if len(l.split(":"))>=2:
                                a = l.split(";")
                                date = a[0]   
                        if "author" in l:       
                            a = l.split(";")
                            a = a[1]
                            a = a.split(":")[1].lstrip().rstrip()
                            #print a
                            author = a
                    diff = "<br /><br /><hr />" + self.GetDiff(version, previous_version) + "<hr />"
                    if self.m_items > 0:
                        self.AddElement(desc, diff, author.lstrip(), date, version, previous_version)
                        self.m_diffs -= 1
                except:
                    print x
                    raise
                    
            def GetDoc(self):
                self.m_xml += "</channel>\n"
                self.m_xml += "</rss>\n"; 
                return self.m_xml
                
        rss = RSSDoc(cvsfile)
        map(rss.Parse, i.m_data)
        
        print "writing", cvsfile+".xml"
        f = open(cvsfile+".xml", "w")
        self.ftp_batch += "put "+cvsfile+".xml\n"
        f.write(rss.GetDoc())
        f.close()
    
        #/home/groups/i/ip/ipodder/htdocs/dev_feeds

def runforfile(cvsfile):
    os.system("cvs log " + cvsfile+ " > cvslog.txt")
    cl = open("cvslog.txt", "r")
    scstr = ""
    for l in cl:
        scstr+=(str(l))
    cl.close
    
    scl= scstr.split("RCS file:")

    cvs2rss = CVS2RSS()
    
    name = ""
    tmp = []
    names = []
    cvs2rss.ftp_batch = "cd /home/groups/i/ip/ipodder/htdocs/dev_feeds\n"
    for x in scl:
        #print x
        lines = x.split("\n")
        for l in lines:
            #print l
            if l!="":
                tmp.append(l)
                if  "Working file:" in l:
                    name = l.split(":")[1].lstrip()            
        #print name
        #print tmp
        cvs2rss.handle_file(tmp, name)
        names.append(name)
        tmp = []

    opml = "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"
    opml += "<!-- OPML generated by iPodderCVS2RSS -->\n"
    opml += "<opml version=\"1.1\">\n"
    opml += "<head>\n";
    opml += "<title>mySubscriptions</title>\n";
    opml += "</head>\n";
    opml += "<body>\n";
    
    for n in names:
        li = n.split("/")
        n = li[len(li)-1]
        opml += "<outline text=\""+n+"\" description=\""+n+"\" title=\""+n+"\" type=\"rss\" version=\"RSS\" htmlUrl=\"http://ipodder.sourceforge.net/\" xmlUrl=\"http://ipodder.sourceforge.net/dev_feeds/"+n+".xml\"/>\n"
    
    opml += "</body>"
    opml += "</opml>"
    
    f = open("iPodderRss.opml", "w")
    f.write(opml)
    f.close()
    
    cvs2rss.ftp_batch += "put iPodderRss.opml\n"
    
    f = open("dev_feeds_batch", "w")
    f.write(cvs2rss.ftp_batch)
    f.close()
    
    os.system("sftp -b dev_feeds_batch rabshakeh@ipodder.sourceforge.net")

#runforfile("./ipodder/threads.py")    
runforfile("todo.txt iPodder.py iPodderGui.pyw ./gui/iPodder.xrc iPodderCVS2RSS.py ./ipodder/conlogging.py ./ipodder/feeds.py ./ipodder/hooks.py ./ipodder/players.py ./ipodder/configuration.py ./ipodder/engine.py ./ipodder/grabbers.py ./ipodder/outlines.py ./ipodder/threads.py iPodderWindows.py scheduler.py ./localization/LanguageModule.py ./localization/iPodderStringsDutch.py ./localization/iPodderStringsGerman.py ./localization/iPodderStringsEnglish.py ./localization/iPodderStringsItalian.py ./localization/iPodderStringsBrazilianPortuguese.py ./localization/iPodderStringsFrench.py ./localization/iPodderStringsSpanish.py ./images/badge_ipodder.gif ./images/donate_header_please.bmp ./images/donate_header_thanks.bmp ./images/newlogo_ipodder_animated.gif ./images/paypal.gif ./images/spacer.gif ./icons_status/application.ico ./icons_status/box-checked.png ./icons_status/box-unchecked.png ./icons_status/icon_checkselected20.png ./icons_status/icon_disabled.ico ./icons_status/icon_downloading.ico ./icons_status/icon_episode_blank.gif ./icons_status/icon_episode_downloading.gif ./icons_status/icon_episode_paused.gif ./icons_status/icon_episode_problem_broken.gif ./icons_status/icon_episode_problem_intact.gif ./icons_status/icon_episode_up-downloading.gif ./icons_status/icon_episode_uploading.gif ./icons_status/icon_feed_checking.gif ./icons_status/icon_feed_disabled.gif ./icons_status/icon_feed_disabled.png ./icons_status/icon_feed_downloading.gif ./icons_status/icon_feed_downloading.png ./icons_status/icon_feed_idle.gif ./icons_status/icon_feed_idle_empty.gif ./icons_status/icon_feed_idle_empty.png ./icons_status/icon_feed_unsubscribed.gif ./icons_status/icon_idle_empty.ico ./icons_status/icon_newitem.ico ./icons_status/icon_notconnected.ico ./icons_status/netflder.png ./icons_status/netflder_open.png ./icons_status/play-file.png ./icons_status/remote-sub.png ./icons_status/remote.png ./icons_status/sorting_arrow_down.png ./icons_status/sorting_arrow_up.png ./icons_status/tb_icon23_checkfeed.png ./icons_status/tb_icon25_addfeed.png ./icons_status/tb_icon25_canceldownload.png ./icons_status/tb_icon25_catchup.png ./icons_status/tb_icon25_checkfeed.gif ./icons_status/tb_icon25_checkfeed.png ./icons_status/tb_icon25_checkselectedfeed.png ./icons_status/tb_icon25_deletefeed.gif ./icons_status/tb_icon25_deletefeed.png ./icons_status/tb_icon25_feedproperties.png ./icons_status/tb_icon25_pausedownload.png ./icons_status/tb_icon25_removelines.png ./icons_status/tb_icon25_scheduler_off.png ./icons_status/tb_icon25_scheduler_on.png")

