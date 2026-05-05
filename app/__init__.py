from flask import Flask
from app.config import config
from app.extensions import db, jwt, migrate


def create_app(env='default'):
    app = Flask(__name__)
    app.config.from_object(config[env])

    # Inicializa extensões
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Registra blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.appointments import appointments_bp
    from app.blueprints.clients import clients_bp
    from app.blueprints.booking import booking_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(booking_bp, url_prefix='/b')

    # Rota raiz
    #from flask import redirect, url_for
    #return redirect(url_for('dashboard.index'))

    return app
