
import  bundlebuilder, os 
from ipodder.configuration import __version__

#os.system("cp /System/Library/Frameworks/Python.framework/Versions/2.3/lib/python2.3/site-packages/wx-2.5.3-mac-unicode/wx/lib/mixins/listctrl.py .")

# I set this to make adding subfolders into the package easier
#packageroot = "/Users/erikdj/eclipse/workspace/iSpider" 
packageroot = "./"

# Create the AppBuilder
myapp = bundlebuilder.AppBuilder(verbosity = 1)

# Tell it where to find the main script - the one that loads on startup
myapp.mainprogram = os.path.join(packageroot, "gui.py") 

myapp.standalone = 1 
myapp.name = "Juice" 
myapp.iconfile=packageroot+'/iPodder.icns'

# includePackages forces certain packages to be added to the app bundle
myapp.includePackages.append("encodings") 
myapp.includePackages.append("_xmlplus") 
myapp.includePackages.append("_strptime")
myapp.includePackages.append("gzip")
myapp.includePackages.append("zipfile")
myapp.includePackages.append("platform")
myapp.includePackages.append("optparse")
myapp.includePackages.append("sgmllib")
myapp.includePackages.append("cgi")
myapp.includePackages.append("select")
myapp.includePackages.append("wxPython")
myapp.includePackages.append("Queue")
myapp.includePackages.append("localization")
myapp.includePackages.append("localization/catalog")
myapp.includePackages.append("shelve")
myapp.includePackages.append("Carbon")
myapp.includePackages.append("Carbon.Scrap")

# Here you add supporting files and/or folders to your bundle
myapp.resources.append(os.path.join(packageroot, "BitTorrent"))
myapp.resources.append(os.path.join(packageroot, "gui"))
myapp.resources.append(os.path.join(packageroot, "mp3"))
myapp.resources.append(os.path.join(packageroot, "icons_status"))
myapp.resources.append(os.path.join(packageroot, "images"))
myapp.resources.append(os.path.join(packageroot, "gpl.txt"))
myapp.resources.append(os.path.join(packageroot, "readme.txt"))
myapp.resources.append(os.path.join(packageroot, "todo.txt"))
myapp.resources.append(os.path.join(packageroot, "iPodder.icns"))
myapp.resources.append(os.path.join(packageroot, "iPodderDoc.icns"))

myapp.resources.append(os.path.join(packageroot, "iPodderGui.py"))
myapp.resources.append(os.path.join(packageroot, "gui/iPodderWindows.py"))

myapp.resources.append(os.path.join(packageroot, "ipodder"))
myapp.resources.append(os.path.join(packageroot, "ipodder/__init__.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/compatibility.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/configuration.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/conlogging.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/contrib"))
myapp.resources.append(os.path.join(packageroot, "ipodder/core.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/engine.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/feeds.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/grabbers.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/history.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/hooks.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/misc.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/outlines.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/players.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/state.py"))
myapp.resources.append(os.path.join(packageroot, "ipodder/threads.py"))

myapp.resources.append(os.path.join(packageroot, "compat"))
myapp.resources.append(os.path.join(packageroot, "compat/__init__.py"))
myapp.resources.append(os.path.join(packageroot, "compat/2x"))
myapp.resources.append(os.path.join(packageroot, "compat/2x/__init__.py"))
myapp.resources.append(os.path.join(packageroot, "compat/2x/iPodder.py"))

myapp.resources.append(os.path.join(packageroot, "localization"))
myapp.resources.append(os.path.join(packageroot, "localization/LanguageModule.py"))
myapp.resources.append(os.path.join(packageroot, "localization/__init__.py"))

myapp.resources.append(os.path.join(packageroot, "localization", "catalog"))
for f in os.listdir(os.path.join(packageroot, "localization", "catalog")):
    myapp.resources.append(os.path.join(packageroot, "localization", "catalog", f))

myapp.resources.append(os.path.join(packageroot, "/System/Library/Frameworks/Python.framework/Versions/2.3/lib/python2.3/bisect.py"))
myapp.resources.append(os.path.join(packageroot, "/System/Library/Frameworks/Python.framework/Versions/2.3/lib/python2.3/htmlentitydefs.py"))

