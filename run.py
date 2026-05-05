import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from app.extensions import db, jwt, migrate

app = Flask(__name__, template_folder='app/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

db.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

from app.blueprints.auth.routes import auth_bp
from app.blueprints.dashboard.routes import dashboard_bp
from app.blueprints.appointments.routes import appointments_bp
from app.blueprints.clients.routes import clients_bp
from app.blueprints.booking.routes import booking_bp
from app.blueprints.services.routes import services_bp

app.register_blueprint(services_bp, url_prefix='/services')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(appointments_bp, url_prefix='/appointments')
app.register_blueprint(clients_bp, url_prefix='/clients')
app.register_blueprint(booking_bp, url_prefix='/b')

if __name__ == '__main__':
    app.run(debug=True)