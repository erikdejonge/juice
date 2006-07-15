#
# iPodder OPML outliner aka iPodder Tuner
#
# The ourliner starts at a user specified opml starting point
# a good example is the ipodder.org directory 
#
# the url is:  http://www.ipodder.org/discuss/reader$4.opml
#
# the user can then use the tree-control which was build out of the opml file to subscribe to podcasts
#
#
# edj 17 oktober 2004: initial alogorithm, needs lots of graphical and ui enhancements.
# edj 13 november 2004: made the opml outliner resizable.
#

from wxPython.wx import *
import types
from xml.sax import make_parser, handler
from gui import images
import wx
import logging
import urllib2, socket
import os.path
import sys
import urllib 
import pickle, shelve
from ipodder import configuration
import StringIO
import threading
import time

log = logging.getLogger('iPodder.Outliner')
basepath = os.path.abspath(os.path.split(sys.argv[0])[0])

def PrintLog(logpanel, message):
	log.debug("%s", message)
	try:
		if logpanel==-1:
			print logpanel
			print message
		else:
			# should do reflection here to support all kind of controls
			# for now we assume wx.TextCtrl
			logpanel.SetValue(message)
	except:
		log.exception("Failed to print to log panel.")
		pass
     
class OPMLCache:
    class __impl(threading.Thread):
        def __init__(self):
            self.m_opml_streams = {}
            threading.Thread.__init__(self)

        def run(self):
            self.RefreshCache(log) 	
            
        def Init(self, state):
            self.m_state = state

            for i in configuration.configOptions:
                if i[0]=="podcast_directory_roots":
                    for j in i[1]:
                        self.AddStream(j[0])
			
        def AddStream(self, theurl):
             if self.m_state.has_key(theurl):
                 self.m_opml_streams[theurl]=self.m_state[theurl]
             else:
                 self.m_opml_streams[theurl]=theurl
                 
        def HasOPML(self, url):
			return self.m_opml_streams.has_key(url)
			
        def GetOPML(self, url):
			return self.m_opml_streams[url]
      			
      	def RefreshCache(self, log):
             for opmlurl in self.m_opml_streams:
                 log.info("checking "+opmlurl)
                 try:
                     dwnopml = urllib.urlopen(opmlurl) 
                     theopml = ""
                     for line in dwnopml:
                         theopml = theopml + line
                     self.m_state[opmlurl]=theopml	
                     self.m_opml_streams[opmlurl]=theopml
                 except:
                     log.info(opmlurl+" failed")
	
    __instance = None
    def __init__(self):
        if OPMLCache.__instance is None:
            OPMLCache.__instance = OPMLCache.__impl()
        self.__dict__['_OPMLCache__instance'] = OPMLCache.__instance                
    def __getattr__(self, attr):
        return getattr(self.__instance, attr)
    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

class OutlineNode:
	def __init__(self, name, url):
		self.m_name = name
		self.m_url = url
		self.m_scanned = False
                
# uses a dictionary to keep track of treenode pointers
# key is the name-path of the tree 
# value is the wxPython treectrl node (a pointer)
class OPMLEventHandler(handler.ContentHandler):
	def __init__(self):
		self.m_chanTitle = ""
		self.m_path = ""
		self.m_tree_path = ""
		self.m_tree = {} 
		
	def startElement(self, name, attrs):  
		self.m_path += "/" + name
		if self.m_path == "/opml/head/title":
			self.m_chanTitle = ""
		
		if name=="outline" and attrs.has_key("text"):
			self.m_tree_path += "<*:)*>" + attrs["text"]			
	
			new_node = False
			parent = self.m_current_node
			
			previous_parent_path = self.m_tree_path[0:self.m_tree_path.rfind('<*:)*>')]
			if self.m_tree.has_key(previous_parent_path):
				parent = self.m_tree[previous_parent_path]				
				
			url = ""
			if attrs.has_key("url"):
				url = attrs["url"]
			self.m_tree[self.m_tree_path]= self.m_lazy_tree.AddGenericItem(parent, attrs["text"], url)
			
	def endElement(self,name):
		self.m_path = self.m_path[0:self.m_path.rfind('/')]		
		self.m_tree_path = self.m_tree_path[0:self.m_tree_path.rfind('<*:)*>')]
		
	def characters(self,ch):
		if self.m_path == "/opml/head/title":
			self.m_chanTitle += ch   
                      
