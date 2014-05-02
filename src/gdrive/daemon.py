#!/usr/bin/env python
from __future__ import division, with_statement, print_function, unicode_literals

import sys
import os
import io
import time
import atexit
import errno
import abc
import signal

class DaemonBase(object):
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method."""
    
    __metaclass__ = abc.ABCMeta

    def __init__(self, pidfile, sleep=1.0, stdin=os.devnull,
                stdout=os.devnull, stderr=os.devnull):

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.sleep = sleep
    
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """

        # do first fork
        try: 
            pid = os.fork() 
        except OSError as e: 
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        else:
            if pid > 0: # exit from first parent
                sys.exit(0) 
    
        # decouple from parent environment
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 
    
        # do second fork
        try: 
            pid = os.fork() 
        except OSError as e: 
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1) 
        else:
            if pid > 0: # exit from second parent
                sys.exit(0) 
    
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        with io.open(self.stdin, 'rb') as si, io.open(self.stdout, 'a+b') as so, io.open(self.stderr, 'a+b', 0) as se:
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())
    
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with io.open(self.pidfile,'w+') as pf:
            pf.write("%s\n" % pid)
    
    def delpid(self):
        """
        Clean up function to run at exit.
        """
        try: os.remove(self.pidfile)
        except OSError: pass
        sys.stdout.flush()
        sys.stderr.flush()

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            with io.open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
    
        if pid is not None:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """

        sys.stdout.flush()
        sys.stderr.flush()
        # Get the pid from the pidfile
        try:
            with io.open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
    
        if pid is None:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process    
        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as e:
            if e.errno == errno.ESRCH: # Error number for "No such process"
                try: os.remove(self.pidfile)
                except OSError: pass
            else:
                sys.stderr.write(str(e.strerror))
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    @abc.abstractmethod
    def run(self):
        """
        You must override this method when you subclass Daemon. It will be called
        after the process has been daemonized by start() or restart().
        """
        while True:
            time.sleep(self.sleep)

