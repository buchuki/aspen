import time
import threading

import cheroot.wsgi
from aspen.engines import ThreadedEngine


class Engine(ThreadedEngine):

    cheroot_server = None

    def bind(self):
        name = "Aspen! Cheroot!"
        self.cheroot_server = cheroot.wsgi.WSGIServer( self.website.address
                                                     , server_name=name
                                                     , wsgi_app=self.website
                                                      )

    def start(self):
        self.cheroot_server.start()

    def stop(self):
        self.cheroot_server.stop()

    def start_restarter(self, check_all):

        def loop():
            while True:
                try:
                    check_all()
                except SystemExit:
                    self.cheroot_server.interrupt = SystemExit
                time.sleep(0.5)

        checker = threading.Thread(target=loop)
        checker.daemon = True
        checker.start()
