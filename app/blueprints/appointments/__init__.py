from flask import Blueprint

appointments_bp = Blueprint('appointments', __name__)

from app.blueprints.appointments import routes
