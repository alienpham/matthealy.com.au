import os
from flask import Flask
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask_wtf.csrf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_flatpages import FlatPages
from flask_frozen import Freezer

from werkzeug.contrib.fixers import ProxyFix

from config import config

from htmlabbrev import HTMLAbbrev

mail = Mail()
moment = Moment()
toolbar = DebugToolbarExtension()

csrf = CsrfProtect()

pages = FlatPages()
freezer = Freezer()

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)

    csrf.init_app(app)
    pages.init_app(app)
    freezer.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')

    app.wsgi_app = ProxyFix(app.wsgi_app)

    @app.template_filter()
    def htmlabbrev(value, maxlen=150):
        parser = HTMLAbbrev(maxlen)
        parser.feed(value)
        return parser.close()

    app.jinja_env.filters['htmlabbrev'] = htmlabbrev

    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler, SMTPHandler

        file_handler = RotatingFileHandler('tmp/healy.log', 'a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('healy startup')

        credentials = None
        secure = None

        if app.config['MAIL_USERNAME'] is not None:
            credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            if app.config['MAIL_USE_TLS'] is True:
                secure = ()

        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['HEALY_MAIL_SENDER'],
            toaddrs=app.config['HEALY_ADMIN_EMAIL'],
            subject=app.config['HEALY_MAIL_SUBJECT_PREFIX'] + ' Application Error',
            credentials=credentials)

        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    return app
