#!/usr/bin/python2.3
#
# mkconstants.py -- Extract constants from Gmail Javascript code
#
# $Revision: 1.1 $ ($Date: 2004/12/04 13:47:07 $)
#
# Author: follower@myrealbox.com
#
# License: GPL 2.0
#
# This tool parses the Javascript file used by Gmail, extracts
# useful constants and then generates an importable Python module.
#
# 2004-07-11: Hmmm, this script is not really any use now because
#             Gmail no longer includes the constants definitions
#             in the Javascript...
#

import re
import sys
import time

OUTPUT_FILENAME = "constants.py"

# These enumerations start at 1 rather than 0 -- I haven't looked into
# why they're are different. We want them to work correctly for Python
# sequences so we have to fudge them and subtract one from each value.
# NOTE: This means we can't send these values back, but that shouldn't be
#       a problem.
FUDGE_OFFSET_PREFIXES = ["QU", "TS", "CS", "MI", "SM", "AR"]

# Used to filter out only the constants we want to use at the moment.
USEFUL_PREFIXES = ["D", "T", "CT", "A"] + FUDGE_OFFSET_PREFIXES
USEFUL_SUFFIXES = ["SEARCH", "START", "VIEW", "COOKIE", "THREAD", "ACTION"]
USEFUL_NAMES = ["U_REFERENCED_MSG", "U_DRAFT_MSG"]
RE_CONSTANTS = "var ([A-Z]{1,}_[A-Z_]+?)=(.+?);"

VAR_JS_VERSION = "js_version"

FMT_DEFINITION = "%s = %s\n"

FILE_HEADER = """\
#
# Generated file -- DO NOT EDIT
#
# %s -- Useful constants extracted from Gmail Javascript code
#
# Source version: %s
#
# Generated: %s
#

""" % (OUTPUT_FILENAME, "%s",
       time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()))

if __name__ == "__main__":
    lines = []

    try:
        inputFilename = sys.argv[1]
    except IndexError:
        print "Usage: mkconstants.py <gmail.js>"
        raise SystemExit

    print "Reading `%s`..." % inputFilename
    code = open(inputFilename).read()

    jsVersion = re.search("var %s=(.+?);" % VAR_JS_VERSION, code).group(1)

    lines.extend([FMT_DEFINITION % (VAR_JS_VERSION, jsVersion), "\n"])

    matches = re.findall(RE_CONSTANTS, code)

    for name, value in matches:
        prefix = name[:name.index("_")]
        suffix = name[name.rindex("_")+1:]

        if prefix in USEFUL_PREFIXES or suffix in USEFUL_SUFFIXES or \
               name.startswith("U_AS_") or name.startswith("U_COMPOSE") or \
               name.startswith("U_ACTION_") or \
               name in USEFUL_NAMES:
            if prefix in FUDGE_OFFSET_PREFIXES:
                value = int(value) - 1
            lines.append(FMT_DEFINITION % (name, value))

    lines.insert(0, FILE_HEADER % jsVersion.strip("'"))

    print "Writing `%s`..." % OUTPUT_FILENAME
    open(OUTPUT_FILENAME, "w").writelines(lines)

    print "Done."
    
