import shlex
import subprocess as sub
from fm.magiclantern.Logger import Logger

class RepoHandler:
	"""Utilty class representing a mercurial repository"""
	def __init__(self, url, branch=None):
		super(RepoHandler, self).__init__()
		self.url = url
		self.branch = branch
		self.logger = Logger("/home/nanomad")

	def clone(self, destination):
		if(self.branch is None):
			clone_cmd = " ".join(["hg clone", self.url , destination])
		else:
			clone_cmd = " ".join(["hg clone -b", self.branch , self.url ,destination])
		
		self.logger.info("CLONE", ("Cloning %s [%s] into %s" % (self.url, self.branch, destination)))		
		self.__quietCmd__(clone_cmd)

	def __quietCmd__(self, cmdString):
		cmdString = shlex.split(cmdString)
		sub.check_output(cmdString)
