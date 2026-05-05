from app.extensions import db
from datetime import datetime


class Service(db.Model):
    __tablename__ = 'services'

    id              = db.Column(db.Integer, primary_key=True)
    barbershop_id   = db.Column(db.Integer, db.ForeignKey('barbershops.id'), nullable=False)
    name            = db.Column(db.String(100), nullable=False)  # ex: Corte, Barba, Combo
    duration_min    = db.Column(db.Integer, default=30)          # duração em minutos
    price           = db.Column(db.Numeric(10, 2))
    active          = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration_min': self.duration_min,
            'price': float(self.price) if self.price else None,
        }


class Appointment(db.Model):
    __tablename__ = 'appointments'

    STATUS_CONFIRMED  = 'confirmed'
    STATUS_CANCELLED  = 'cancelled'
    STATUS_COMPLETED  = 'completed'
    STATUS_NO_SHOW    = 'no_show'

    id              = db.Column(db.Integer, primary_key=True)
    barbershop_id   = db.Column(db.Integer, db.ForeignKey('barbershops.id'), nullable=False)
    barber_id       = db.Column(db.Integer, db.ForeignKey('barbers.id'), nullable=False)
    client_id       = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    service_id      = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    scheduled_at    = db.Column(db.DateTime, nullable=False)
    status          = db.Column(db.String(20), default='confirmed')
    reminder_sent   = db.Column(db.Boolean, default=False)  # lembrete 24h enviado?
    notes           = db.Column(db.Text)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    service = db.relationship('Service', backref='appointments', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client.name,
            'client_phone': self.client.phone,
            'service_name': self.service.name,
            'scheduled_at': self.scheduled_at.isoformat(),
            'status': self.status,
        }
