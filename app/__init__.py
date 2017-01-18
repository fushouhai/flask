from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask.ext.pagedown import PageDown

from celery import Celery
from flask import current_app, render_template
from flask_mail import Message, Mail



pagedown = PageDown()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

                 
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'



celery = Celery('__name__', broker='redis://localhost', backend='redis://localhost')
celery.conf.update(
    result_expires = 3600
#    task_serializer = 'pickle', 
#    accept_content = ['pickle']
    )
    
    
@celery.task(bind=True)
def send_email(self, to, subject, template, **kwargs):
    
#    app = current_app._get_current_object()
    
    msg = Message('FLASKY' + ' ' + subject,
                  sender='1821938264@qq.com', recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    
    mail.send(msg)
#    with app.app_context():
#        mail.send(msg)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    
    #if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    if not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
