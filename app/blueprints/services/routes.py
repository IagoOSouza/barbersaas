from app.blueprints.services import services_bp
from flask import render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.barber import Barber
from app.models.appointment import Service


def get_current_barber():
    return Barber.query.get(int(get_jwt_identity()))


@services_bp.route('/')
@jwt_required()
def index():
    barber = get_current_barber()
    services = Service.query.filter_by(
        barbershop_id=barber.barbershop_id
    ).order_by(Service.name).all()
    return render_template('services/index.html', barber=barber, services=services, current_barber=barber)


@services_bp.route('/new', methods=['GET', 'POST'])
@jwt_required()
def new():
    barber = get_current_barber()

    if request.method == 'POST':
        data = request.form
        service = Service(
            barbershop_id=barber.barbershop_id,
            name=data['name'],
            duration_min=int(data['duration_min']),
            price=float(data['price']),
        )
        db.session.add(service)
        db.session.commit()
        return redirect(url_for('services.index'))

    return render_template('services/new.html', barber=barber, current_barber=barber)


@services_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required()
def edit(id):
    barber = get_current_barber()
    service = Service.query.filter_by(
        id=id,
        barbershop_id=barber.barbershop_id
    ).first_or_404()

    if request.method == 'POST':
        data = request.form
        service.name = data['name']
        service.duration_min = int(data['duration_min'])
        service.price = float(data['price'])
        db.session.commit()
        return redirect(url_for('services.index'))

    return render_template('services/edit.html', barber=barber, service=service, current_barber=barber)


@services_bp.route('/<int:id>/toggle', methods=['POST'])
@jwt_required()
def toggle(id):
    """Ativa ou desativa um serviço."""
    barber = get_current_barber()
    service = Service.query.filter_by(
        id=id,
        barbershop_id=barber.barbershop_id
    ).first_or_404()

    service.active = not service.active
    db.session.commit()
    return redirect(url_for('services.index'))


@services_bp.route('/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete(id):
    barber = get_current_barber()
    service = Service.query.filter_by(
        id=id,
        barbershop_id=barber.barbershop_id
    ).first_or_404()

    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('services.index'))
