from fm.magiclantern.Logger import Logger
from fm.magiclantern.Exceptions import BuildException

import time
import tempfile
import subprocess as sub
import shlex

class Builder:
    def __init__(self, model, version, repository, branch="unified"):
        self.model      = model
        self.version    = version
        self.repository = repository
        self.branch     = branch
        self.work_dir   = tempfile.TemporaryDirectory(suffix="-mlbuild-"+model+"_"+version)
        self.logger     = Logger("/home/nanomad/")
        self.customConfig  = None

    def injectConfig(self, fName):
        self.customConfig = fName

    def before_build(self):
        self.clone()
        if(self.customConfig is not None):
            fpIN = open(self.customConfig)
            fpOUT = open(self.work_dir.name + "/Makefile.user", "w")
            lines = fpIN.readlines()
            fpOUT.writelines(lines)
            fpOUT.close()
            fpIN.close()

    def after_ok_build(self):
        pass

    def after_err_build(self, error):
        self.logger.error("BUILD", "Compilation failed")
        self.logger.error("BUILD", error)

    def after_build(self):
        self.work_dir.cleanup()

    def do_build(self):
        self.logger.info("BUILD", "Building %s ver %s" % (self.model, self.version))
        p = sub.Popen(["make", self.model], stdout=sub.PIPE, stderr=sub.PIPE, cwd=self.work_dir.name)
        out,err = p.communicate()
        if p.returncode != 0:
            raise BuildException({"stdout":out,"stderr":err})
        print(out.split())
        return (out,err)

    def clone(self):
        clone_string = " ".join(["hg clone -r", self.branch , self.repository ,self.work_dir.name])
        clone_cmd = shlex.split(clone_string)
        self.logger.info("CLONE", ("Cloning %s [%s] into %s" % (self.repository, self.branch, self.work_dir.name)))
        sub.check_output(clone_cmd)

    def work(self):
        start = time.monotonic()
        self.before_build()
        
        try:
            self.do_build()
        except Exception as e:
            self.after_err_build(e)
        else:
            self.after_ok_build()
        
        self.after_build()

        self.logger.info("BUILD", "\tElapsed: " + str(time.monotonic()-start))
