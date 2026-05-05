from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import (
    create_access_token, set_access_cookies,
    unset_jwt_cookies, jwt_required, get_jwt_identity
)
from app.extensions import db
from app.models.barber import Barber
from app.models.barbershop import Barbershop

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    data = request.form
    barber = Barber.query.filter_by(email=data.get('email')).first()

    if not barber or not barber.check_password(data.get('password', '')):
        return render_template('auth/login.html', error='Email ou senha incorretos.')

    token = create_access_token(identity=str(barber.id))
    response = redirect(url_for('dashboard.index'))
    set_access_cookies(response, token)
    return response


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')

    data = request.form

    # Verifica se email já existe
    if Barber.query.filter_by(email=data.get('email')).first():
        return render_template('auth/register.html', error='Email já cadastrado.')

    # Cria a barbearia
    shop_name = data.get('barbershop_name', '').strip()
    slug = Barbershop.generate_slug(shop_name)

    # Garante slug único
    base_slug = slug
    counter = 1
    while Barbershop.query.filter_by(slug=slug).first():
        slug = f'{base_slug}-{counter}'
        counter += 1

    barbershop = Barbershop(name=shop_name, slug=slug)
    db.session.add(barbershop)
    db.session.flush()  # gera o ID sem commitar

    # Cria o barbeiro dono
    barber = Barber(
        barbershop_id=barbershop.id,
        name=data.get('name'),
        email=data.get('email'),
        is_owner=True
    )
    barber.set_password(data.get('password'))
    db.session.add(barber)
    db.session.commit()

    token = create_access_token(identity=str(barber.id))
    response = redirect(url_for('dashboard.index'))
    set_access_cookies(response, token)
    return response


@auth_bp.route('/logout')
def logout():
    response = redirect(url_for('auth.login'))
    unset_jwt_cookies(response)
    return response
