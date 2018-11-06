from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
import os
import logging

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
login.login_view = 'login'

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.api import bp as api_bp
app.register_blueprint(api_bp)

if not app.debug:
	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/serialshow.log', maxBytes=10240,
		backupCount=10)
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)

	app.logger.setLevel(logging.INFO)
	app.logger.info('Serialshow startup')

from app import routes, models, errors