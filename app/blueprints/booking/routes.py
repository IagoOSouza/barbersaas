from flask import render_template, request, redirect, jsonify
from app.blueprints.booking import booking_bp
from app.extensions import db
from app.models.barbershop import Barbershop
from app.models.barber import Barber
from app.models.client import Client
from app.models.appointment import Appointment, Service
from app.services.whatsapp import send_confirmation
from datetime import datetime, timedelta


@booking_bp.route('/<slug>')
def index(slug):
    barbershop = Barbershop.query.filter_by(slug=slug, active=True).first_or_404()
    services = Service.query.filter_by(barbershop_id=barbershop.id, active=True).all()
    barbers = Barber.query.filter_by(barbershop_id=barbershop.id, active=True).all()
    return render_template('booking/index.html',
        barbershop=barbershop,
        services=services,
        barbers=barbers,
    )


@booking_bp.route('/<slug>/slots')
def slots(slug):
    """
    Retorna os horários ocupados de um barbeiro numa data.
    Chamado via fetch() pelo JavaScript da página pública.

    Query params:
        barber_id: int
        date: YYYY-MM-DD
    """
    barbershop = Barbershop.query.filter_by(slug=slug, active=True).first_or_404()

    barber_id = request.args.get('barber_id', type=int)
    date_str  = request.args.get('date', '')

    if not barber_id or not date_str:
        return jsonify({'busy': []})

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'busy': []})

    # Busca agendamentos confirmados nesse dia para esse barbeiro
    appointments = Appointment.query.filter(
        Appointment.barbershop_id == barbershop.id,
        Appointment.barber_id    == barber_id,
        Appointment.status       == 'confirmed',
        db.func.date(Appointment.scheduled_at) == selected_date
    ).all()

    # Retorna lista de horários ocupados no formato HH:MM
    busy = []
    for apt in appointments:
        service = apt.service
        duration = service.duration_min if service else 30
        # Bloqueia o horário de início + todos os slots dentro da duração do serviço
        slot = apt.scheduled_at
        while slot < apt.scheduled_at + timedelta(minutes=duration):
            busy.append(slot.strftime('%H:%M'))
            slot += timedelta(minutes=30)

    return jsonify({'busy': busy})


@booking_bp.route('/<slug>/confirm', methods=['POST'])
def confirm(slug):
    barbershop = Barbershop.query.filter_by(slug=slug, active=True).first_or_404()
    data = request.form

    # Verifica se o horário ainda está disponível antes de confirmar
    scheduled_at = datetime.strptime(data['scheduled_at'], '%Y-%m-%dT%H:%M')
    conflict = Appointment.query.filter_by(
        barbershop_id=barbershop.id,
        barber_id=int(data['barber_id']),
        scheduled_at=scheduled_at,
        status='confirmed'
    ).first()

    if conflict:
        barbers  = Barber.query.filter_by(barbershop_id=barbershop.id, active=True).all()
        services = Service.query.filter_by(barbershop_id=barbershop.id, active=True).all()
        return render_template('booking/index.html',
            barbershop=barbershop,
            services=services,
            barbers=barbers,
            error='Este horário acabou de ser ocupado. Por favor, escolha outro.'
        )

    # Busca ou cria o cliente pelo telefone
    client = Client.query.filter_by(
        barbershop_id=barbershop.id,
        phone=data['phone']
    ).first()

    if not client:
        client = Client(
            barbershop_id=barbershop.id,
            name=data['name'],
            phone=data['phone'],
        )
        db.session.add(client)
        db.session.flush()

    appointment = Appointment(
        barbershop_id=barbershop.id,
        barber_id=int(data['barber_id']),
        client_id=client.id,
        service_id=int(data['service_id']),
        scheduled_at=scheduled_at,
    )
    db.session.add(appointment)
    db.session.commit()

    send_confirmation(client.phone, appointment)

    return render_template('booking/success.html',
        barbershop=barbershop,
        appointment=appointment,
        client=client,
    )
