"""gatherer.py gathers a lot of system information on *nix boxes"""
import os
import subprocess
import time
import sys

class Gatherer:
    
    
    def __init__(self, n=5):
        # n is the number of points a short toplist has, like the list of
        # most active processes.
        self.n = n
        #
        # Static attributes of the environment are saved here, the dynamic
        # stuff gets set by the self.refresh() function.
        self.os = os.name                           # operating system name
        self.working_directory = os.getcwd()        # working directory
        self.uid = os.geteuid()                     # id of executing user
        self.gid = os.getgid()                      # group id of above user
        self.login = os.getlogin()                  # username of above user
        self.pid = os.getpid()                      # my process id
        self.ppid = os.getppid()                    # my parent's process id
        self.system = os.uname()[0]                 # similar to self.os
        self.hostname = os.uname()[1]               # current host's name
        self.system_release = os.uname()[2]         # similar to self.os_version
        self.system_version = os.uname()[3]         # OS' version
        self.machine = os.uname()[4]                # info on the machine itself
        self.python = sys.version.split()[0]        # Python version

        self.refresh()
    
    def refresh(self, attribute=""):
        """Called whenever an update is made."""
        self.time = time.time()
        #self.top_processes = self._most_active_processes(self.n)
        self.uptime = self._get_output("uptime")
    
    def export_as_string(self):
        return "os=%s::working_directory=%s::uid=%s::gid=%s::login=%s::pid=%s::ppid=%s::\
system=%s::hostname=%s::system_release=%s::system_version=%s::machine=%s::python=%s::\
top_process=%s" % (self.os, self.working_directory, self.uid, self.gid, self.login, self.pid,
self.ppid, self.system, self.hostname, self.system_release, self.system_version, self.machine,
self.python, self.top_processes)
    
    def _most_active_processes(self, number):
        """Returns a list of the n most active processes."""
        output = self._get_output("ps -ax")
        li = []
        for line in output.split("\n")[1:-1]:
            pid = line.split()[0]
            process = line.split()[3].split("/")[-1]
            li.append((pid, process))
        return li[0:number]
    
    def _get_output(self, command, stdout = True, stderr = False):
        """
        Runs a program specified in the first argument and returns its output
        as a string.
    
        Borrowed from P1tr (https://launchpad.net/p1tr).
        """
        if (stdout or stderr) and not (stdout and stderr):
            pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            if stdout:
            	return pipe.stdout.read()
            else:
            	return pipe.stderr.read()
        elif stdout and stderr:
        	return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).stdout().read()
        else:
            try:
                return bool(subprocess.Popen(command))
            except OSError:
                print "Failed to execute process %s for updating system stats." % command
                return "N/A"