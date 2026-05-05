from app.extensions import db
from datetime import datetime
import re


class Barbershop(db.Model):
    __tablename__ = 'barbershops'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    slug       = db.Column(db.String(80), unique=True, nullable=False)  # ex: barbearia-do-joao
    phone      = db.Column(db.String(20))
    address    = db.Column(db.String(255))
    plan       = db.Column(db.String(20), default='basic')  # basic, pro, premium
    active     = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    barbers      = db.relationship('Barber', backref='barbershop', lazy=True)
    clients      = db.relationship('Client', backref='barbershop', lazy=True)
    services     = db.relationship('Service', backref='barbershop', lazy=True)
    appointments = db.relationship('Appointment', backref='barbershop', lazy=True)

    @staticmethod
    def generate_slug(name):
        slug = name.lower().strip()
        slug = re.sub(r'[àáâãä]', 'a', slug)
        slug = re.sub(r'[èéêë]', 'e', slug)
        slug = re.sub(r'[ìíîï]', 'i', slug)
        slug = re.sub(r'[òóôõö]', 'o', slug)
        slug = re.sub(r'[ùúûü]', 'u', slug)
        slug = re.sub(r'[ç]', 'c', slug)
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s]+', '-', slug)
        return slug

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'phone': self.phone,
            'plan': self.plan,
        }
