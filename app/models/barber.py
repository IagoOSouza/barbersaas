from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Barber(db.Model):
    __tablename__ = 'barbers'

    id              = db.Column(db.Integer, primary_key=True)
    barbershop_id   = db.Column(db.Integer, db.ForeignKey('barbershops.id'), nullable=False)
    name            = db.Column(db.String(120), nullable=False)
    email           = db.Column(db.String(120), unique=True, nullable=False)
    password_hash   = db.Column(db.String(255), nullable=False)
    phone           = db.Column(db.String(20))
    is_owner        = db.Column(db.Boolean, default=False)  # dono da barbearia
    active          = db.Column(db.Boolean, default=True)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    appointments = db.relationship('Appointment', backref='barber', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_owner': self.is_owner,
        }
