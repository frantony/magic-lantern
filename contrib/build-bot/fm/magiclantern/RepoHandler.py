import shlex
import subprocess as sub
import logging
from datetime import date, timedelta

class RepoHandler:
    """Utilty class representing a mercurial repository"""
    def __init__(self, url, branch=None):
        super(RepoHandler, self).__init__()
        self.url = url
        self.branch = branch
        self.logger = logging.getLogger(__name__)

    def clone(self, destination):
        if(self.branch is None):
            clone_cmd = " ".join(["hg clone", self.url , destination])
        else:
            clone_cmd = " ".join(["hg clone -b", self.branch , self.url ,destination])
        
        self.logger.info("Cloning %s [%s] into %s", self.url, self.branch, destination)        
        self.__quietCmd__(clone_cmd)

    def todays_changes(self):
        today = date.today()
        yesterday = today - timedelta(days = 1)
        return self.changelog(yesterday, today)

    def yesterdays_changes(self):
        end = date.today()- timedelta(days = 1)
        start = end - timedelta(days = 1)
        return self.changelog(start, end)

    def changelog(self, start, end):
        tmpl_frag = "--template '{node|short} | {author|user}: {desc|strip|firstline} \n'"
        log_cmd = "hg log "  + self.__hg_date_range__(start,end) + " " + tmpl_frag
        cmdString = shlex.split(log_cmd)
        out = sub.check_output(cmdString, universal_newlines=True)
        return out.strip()

    def id(self):
        cmdString = shlex.split("hg id -i -r .")
        out = sub.check_output(cmdString, universal_newlines=True)
        return out.strip()

    def __hg_date__(self, d):
        return d.strftime('%Y-%m-%d %H:%M:%S')

    def __hg_date_range__(self, start, end):
        _start = self.__hg_date__(start)
        _end   = self.__hg_date__(end)
        return '--date "' + _start + " to " + _end + '"'

    def __hg_changeset_before__(self, date):
        date_frag  = 'log --date <"' + self.__hg_date__(date) + '"'
        templ_frag = "--template '{date|localdate}:{node|short} \n'"

    def __quietCmd__(self, cmdString):
        cmdString = shlex.split(cmdString)
        sub.check_output(cmdString)
