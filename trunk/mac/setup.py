from distutils.core import setup
import os
import py2app
import sys
sys.path.append("/sw/lib/python2.3/lib-dynload")

NAME = "Juice"
DESCRIPTION = "Juice, the cross-platform podcast receiver."
VERSION = '2.2.3'
ICON = "iPodder.icns"

DATA_FILES  = [
        'favorites.txt',
	'gpl.txt',
        'readme.txt',
        'gui',
	'gui/iPodder.xrc', 
	'icons_status',
	'images',
        'localization',
        'mac',
        'plugins',
        'compat',
        'docs', 
        'iPodder.icns',
        'iPodderDoc.icns',
]

infoPlist = dict (
	#metadata
	CFBundleName = NAME,
	CFBundleVersion = VERSION,
	CFBundleGetInfoString = DESCRIPTION,
	CFBundleIconFile = ICON,
)

#constants for file type
MR_EXTENSION = "rss"
MR_MIME_TYPE = "application/rss+xml"

infoPlist["CFBundleDocumentTypes"] = [
    { "CFBundleTypeExtensions" : [MR_EXTENSION],
      "CFBundleTypeMIMETypes" : [MR_MIME_TYPE],
      "CFBundleTypeName": "Podcast Document",
      "CFBundleTypeIconFile": "iPodderDoc.icns",
      "LSIsAppleDefaultForType": True,
      "CFBundleTypeRole": "Viewer"}]
infoPlist["UTExportedTypeDeclarations"] = [
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

#Requires a GURL listener.
infoPlist["CFBundleURLTypes"] = [
                       { "CFBundleURLSchemes" : ['pcast'],
                         "CFBundleURLName": "Podcast URL",
                         "CFBundleTypeRole": "Viewer",
                         "LSIsAppleDefaultForType": "yes" }]

infoPlist["CFBundleShortVersionString"] = VERSION
infoPlist["CFBundleIdentifier"] = "net.sourceforge.ipodder"
infoPlist["CFBundleSignature"] = "IpdR"

py2app_options = dict(
        plist=infoPlist,
        #includes=['iPodderGui'],
)

setup(	
	app = ['gui.py'],
	data_files = DATA_FILES,
	options=dict(py2app=py2app_options,),
)
