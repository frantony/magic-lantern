#!/usr/bin/env python3

import subprocess as sub
import shlex
import tempfile
import time

repo_url = "https://bitbucket.org/hudson/magic-lantern"
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

class MLCloneException(Exception):
    pass

class MLBuildException(Exception):
    pass

class MLBuilder:
    def __init__(self, model, version, repository, branch="unified"):
        self.model = model
        self.version = version
        self.repository = repository
        self.branch = branch
        self.work_dir = tempfile.TemporaryDirectory(suffix="-mlbuild-"+model+"_"+version)

    def before_build(self):
        self.clone()

    def after_ok_build(self):
        pass

    def after_err_build(self, error):
        print("Build Failed!")
        print(error)

    def after_build(self):
        self.work_dir.cleanup()

    def do_build(self):
        start = time.monotonic()
        print("Building %s ver %s" % (self.model, self.version))
        p = sub.Popen(["make", self.model], stdout=sub.PIPE, stderr=sub.PIPE, cwd=self.work_dir.name)
        out,err = p.communicate()
        print("\tElapsed: ", time.monotonic()-start)
        if p.returncode != 0:
            raise MLBuildException({"stdout":out,"stderr":err})
        print(out.split())
        return (out,err)

    def clone(self):
        clone_string = "hg clone -r " + self.branch + " " + self.repository + " " + self.work_dir.name
        clone_cmd = shlex.split(clone_string)
        print("Cloning %s [%s] into %s" % (self.repository, self.branch, self.work_dir.name))
        sub.call(clone_cmd)

    def work(self):
        self.before_build()
        
        try:
            self.do_build()
        except Exception as e:
            self.after_err_build(e)
        else:
            self.after_ok_build()
        
        self.after_build()


def initial_clone(url=repo_url):
    clone_folder = tempfile.TemporaryDirectory(suffix="-mlbuild")
    print("Cloning %s [%s] into %s" % (url, branch, clone_folder.name))
    clone_string = "hg clone -r " + branch + " " + url + " " + clone_folder.name
    clone_cmd = shlex.split(clone_string)
    sub.call(clone_cmd)
    return clone_folder

if __name__ == "__main__":
    base_repo = initial_clone()
    for model,version in platforms.items():
        builder = MLBuilder(model, version, base_repo.name)
        builder.work()
        break
    base_repo.cleanup()