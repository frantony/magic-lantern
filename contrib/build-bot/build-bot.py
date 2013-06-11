#!/usr/bin/env python3

import subprocess as sub
import shlex
import tempfile

from fm.magiclantern.Builder import Builder
from fm.magiclantern.RepoHandler import RepoHandler

#repo_url = "https://bitbucket.org/hudson/magic-lantern"
repo_url = "/home/nanomad/Progetti/magic-lantern"
branch   = "unified"

platforms = {
    "1100D" : "105",
    "40D" : "111",
    "500D" : "111",
    "50D" : "109",
    "550D" : "109",
    "5D2" : "212",
    "5D3" : "113",
    "5DC" : "111",
    "600D" : "102",
    "60D" : "111",
    "650D" : "101",
    "6D" : "113",
    "700D" : "111",
    "7D" : "203",
    "7D_MASTER" : "203",
    "EOSM" : "106",
}

def initial_clone(url=repo_url):
    clone_folder = tempfile.TemporaryDirectory(suffix="-mlbuild")
    print("Cloning %s [%s] into %s" % (url, branch, clone_folder.name))
    clone_string = "hg clone -r " + branch + " " + url + " " + clone_folder.name
    clone_cmd = shlex.split(clone_string)
    sub.call(clone_cmd)
    return clone_folder

if __name__ == "__main__":
    cloneDir = tempfile.TemporaryDirectory(suffix="-mlbuild")
    r = RepoHandler("/home/nanomad/Progetti/magic-lantern/", "unified")
    r.clone(cloneDir.name)
    #base_repo = initial_clone()
    #for model,version in platforms.items():
    #    builder = Builder(model, version, base_repo.name)
    #    builder.work()
    #    break
    #base_repo.cleanup()
