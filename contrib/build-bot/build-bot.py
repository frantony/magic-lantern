#!/usr/bin/env python3

import tempfile

from fm.magiclantern.Builder import Builder
from fm.magiclantern.RepoHandler import RepoHandler
import logging

#repo_url = "https://bitbucket.org/hudson/magic-lantern"
repo_url = "/home/nanomad/Progetti/magic-lantern"
branch   = "unified"
logging.basicConfig(filename='example.log',level=logging.DEBUG)

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

if __name__ == "__main__":
    cloneDir = tempfile.TemporaryDirectory(suffix="-mlbuild")
    r = RepoHandler("/home/nanomad/Progetti/magic-lantern-newmake/", "ppluciennik/new_makefile_system")
    r.clone(cloneDir.name)
    builder = Builder("650D", "101", cloneDir.name, "ppluciennik/new_makefile_system")
    builder.injectConfig("/home/nanomad/Progetti/magic-lantern/Makefile.user")
    builder.work()
    cloneDir.cleanup()
