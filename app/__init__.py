# coding=utf-8
"""
    app
    ~~~

    整个Web服务器应用。

    __init__.py主要包含create_app(config_name)工厂方法，用于根据配置创建Flask应
    用对象。
"""

from flask import Flask
from flask_admin import Admin
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import utils as security_utils
from sqlalchemy.exc import SQLAlchemyError

from config import config

db = SQLAlchemy()
admin = Admin(name='Flask-backbone 后台', template_mode='bootstrap3')
babel = Babel()


def create_app(config_name: str) -> Flask:
    """
    创建Flask对象的工厂方法。
    :param config_name: 配置的名称
    :return: Flask对象
    """
    app = Flask(__name__)

    from app.utils import CustomJsonEncoder
    app.json_encoder = CustomJsonEncoder

    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.models.sqla_models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    try:
        with app.app_context():
            create_init_user(user_datastore)
    except SQLAlchemyError:
        print('>>> Failed to create initial user, if you are creating database,'
              ' ignore this.')

    admin.init_app(app)
    setup_admin()

    babel.init_app(app)

    from app.blueprints.api.controllers import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from app.blueprints.doc.controllers import doc as doc_blueprint
    app.register_blueprint(doc_blueprint, url_prefix='/doc')

    # TODO in doc:
    # 如果还有其他的blueprint，在这里注册

    return app


def create_init_user(user_datastore: SQLAlchemyUserDatastore) -> None:

    """
    TODO in doc:
    在这里创建初始的角色和管理用户。
    """
    user_datastore.find_or_create_role(name='root', description='系统管理员')
    user_datastore.find_or_create_role(name='admin', description='管理员')
    user_datastore.find_or_create_role(name='user', description='用户')

    if not user_datastore.get_user('tgmerge@163.com'):
        user_datastore.create_user(
            email='tgmerge@163.com',
            password=security_utils.encrypt_password('default_password')
        )

    # TODO in doc:
    # 如果还需要更多的初始用户，在这里创建

    db.session.commit()  # 在给用户分配角色前，必须commit这个User对象

    user_datastore.add_role_to_user('tgmerge@163.com', 'root')

    # TODO in doc:
    # 在这里分配其他角色给初始用户

    db.session.commit()


def setup_admin():

    from app.models.sqla_models import Article
    from app.models.admin_modelviews import ArticleView
    admin.add_view(ArticleView(Article, db.session, name='文章'))

    # TODO in doc:
    # 在这里配置其他的Flask-admin管理视图


@babel.localeselector
def get_locale():
    return 'zh_CN'
