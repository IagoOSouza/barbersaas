from app.extensions import db
from datetime import datetime


class Client(db.Model):
    __tablename__ = 'clients'

    id              = db.Column(db.Integer, primary_key=True)
    barbershop_id   = db.Column(db.Integer, db.ForeignKey('barbershops.id'), nullable=False)
    name            = db.Column(db.String(120), nullable=False)
    phone           = db.Column(db.String(20), nullable=False)
    email           = db.Column(db.String(120))
    birthday        = db.Column(db.Date)
    notes           = db.Column(db.Text)  # preferências, observações
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    appointments = db.relationship('Appointment', backref='client', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'notes': self.notes,
        }