class iPodderTuner:		
	def scanoutlines(self):
		try:
			opmlhandler = OPMLEventHandler()
			opmlhandler.m_lazy_tree = self.m_lazy_tree 
			opmlhandler.m_current_node = self.m_current_node	

			for contenturl in self.m_urls:
				parser = make_parser()
				try:
					parser.setContentHandler(opmlhandler)
					opmlcache = OPMLCache()
					if opmlcache.HasOPML(contenturl)==True:
						data = StringIO.StringIO(opmlcache.GetOPML(contenturl))						
						parser.parse(data)    
					else:
						parser.parse(contenturl)    
				except urllib2.URLError, ex: 
					if isinstance(ex.reason, socket.error): 
						args = ex.reason.args
						if len(args) == 2: 
							code, message = args
							if code == 10061: 
								log.error("Connection refused by %s", contenturl)
							else: 
								log.error("Socket error \"%s\" (%d) trying to fetch %s", message, code, contenturl)
						elif len(args) == 1: 
							message = args[0]
							if message == 'timed out': 
								log.error("Connection timeout trying to fetch %s", contenturl)
							else: 
								log.error("Socket error \"%s\" trying to fetch %s", contenturl, args[0])
						else: 
							log.exception("Unidentified socket error trying to fetch %s.", contenturl)
					else: 
						log.debug("URLError trying to fetch %s: %s", contenturl, repr(ex.reason))
				except:
					log.exception("Couldn't parse %s", contenturl)
					#PrintLog (self.logpanel, "nothing here "+contenturl)
		except:
			log.exception("Couldn't scan the outlines.")
			#PrintLog (self.logpanel, "scanoutlines did not succeed")
			pass
	
	def parseoutlinedirectories(self, directory_uri):
		#hardcoded for now
		self.m_urls = []
		self.m_urls.append(directory_uri)

class OPMLTree(wxTreeCtrl):
	'''Lazy Tree is a simple "Lazy Evaluation" tree,
	that is, it only adds items to the tree view when
	they are needed.'''
	def __init__(self):
            p = wx.PreTreeCtrl()
            self.PostCreate(p)
            
	def Init(self,rootNodes):
		EVT_TREE_ITEM_EXPANDING(self, self.GetId(), self.OnExpandNode)
		EVT_TREE_SEL_CHANGED(self, self.GetId(), self.OnSelectNode)

		isz = (16,16)
		il = wx.ImageList(isz[0], isz[1])
		self.fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
		self.fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
		self.fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, isz))
		self.smileidx    = il.Add(images.getSmilesBitmap())
		self.netfldridx  = il.Add(getNetFolderBitmap())
		self.remoteidx   = il.Add(getRemoteBitmap())
                
		self.SetImageList(il)
		self.il = il
		self.logpanel = -1
		
		rootID = self.AddGenericItem(None, "Directories", '')
		for url, name in rootNodes: 
			self.AddGenericItem(rootID, name, url)
		self.Expand(rootID)

	def SetLogPanel(self, logpanel):
		self.logpanel = logpanel
		
	def OnExpandNode( self, event ):		
		ID = event.GetItem()
		node = self.GetPyData(ID)
		
	def OnSelectNode( self, event ):		
		ID = event.GetItem()
		node = self.GetPyData(ID)
		self.ScanNode(node, ID)
		
	def ScanNode(self, node, ID): 
		ext = node.m_url.split(".")
		if ext[len(ext)-1].lower()=="opml" and not node.m_scanned:
			PrintLog (self.logpanel, node.m_url)			
			ipt = iPodderTuner()	
			ipt.m_current_node = ID
			ipt.m_lazy_tree = self
			ipt.parseoutlinedirectories(node.m_url)
			ipt.scanoutlines()
			node.m_scanned = True
		else:
			if node.m_url!="":
				self.m_current_node=node.m_url
				PrintLog (self.logpanel, node.m_url)
		#url
		
	def AddRootItem( self, node ):
		rootUrl, rootName = node
		self.AddGenericItem(None, rootName, rootUrl)		
  
	def AddGenericItem(self, parentID, node, url):
		name = self.GetName( node )

		if parentID is None:
			ID = self.AddRoot( name, )
		else:
			ID = self.AppendItem( parentID, name )
		
		if url=="":
			self.SetItemImage(ID, self.fldridx, )			
		else:
			ext = url.split(".")
			if ext[-1].lower()=="opml":		
				self.SetItemImage(ID, self.netfldridx, )	
			else:		
				self.SetItemImage(ID, self.remoteidx, )	
			
		self.SetPyData(ID, OutlineNode(node, url))
		
		if self.GetChildren( node ):
			self.SetItemHasChildren( ID, TRUE )
		return ID
	 
	def GetName( self, node ):
		return str(node)
	 
	def GetChildren( self, node ):
		if type(node) in (types.ListType, types.TupleType):
			return node
		else:
			return []
			
def getNetFolderBitmap():
    bmp = wx.Bitmap(os.path.join(basepath,'netflder.png'), wx.BITMAP_TYPE_PNG)
    return bmp

def getRemoteBitmap():
    bmp = wx.Bitmap(os.path.join(basepath,'remote.png'), wx.BITMAP_TYPE_PNG)
    return bmp
    
from ipodder.configuration import *

def rununittest():	
    state = shelve.open("test.db", 'c',
                        writeback=False, protocol=pickle.HIGHEST_PROTOCOL)
    opmlc = OPMLCache()
    opmlc.Init(state)
    opmlc.setDaemon(True)
    opmlc.start()
    for i in configuration.configOptions:
        if i[0]=="podcast_directory_roots":
            for j in i[1]:
	                opmlc.GetOPML(j[0])
    while True:
        print "main thread"
        time.sleep(1)
        
if __name__ == "__main__":
	logging.basicConfig()
	log.setLevel(logging.DEBUG)
	rununittest()
