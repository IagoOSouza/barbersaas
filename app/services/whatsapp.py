import requests
from flask import current_app


def _send_message(phone: str, message: str) -> bool:
    """Envia mensagem via Z-API ou Evolution API."""
    api_url = current_app.config.get('WHATSAPP_API_URL')
    token = current_app.config.get('WHATSAPP_TOKEN')

    if not api_url or not token:
        current_app.logger.warning('WhatsApp API não configurada.')
        return False

    # Formata o número: remove tudo que não for dígito
    phone_clean = ''.join(filter(str.isdigit, phone))
    if not phone_clean.startswith('55'):
        phone_clean = '55' + phone_clean

    try:
        response = requests.post(
            api_url,
            json={'phone': phone_clean, 'message': message},
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        current_app.logger.error(f'Erro ao enviar WhatsApp: {e}')
        return False


def send_confirmation(phone: str, appointment) -> bool:
    """Envia confirmação de agendamento para o cliente."""
    scheduled = appointment.scheduled_at.strftime('%d/%m/%Y às %H:%M')
    message = (
        f'✅ *Agendamento confirmado!*\n\n'
        f'Olá, {appointment.client.name}!\n'
        f'Seu horário foi confirmado:\n\n'
        f'📅 {scheduled}\n'
        f'✂️ {appointment.service.name}\n'
        f'💈 {appointment.barber.name}\n\n'
        f'Até lá!'
    )
    return _send_message(phone, message)


def send_reminder(phone: str, appointment) -> bool:
    """Envia lembrete 24h antes para o cliente."""
    scheduled = appointment.scheduled_at.strftime('%d/%m/%Y às %H:%M')
    message = (
        f'⏰ *Lembrete de agendamento*\n\n'
        f'Olá, {appointment.client.name}!\n'
        f'Lembrando do seu horário *amanhã*:\n\n'
        f'📅 {scheduled}\n'
        f'✂️ {appointment.service.name}\n'
        f'💈 {appointment.barber.name}\n\n'
        f'Até amanhã!'
    )
    return _send_message(phone, message)
