from flask import Blueprint

clients_bp = Blueprint('clients', __name__)

from app.blueprints.clients import routes
