from flask import Blueprint

settings_bp = Blueprint('settings', __name__)

from app.blueprints.settings.routes import *
