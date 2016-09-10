#!/usr/bin/env python
import wsgi_proxy

application = wsgi_proxy.app

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    import os

    port = int(os.environ.get('PORT', 8080))
    httpd = make_server('0.0.0.0', port, wsgi_proxy.app)
    httpd.serve_forever()