#myapp.resources.append(os.path.join(packageroot, "/System/Library/Frameworks/Python.framework/Versions/2.3/lib/python2.3/site-packages/wx-2.5.3-mac-unicode/wx/lib/mixins"))
#myapp.resources.append(os.path.join(packageroot, "/Library/Python/2.3/wx-2.5.3-mac-unicode/wxPython/lib"))
#myapp.resources.append(os.path.join(packageroot, "/Library/Python/2.3/wx-2.5.3-mac-unicode/wx/lib/mixins"))
#myapp.resources.append(os.path.join(packageroot, "/Library/Python/2.3/wx-2.5.3-mac-unicode/wx/lib/mixins/listctrl.py"))

#myapp.resources.append(os.path.join(packageroot, "GenericDispatch.py"))
#myapp.resources.append(os.path.join(packageroot, "OPMLOutliner.py"))
#myapp.resources.append(os.path.join(packageroot, "bloglines.py"))
#myapp.resources.append(os.path.join(packageroot, "btdownloadlibrary.py"))
#myapp.resources.append(os.path.join(packageroot, "btshowmetainfo.py"))

# bundlebuilder does not yet have the capability to detect what shared libraries
# are needed by your app - so in this case I am adding the wxPython libs manually
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd-2.5.2.0.0.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd-2.5.2.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd-2.5.2.r")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd-2.5.2.rsrc") 
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd-2.5.dylib") 
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_gizmos-2.5.2.0.0.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_gizmos-2.5.2.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_gizmos-2.5.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_gl-2.5.2.0.0.dylib") 
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_gl-2.5.2.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_gl-2.5.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_ogl-2.5.2.0.0.dylib") 
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_ogl-2.5.2.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_ogl-2.5.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_stc-2.5.2.0.0.dylib") 
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_stc-2.5.2.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_stc-2.5.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_xrc-2.5.2.0.0.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_xrc-2.5.2.dylib")
#myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_xrc-2.5.dylib")

myapp.libs.append("/usr/local/lib/wxPython-unicode-2.5.3.1/lib/libwx_macud-2.5.3.0.0.dylib")
myapp.libs.append("/usr/local/lib/wxPython-unicode-2.5.3.1/lib/libwx_macud-2.5.3.rsrc") 
myapp.libs.append("/usr/local/lib/wxPython-unicode-2.5.3.1/lib/libwx_macud-2.5.3.dylib")
myapp.libs.append("//sw/lib/libdb-4.2.dylib")

#constants for file type
MR_EXTENSION = "rss"
MR_MIME_TYPE = "application/rss+xml"
actualVersion = __version__

myapp.plist["CFBundleDocumentTypes"] = [
    { "CFBundleTypeExtensions" : [MR_EXTENSION],
      "CFBundleTypeMIMETypes" : [MR_MIME_TYPE],
      "CFBundleTypeName": "Podcast Document",
      "CFBundleTypeIconFile": "iPodderDoc.icns",
      "LSIsAppleDefaultForType": True,
      "CFBundleTypeRole": "Viewer"}]
myapp.plist["UTExportedTypeDeclarations"] = [
    { "UTTypeIdentifier" : "com.sourceforge.ipodder.podcastrss",
      "UTTypeReferenceURL": "http://pswg.jot.com/WikiHome/OneClickSpec2",
      "UTTypeDescription": "Podcast Document",
      "UTTypeIconName": "iPodderDoc.icns",
      "UTTypeConformsTo" : ["public.text"],
      "UTTypeTagSpecification" : {
          "public.filename-extension" : [MR_EXTENSION],
          "public.mime-type" : MR_MIME_TYPE
       }
     }]

# this also may have an uti counterpart
myapp.plist["CFBundleURLTypes"] = [
                       { "CFBundleURLSchemes" : ['podcast','pcast'],
                         "CFBundleURLName": "podcast URL",
                         "CFBundleURLIconFile" : "iPodderDoc.icns",
                         "LSIsAppleDefaultForScheme": True}]

myapp.plist["CFBundleShortVersionString"] = actualVersion
#myapp.plist["CFBundleVersion"] = "builddate"

myapp.plist["CFBundleIdentifier"] = "net.sourceforge.ipodder"
myapp.plist["CFBundleSignature"] = "IpdR"

# Here we build the app!
myapp.setup () 
myapp.build ()
