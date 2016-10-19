# coding=utf-8

from app import create_app
from werkzeug.contrib.fixers import ProxyFix

application = create_app('deploy')
application.wsgi_app = ProxyFix(application.wsgi_app)

if __name__ == '__main__':
    application.run()
