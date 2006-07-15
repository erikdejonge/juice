import _winreg
import sys
from os.path import abspath
import logging

#constants for MIME type support
log = logging.getLogger('Juice')

def read_reg_key(key,subkey,value):
    """Return info,type for the data at key\subkey\value."""
    openkeys = []

    try:    
        try:
            key = _winreg.OpenKeyEx(key,subkey,0,_winreg.KEY_QUERY_VALUE)
            openkeys.insert(0,key)
            return _winreg.QueryValueEx(key, value)
        finally:
            for key in openkeys:
                _winreg.CloseKey(key)
    except WindowsError, e:
        errno, message = e.args
        if errno != 2:
            raise e

    return (None,None)

def deregister_file_extension(ext):
    """Remove ourselves as the default handler for the file extension, setting
    the first available alternative handler if found."""
    openkeys = []
    replacement = ""
    try:    
        try:
            key = _winreg.OpenKeyEx(_winreg.HKEY_CLASSES_ROOT,"%s\\OpenWithProgIds" % ext,0,_winreg.KEY_QUERY_VALUE)
            openkeys.insert(0,key)
            for i in range(0,_winreg.QueryInfoKey(key)[1]):
                value = _winreg.EnumValue(key,i)[0]
                if value and value != "Juice%s" % ext:
                    replacement = value   
            key = _winreg.OpenKeyEx(_winreg.HKEY_CLASSES_ROOT,ext,0,_winreg.KEY_ALL_ACCESS)
            openkeys.insert(0,key)
            _winreg.SetValueEx(key,"",0,_winreg.REG_SZ,replacement)
        finally:
            for key in openkeys:
                _winreg.CloseKey(key)
    except WindowsError, e:
        errno, message = e.args
        if errno != 2:
            raise e

def deregister_pseudo_protocol(protocol):
    """Remove the open command for this protocol handler."""
    subkey = protocol.split("://")[0]
    openkeys = []
    try:    
        try:
            key = _winreg.OpenKeyEx(_winreg.HKEY_CLASSES_ROOT,"%s\\shell\\open" % subkey,0,_winreg.KEY_ALL_ACCESS)
            openkeys.insert(0,key)
            _winreg.DeleteKey(key,"command")
        finally:
            for key in openkeys:
                _winreg.CloseKey(key)
    except WindowsError, e:
        log.exception("Error deregistering protcol handler for '%s'" % subkey)

try:
    OPEN = read_reg_key(_winreg.HKEY_CLASSES_ROOT,"Applications\Juice.exe\shell\open\command","")[0]
except:
    OPEN = None

if OPEN == None:
    log.exception("oneclick.py: Couldn't find Juice registry keys.  No one-click behaviors will be registered.")

# Value format is: display name, list of key, subkey, value, data

#ADD DEREG ACTIONS
FILE_TYPES = { \
    'filetype_rss' : ('.rss', \
         [ \
             (_winreg.HKEY_CLASSES_ROOT,'.rss','','Juice.rss'), \
             (_winreg.HKEY_CLASSES_ROOT,'.rss','PerceivedType','text'), \
             (_winreg.HKEY_CLASSES_ROOT,'.rss','Content Type','application/rss+xml'), \
         ], \
         deregister_file_extension, \
    ), \
    'filetype_pcast' : ('.pcast', \
         [ \
             (_winreg.HKEY_CLASSES_ROOT,'.pcast','','Juice.pcast'), \
             (_winreg.HKEY_CLASSES_ROOT,'.pcast','PerceivedType','text'), \
             (_winreg.HKEY_CLASSES_ROOT,'.pcast','Content Type','application/x-podcast'), \
         ], \
         deregister_file_extension, \
    ), \
    'filetype_pcast_protocol' : ('pcast://', \
         [ \
             (_winreg.HKEY_CLASSES_ROOT,'pcast','','URL: Pcast Protocol'), \
             (_winreg.HKEY_CLASSES_ROOT,'pcast','URL Protocol',''), \
             (_winreg.HKEY_CLASSES_ROOT,'pcast\shell\open\command','',OPEN), \
         ], \
         deregister_pseudo_protocol, \
    ),
    'filetype_podcast_protocol' : ('podcast://', \
         [ \
             (_winreg.HKEY_CLASSES_ROOT,'podcast','','URL: Podcast Protocol'), \
             (_winreg.HKEY_CLASSES_ROOT,'podcast','URL Protocol',''), \
             (_winreg.HKEY_CLASSES_ROOT,'podcast\shell\open\command','',OPEN), \
         ], \
         deregister_pseudo_protocol, \
    ),
}
    
def do_registrations(config,force,deregistered_types=[]):
    
    if OPEN == None:
        log.debug("do_registrations: registry is in an unknown state, giving up.")
        return

    #Deal with any deregistrations.
    for filetype in FILE_TYPES.keys():
        if filetype in deregistered_types:
            (name,regkeys,unreg_proc) = FILE_TYPES[filetype]
            if unreg_proc:
                unreg_proc(name)
    
    (am_i,was_anybody,unregistered_config_attrs) = am_i_registered(config)
    log.debug("am_i_registered returns: %s,%s" % (str(am_i),str(was_anybody)))
              
    if am_i:
        return (True, was_anybody,[])

    if was_anybody and not force:
        return (False, True,unregistered_config_attrs)

    #If we get here we're either forcing or registering for the first time.
    unregistered_config_attrs = []
    for filetype in FILE_TYPES.keys():
        attr = "handle_%s" % filetype
        if getattr(config,attr,False):
            (name,regkeys,unreg_proc) = FILE_TYPES[filetype]
            log.debug("Registering file type: %s" % name)
            for (key, subkey, value, data) in regkeys:
                openkeys = []
                try:
                    kh = _winreg.CreateKey(key,subkey)
                    openkeys.insert(0,kh)
                    _winreg.SetValueEx(kh,value,0,_winreg.REG_SZ,data)
                finally:
                    for kh in openkeys:
                        _winreg.CloseKey(kh)
            
    return (True, was_anybody,[])

def am_i_registered(config):
    """Returns a three-tuple (am_i_registered,was_anybody_registered,unregistered_config_attrs)."""
    
    if OPEN == None:
        log.debug("am_i_registered: registry is in an unknown state, giving up.")
        return

    am_i = True
    was_anybody = False
    unregistered_attrs = []
    
    for filetype in FILE_TYPES.keys():
        attr = "handle_%s" % filetype
        if getattr(config,attr,False):
            (name,regkeys,unreg_proc) = FILE_TYPES[filetype]
            log.debug("Checking if we're registered for file type: %s" % name)
            for (key, subkey, value, data) in regkeys:
                regdata = read_reg_key(key,subkey,value)[0]
                log.debug("Path: %s\\%s\\%s: expected: %s, got: %s" % (key,subkey,value,data,regdata))
                if regdata != data:
                    am_i = False
                    if regdata != None:
                        if attr not in unregistered_attrs:
                            unregistered_attrs.append(attr)
                        was_anybody = True
        else:
            log.debug("Not registered for file type %s, so not checking" % filetype)

    return (am_i,was_anybody,unregistered_attrs)
