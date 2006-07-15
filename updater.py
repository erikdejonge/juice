"""
iPodder updater module. 

Only use this in iPodderCli.py and iPodderGui.pyw!

BEFORE you start importing other parts of iPodder, import this and call
loadUpdates(). 

We'll look for the most recent looking zip files matching
ipodder-YYYY-MM-DD.zip we can find in the directory from which the program
was run. I'm hoping that sys.argv[0] is preserved in py2exe software. 

We'll insert the zip file into sys.path AT THE BEGINNING.  That means that
anything you import from then on will come out of the zip file if it's
there. If not, hey, it won't. :) 

To open a file from the update archive (if present), use the open() method.
Easy, huh? 

Caveats: 
    
* Make sure that the paths in the zip file match the paths you'll be trying 
  to import. 
  
* Include *all* of a package (ipodder/* or gui/*), not just individual 
  modules in it. I'm pretty sure that the result will be messy if you get 
  it wrong. 
"""

import sys
import os
import os.path
import re
import time
import zipfile
import StringIO

loadedUpdates = {}

def getrundir(): 
    "Determine the run directory."
    return os.path.abspath(os.path.split(sys.argv[0])[0])

def testit(zipfile): 
    assert zipfile.testzip() is None, "Bad archive."
    
def loadupdates(signaturetag='juice'): 
    """Find update archives and insert them into the import chain."""
    assert signaturetag == 'juice', \
            "Haven't figured out a sensible way to handle file imports " \
            "from multiple tags yet, so disabling it."
    if loadedUpdates.has_key(signaturetag): 
        return # don't do it more than once per signature
    rundir = getrundir()
    logfile = os.path.join(rundir, 'updater.log')
    try: 
        log = file(logfile, 'wt')
    except (OSError, IOError):
        # Commenting this out because it causes error dialogs on
        # py2exed dists.  But this isn't really an error because user
        # may not have write access on the rundir.
        # print >> sys.stderr, "Can't open updater log file %s for writing." % logfile
        log = None
    tell(log, "Looking for update archives...")
    
    signature = r"%s\-([0-9]{4})\-([0-9]{2})\-([0-9]{2}).zip" % signaturetag
    matcher = re.compile(signature, re.IGNORECASE)
    updates = {}
    for filename in os.listdir(rundir): 
        match = matcher.match(filename)
        if match is None: 
            continue # file didn't match the signature
        year, month, day = [int(s) for s in match.groups()]
        timestamp = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
        updates[timestamp] = os.path.join(rundir, filename)
    if not updates: # couldn't find any modules
        tell(log, "No updates found.")
        return

    timestamps = updates.keys()
    timestamps.sort()
    timestamps.reverse()
    for timestamp in timestamps: 
        update = updates[timestamp]
        tell(log, "Trying update archive: %s" % update)
        zip = zipfile.ZipFile(update, 'r')
        if zip.testzip() is not None: 
            tell(log, "Bad archive ignored.")
            continue
    tell(log, "Success.")
    sys.path.insert(0, update)
    loadedUpdates[signaturetag] = {
        'filename': update, 
        'object': zip, 
        }

def open(filename, mode='r', signaturetag='ipodder'): 
    "Open a file either from the update or the run directory."
    assert mode in ('r', 'rt', 'rb')
    updateinfo = loadedUpdates.get(signaturetag)
    if updateinfo is not None: 
        try: 
            zipfile = updateinfo['object']
            fileinfo = zipfile.getinfo(filename)
            return StringIO.StringIO(zipfile.read(filename))
        except KeyError: 
            pass
    return file(os.path.join(getrundir(), filename, mode))
 
def tell(log, message): 
    "Warn the users."
    # Commenting this out because it causes error dialogs on
    # py2exed dists.  This could be made clever obviously.
    # print >> sys.stderr, message
    if log is not None: 
        print >> log, message

if __name__ == '__main__': 
    loadupdates()
    print sys.path
    from ipodder import history
    print history.__file__
    print ''.join(open(os.path.join('ipodder', 'history.py')).readlines()[1:5])+'...'

