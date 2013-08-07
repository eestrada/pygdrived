#!/usr/bin/env python
from __future__ import division, with_statement, print_function, unicode_literals

import sys, time
from datetime import datetime
from gdrive.daemon import DaemonBase

class MyDaemon(DaemonBase):
    def run(self):
        while True:
            time.sleep(self.sleep)
            sys.stdout.write("Running my daemon at: ")
            sys.stdout.write(datetime.now().isoformat())
            sys.stdout.write("\n")
            sys.stdout.flush()

def usage(prog):
    print("usage: %s status|start|stop|restart" % prog)
    
if __name__ == "__main__":
    d = MyDaemon('/tmp/daemon-example.pid', sleep=10.0, stdout='/tmp/daemon_tests.log')
    md = {'status': d.stop, 'start': d.start, 'stop': d.stop, 'restart': d.restart}

    if len(sys.argv) == 2:
        try:
            md[sys.argv[1]]()
        except KeyError as e:
            print("Unknown command: " + sys.argv[1])
            usage(sys.argv[0])
            sys.exit(2)
        else:
            sys.exit(0)
    else:
        usage(sys.argv[0])
        sys.exit(2)
        
