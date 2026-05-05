from app.blueprints.settings import settings_bp
from flask import render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app.extensions import db
from app.models.barber import Barber
from app.models.barbershop import Barbershop


def get_current_barber():
    return Barber.query.get(int(get_jwt_identity()))


@settings_bp.route('/')
@jwt_required()
def index():
    barber = get_current_barber()
    return render_template('settings/index.html', barber=barber, current_barber=barber)


@settings_bp.route('/barbershop', methods=['POST'])
@jwt_required()
def update_barbershop():
    """Atualiza os dados da barbearia."""
    barber = get_current_barber()
    shop = barber.barbershop
    data = request.form

    shop.name    = data.get('name', shop.name).strip()
    shop.phone   = data.get('phone', shop.phone).strip()
    shop.address = data.get('address', shop.address).strip()

    db.session.commit()
    flash('Dados da barbearia atualizados!', 'success')
    return redirect(url_for('settings.index'))


@settings_bp.route('/hours', methods=['POST'])
@jwt_required()
def update_hours():
    """Salva o horário de funcionamento no campo notes da barbearia por enquanto."""
    barber = get_current_barber()
    shop = barber.barbershop
    data = request.form

    # Salva como JSON string no campo address por enquanto
    # Quando tiver uma tabela própria, migra para lá
    import json
    hours = {
        'monday':    {'open': data.get('mon_open'),    'close': data.get('mon_close'),    'active': 'mon_active'    in data},
        'tuesday':   {'open': data.get('tue_open'),    'close': data.get('tue_close'),    'active': 'tue_active'    in data},
        'wednesday': {'open': data.get('wed_open'),    'close': data.get('wed_close'),    'active': 'wed_active'    in data},
        'thursday':  {'open': data.get('thu_open'),    'close': data.get('thu_close'),    'active': 'thu_active'    in data},
        'friday':    {'open': data.get('fri_open'),    'close': data.get('fri_close'),    'active': 'fri_active'    in data},
        'saturday':  {'open': data.get('sat_open'),    'close': data.get('sat_close'),    'active': 'sat_active'    in data},
        'sunday':    {'open': data.get('sun_open'),    'close': data.get('sun_close'),    'active': 'sun_active'    in data},
    }

    # Guarda no campo notes da barbershop como JSON
    if not hasattr(shop, 'working_hours'):
        shop.address = shop.address  # força dirty
    shop.working_hours_json = json.dumps(hours)

    # Adiciona coluna se não existir ainda
    try:
        db.session.execute(
            db.text("ALTER TABLE barbershops ADD COLUMN working_hours_json TEXT")
        )
        db.session.commit()
    except Exception:
        db.session.rollback()

    # Atualiza via SQL direto para evitar problema de model desatualizado
    db.session.execute(
        db.text("UPDATE barbershops SET working_hours_json = :h WHERE id = :id"),
        {'h': json.dumps(hours), 'id': shop.id}
    )
    db.session.commit()

    flash('Horários de funcionamento atualizados!', 'success')
    return redirect(url_for('settings.index'))


@settings_bp.route('/password', methods=['POST'])
@jwt_required()
def update_password():
    """Atualiza a senha do barbeiro logado."""
    barber = get_current_barber()
    data = request.form

    if not barber.check_password(data.get('current_password', '')):
        flash('Senha atual incorreta.', 'error')
        return redirect(url_for('settings.index'))

    new_password = data.get('new_password', '')
    if len(new_password) < 6:
        flash('A nova senha precisa ter pelo menos 6 caracteres.', 'error')
        return redirect(url_for('settings.index'))

    if new_password != data.get('confirm_password', ''):
        flash('As senhas não coincidem.', 'error')
        return redirect(url_for('settings.index'))

    barber.set_password(new_password)
    db.session.commit()
    flash('Senha atualizada com sucesso!', 'success')
    return redirect(url_for('settings.index'))
