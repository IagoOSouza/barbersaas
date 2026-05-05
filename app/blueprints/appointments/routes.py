from flask import render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.blueprints.appointments import appointments_bp
from app.extensions import db
from app.models.barber import Barber
from app.models.appointment import Appointment, Service
from app.models.client import Client
from datetime import datetime, date


def get_current_barber():
    return Barber.query.get(int(get_jwt_identity()))


@appointments_bp.route('/')
@jwt_required()
def index():
    barber = get_current_barber()
    date_str = request.args.get('date', date.today().isoformat())
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    appointments = Appointment.query.filter(
        Appointment.barbershop_id == barber.barbershop_id,
        Appointment.barber_id == barber.id,
        db.func.date(Appointment.scheduled_at) == selected_date
    ).order_by(Appointment.scheduled_at).all()

    return render_template('appointments/index.html',
        barber=barber,
        appointments=appointments,
        selected_date=selected_date,
        current_barber=barber,
    )


@appointments_bp.route('/new', methods=['GET', 'POST'])
@jwt_required()
def new():
    barber = get_current_barber()

    if request.method == 'POST':
        data = request.form
        appointment = Appointment(
            barbershop_id=barber.barbershop_id,
            barber_id=barber.id,
            client_id=int(data['client_id']),
            service_id=int(data['service_id']),
            scheduled_at=datetime.strptime(data['scheduled_at'], '%Y-%m-%dT%H:%M'),
            notes=data.get('notes', ''),
            current_barber=barber,
        )
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('appointments.index'))

    clients = Client.query.filter_by(barbershop_id=barber.barbershop_id).all()
    services = Service.query.filter_by(barbershop_id=barber.barbershop_id, active=True).all()

    return render_template('appointments/new.html',
        barber=barber,
        clients=clients,
        services=services,
    )


@appointments_bp.route('/<int:id>/cancel', methods=['POST'])
@jwt_required()
def cancel(id):
    barber = get_current_barber()
    appointment = Appointment.query.filter_by(
        id=id,
        barbershop_id=barber.barbershop_id  # segurança: só cancela da própria barbearia
    ).first_or_404()

    appointment.status = 'cancelled'
    db.session.commit()
    return redirect(url_for('appointments.index'))
