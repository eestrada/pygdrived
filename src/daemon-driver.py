#!/usr/bin/env python
from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import sys, time
from datetime import datetime
from gdrive.daemon import DaemonBase

try:
    import threading
except ImportError:
    import dummy_threading as threading

def _dummy_func():
    while True:
        time.sleep(5)

class SimpleDaemon(DaemonBase):
    def __init__(self, *args, **kwargs):
        self.thread_target = kwargs.pop('thread_target', _dummy_func)
        self.thread_args = kwargs.pop('thread_ags', tuple())
        self.thread_kwargs = kwargs.pop('thread_kwargs', dict())
        self.lock = kwargs.pop('pref_lock', None)

        self.gui_thread = threading.Thread(target=self.thread_target,
            args=self.thread_args, kwargs=self.thread_kwargs)

        super(SimpleDaemon, self).__init__(*args, **kwargs)

    def daemonize(self):
        super(SimpleDaemon, self).daemonize()
        self.gui_thread.start()

    def run(self):
        while True:
            if not self.gui_thread.is_active():
                sys.exit(0)
            if self.target is not None:
                args = self.args
                kwargs = self.kwargs
                self.target(*args, **kwargs)
            time.sleep(self.sleep)

_d = SimpleDaemon('/tmp/daemon-example.pid', sleep=10.0, stdout='/tmp/daemon_tests.log')

_METHOD_DICT = {'status': _d.stop, 'start': _d.start, 'stop': _d.stop,
    'restart': _d.restart}

def usage(prog):
    print("usage: %s status|start|stop|restart" % prog)
    
if __name__ == "__main__":

    if len(sys.argv) == 2:
        try:
            _METHOD_DICT[sys.argv[1]]()
        except KeyError as e:
            print("Unknown command: " + sys.argv[1])
            usage(sys.argv[0])
            sys.exit(2)
        else:
            sys.exit(0)
    else:
        usage(sys.argv[0])
        sys.exit(2)
        
