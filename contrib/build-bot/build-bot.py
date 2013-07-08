#!/usr/bin/env python3

import tempfile

from fm.magiclantern.Builder import Builder
from fm.magiclantern.RepoHandler import RepoHandler
import logging
from datetime import date, timedelta

#repo_url = "https://bitbucket.org/hudson/magic-lantern"
repo_url = "/home/nanomad/Progetti/magic-lantern"
branch   = "unified"
logFmt   = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(filename='ml-nightly.log',level=logging.DEBUG, format=logFmt)

platforms = {
    "1100D" : "105",
    "40D"   : "111",
    "500D"  : "111",
    "50D"   : "109",
    "550D"  : "109",
    "5D2"   : "212",
    "5D3"   : "113",
    "5DC"   : "111",
    "600D"  : "102",
    "60D"   : "111",
    "650D"  : "101",
    "6D"    : "113",
    "700D"  : "111",
    "7D"    : "203",
    "EOSM" : "106",
}

def save(content, path):
    fp = open(path,'w')
    fp.write(content)
    fp.close()

def build_changelog(r):
    banner = "Change log\n" + \
             "compiled from https://bitbucket.org/hudson/magic-lantern/changeset/"+r.id()+"\n" + \
             "===============================================================================\n"
    today = r.todays_changes()
    if(len(today) == 0): today = "No changes."

    yesterday = r.yesterdays_changes()
    if(len(yesterday) == 0): yesterday = "No changes."

    return "%s\nToday's changes:\n----------------\n%s\n\nYesterday's changes:\n--------------------\n%s\n\n" % (banner, today, yesterday)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("+----------------------------------+")
    logger.info("| ML Nightly build process started |")
    logger.info("+----------------------------------+")
    cloneDir = tempfile.TemporaryDirectory(suffix="-mlbuild")
    r = RepoHandler("/home/nanomad/Progetti/magic-lantern/", "unified")
    r.clone(cloneDir.name)
    changeLog = build_changelog(r)
    save(changeLog, "/tmp/ChangeLog.txt")
    builder = Builder("40D", "111", cloneDir.name, "unified")
    builder.injectConfig("/home/nanomad/Progetti/magic-lantern/Makefile.user")
    builder.work()
    cloneDir.cleanup()

    print("Nightly build should be OK")
