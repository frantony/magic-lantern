from fm.magiclantern.Exceptions import BuildException

import time
import tempfile
import subprocess as sub
import shlex
import os
import logging


class Builder:
    def __init__(self, model, version, repository, branch="unified"):
        self.model        = model
        self.version      = version
        self.repository   = repository
        self.branch       = branch
        self.work_dir     = tempfile.TemporaryDirectory(suffix="-mlbuild-"+model+"_"+version)
        self.platform_dir = os.path.join(self.work_dir.name, "platform", self.model + "." + self.version)
        self.customConfig = None
        self.logger       = logging.getLogger(__name__)

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
        files = os.listdir(self.platform_dir)

    def after_err_build(self, error):
        self.logger.error("Compilation failed!")
        self.logger.exception(error)

    def after_build(self):
        self.work_dir.cleanup()

    def do_build(self):
        self.logger.info("Building %s ver %s in %s" , self.model, self.version, self.platform_dir)
        p = sub.Popen(["make", "zip"], stdout=sub.PIPE, stderr=sub.PIPE, cwd=self.platform_dir)
        out,err = p.communicate()
        self.logger.debug("Build output:")
        for l in out.split("\n"):
            self.logger.debug(l)
        for l in err.split("\n"):
            self.logger.warn(l)
        if p.returncode != 0:
            raise BuildException({"stdout":out,"stderr":err})
        return (out,err)

    def clone(self):
        clone_string = " ".join(["hg clone -r", self.branch , self.repository ,self.work_dir.name])
        clone_cmd = shlex.split(clone_string)
        self.logger.info("Cloning %s [%s] into %s", self.repository, self.branch, self.work_dir.name)
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

        self.logger.info("\tElapsed: %s",  str(time.monotonic()-start))
