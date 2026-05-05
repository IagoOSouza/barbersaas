from flask import render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.blueprints.dashboard import dashboard_bp
from app.models.barber import Barber
from app.models.appointment import Appointment
from datetime import datetime, date


def get_current_barber():
    barber_id = get_jwt_identity()
    return Barber.query.get(int(barber_id))


@dashboard_bp.route('/')
@jwt_required()
def index():
    barber = get_current_barber()
    if not barber:
        return redirect(url_for('auth.login'))

    today = date.today()

    # Agendamentos de hoje
    today_appointments = Appointment.query.filter(
        Appointment.barbershop_id == barber.barbershop_id,
        Appointment.barber_id == barber.id,
        db.func.date(Appointment.scheduled_at) == today,
        Appointment.status == 'confirmed'
    ).order_by(Appointment.scheduled_at).all()

    # Total de clientes
    from app.models.client import Client
    total_clients = Client.query.filter_by(
        barbershop_id=barber.barbershop_id
    ).count()

    return render_template('dashboard/index.html',
        barber=barber,
        today_appointments=today_appointments,
        total_clients=total_clients,
        today=today,
        current_barber=barber,
    )


# Importa db para usar nas queries acima
from app.extensions import db
