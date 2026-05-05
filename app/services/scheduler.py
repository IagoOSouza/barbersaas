from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import logging

scheduler = BackgroundScheduler()
logger = logging.getLogger(__name__)


def send_reminders_job(app):
    """Verifica agendamentos em ~24h e envia lembretes."""
    with app.app_context():
        from app.extensions import db
        from app.models.appointment import Appointment
        from app.services.whatsapp import send_reminder

        now = datetime.now()
        window_start = now + timedelta(hours=23)
        window_end = now + timedelta(hours=25)

        appointments = Appointment.query.filter(
            Appointment.scheduled_at.between(window_start, window_end),
            Appointment.reminder_sent == False,
            Appointment.status == 'confirmed'
        ).all()

        for apt in appointments:
            success = send_reminder(apt.client.phone, apt)
            if success:
                apt.reminder_sent = True
                logger.info(f'Lembrete enviado: agendamento {apt.id}')

        db.session.commit()


def start_scheduler(app):
    """Inicia o scheduler com o job de lembretes."""
    scheduler.add_job(
        send_reminders_job,
        'interval',
        hours=1,
        args=[app],
        id='send_reminders',
        replace_existing=True,
    )
    scheduler.start()
    logger.info('Scheduler iniciado.')
