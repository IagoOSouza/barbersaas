from flask import render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.blueprints.clients import clients_bp
from app.extensions import db
from app.models.barber import Barber
from app.models.client import Client
from datetime import datetime


def get_current_barber():
    return Barber.query.get(int(get_jwt_identity()))


@clients_bp.route('/')
@jwt_required()
def index():
    barber = get_current_barber()
    search = request.args.get('q', '')

    query = Client.query.filter_by(barbershop_id=barber.barbershop_id)
    if search:
        query = query.filter(Client.name.ilike(f'%{search}%'))

    clients = query.order_by(Client.name).all()
    return render_template('clients/index.html', barber=barber, clients=clients, search=search, current_barber=barber)


@clients_bp.route('/new', methods=['GET', 'POST'])
@jwt_required()
def new():
    barber = get_current_barber()

    if request.method == 'POST':
        data = request.form
        birthday = None
        if data.get('birthday'):
            birthday = datetime.strptime(data['birthday'], '%Y-%m-%d').date()

        client = Client(
            barbershop_id=barber.barbershop_id,
            name=data['name'],
            phone=data['phone'],
            email=data.get('email', ''),
            birthday=birthday,
            notes=data.get('notes', ''),
        )
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('clients.index'))

    return render_template('clients/new.html', barber=barber, current_barber=barber)


@clients_bp.route('/<int:id>')
@jwt_required()
def detail(id):
    barber = get_current_barber()
    client = Client.query.filter_by(
        id=id,
        barbershop_id=barber.barbershop_id
    ).first_or_404()

    appointments = client.appointments
    return render_template('clients/detail.html',
        barber=barber,
        client=client,
        appointments=appointments,
        current_barber=barber,
    )
