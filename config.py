# coding=utf-8
"""
    config.py
    ~~~~~~~~~

    包含用于创建Flask对象的配置。使用config字典和配置名称来获取配置。
"""

import os

# 这个文件的所在目录，即项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    一些默认配置
    """

    # 文档目录
    DOC_DIR = os.path.join(basedir, 'document', '_build', 'html')

    # TODO in doc
    # (flask-sqlalchemy)
    # 在这里修改数据库连接方式
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@127.0.0.1:5432/database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO in doc
    # (flask)
    # 必须在这里设置一个secret key，用于session
    SECRET_KEY = 'Some string hard to guess'

    # TODO in doc
    # (flask-security)
    # 必须在这里设置一个password salt，用于密码加盐
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'some salt hard to guess'

    # TODO in doc
    # 在这里设置客户端用于API请求签名的key: secret对
    CLIENT_KEYS = {
        'xY6RNbg48KlFmnbq': 'yskMv2XZ8xNwIEeT',  # e.g. iOS client
        'V7B8rXBpuKTBJN0Z': 'VUrSJ4wc8gxDdSPx'   # e.g. Android client
    }

    # API蓝图的最大请求内容长度(1MB)
    API_MAX_CONTENT_LENGTH = 1 * 1024 * 1024

    # TODO in doc
    # 如果需要整合又拍云，在这里设置默认账号信息
    UPYUN_BUCKET = 'my-bucket'
    UPYUN_USERNAME = 'someone'
    UPYUN_PASSWORD = 'somewhere'


class DevelopmentConfig(Config):
    """
    开发环境配置
    """

    DEBUG = True

    # TODO in doc
    # 在这里设置一个可以跳过API请求签名验证的签名，用于调试
    MASTER_REQUEST_SIGNATURE = 'DOGE2181173204e04efb9f18751edc0bca02'

    # (flask-sqlalchemy)
    # 输出SQLAlchemy执行的SQL语句
    SQLALCHEMY_ECHO = False


class DeployConfig(Config):
    """
    生产环境配置
    """

    DEBUG = False
    SQLALCHEMY_ECHO = False


config = {
    'development': DevelopmentConfig,
    'deploy': DeployConfig
}
