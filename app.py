#!/usr/bin/env python

import os
import sys
import gunicorn.app.base
from gunicorn.six import iteritems

import wsgi_proxy

def number_of_workers():
    import multiprocessing
    return (multiprocessing.cpu_count() * 2) + 1

class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':
    # Get the environment information we need to start the server
    ip = os.environ.get('OPENSHIFT_PYTHON_IP', '0.0.0.0')
    port = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
    host_name = os.environ.get('OPENSHIFT_GEAR_DNS', 'localhost')
    options = {
        'bind': '%s:%s' % (ip, port),
        'workers': number_of_workers(),
    }
    StandaloneApplication(wsgi_proxy.app, options).run()