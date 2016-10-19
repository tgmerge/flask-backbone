# coding=utf-8
"""
    gunicorn-config.py
    ~~~~~~~~~~~~~~~~~~

    Gunicorn部署配置文件。使用

        gunicorn -c gunicorn-config.py wsgi:application

    来运行Web服务器
"""

import multiprocessing

bind = 'localhost:5000'
workers = multiprocessing.cpu_count() * 2 + 1

# 使用gevent工作
worker_class = 'gevent'

# 在后台运行
daemon = True

errorlog = 'log/error.log'
capture_output = True
