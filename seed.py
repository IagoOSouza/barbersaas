"""
Script de seed — popula o banco com dados de teste.

Como usar:
    python seed.py

Isso cria:
- 1 barbearia (Barbearia do João)
- 1 barbeiro dono (login: joao@barberia.com / senha: 123456)
- 4 serviços (Corte, Barba, Combo, Sobrancelha)
- 5 clientes de exemplo
- 3 agendamentos (hoje, amanhã, depois de amanhã)
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.extensions import db
from app.models.barbershop import Barbershop
from app.models.barber import Barber
from app.models.client import Client
from app.models.appointment import Appointment, Service
from datetime import datetime, date, timedelta

app = create_app('development')

with app.app_context():
    print("🗑️  Limpando banco...")
    db.drop_all()
    db.create_all()

    # ─── Barbearia ───────────────────────────────────────────
    print("💈 Criando barbearia...")
    shop = Barbershop(
        name="Barbearia do João",
        slug="barbearia-do-joao",
        phone="31999990000",
        address="Rua das Tesouras, 42 — BH/MG",
        plan="pro",
    )
    db.session.add(shop)
    db.session.flush()

    # ─── Barbeiro dono ────────────────────────────────────────
    print("👤 Criando barbeiro...")
    joao = Barber(
        barbershop_id=shop.id,
        name="João Silva",
        email="joao@barberia.com",
        phone="31999990001",
        is_owner=True,
    )
    joao.set_password("123456")
    db.session.add(joao)
    db.session.flush()

    # ─── Serviços ─────────────────────────────────────────────
    print("✂️  Criando serviços...")
    services_data = [
        {"name": "Corte",              "duration_min": 30, "price": 35.00},
        {"name": "Barba",              "duration_min": 20, "price": 25.00},
        {"name": "Combo Corte + Barba","duration_min": 50, "price": 55.00},
        {"name": "Sobrancelha",        "duration_min": 15, "price": 15.00},
    ]
    services = []
    for s in services_data:
        service = Service(barbershop_id=shop.id, **s)
        db.session.add(service)
        services.append(service)
    db.session.flush()

    # ─── Clientes ─────────────────────────────────────────────
    print("👥 Criando clientes...")
    clients_data = [
        {"name": "Carlos Mendes",   "phone": "31988880001", "email": "carlos@email.com",  "notes": "Prefere tesoura"},
        {"name": "Rafael Souza",    "phone": "31988880002", "email": "rafael@email.com",  "notes": "Cabelo enrolado"},
        {"name": "Lucas Oliveira",  "phone": "31988880003", "email": "",                  "notes": ""},
        {"name": "Pedro Alves",     "phone": "31988880004", "email": "pedro@email.com",   "notes": "Sempre às terças"},
        {"name": "Bruno Costa",     "phone": "31988880005", "email": "",                  "notes": "Alérgico a certos produtos"},
    ]
    clients = []
    for c in clients_data:
        client = Client(barbershop_id=shop.id, **c)
        db.session.add(client)
        clients.append(client)
    db.session.flush()

    # ─── Agendamentos ─────────────────────────────────────────
    print("📅 Criando agendamentos...")
    today = date.today()

    appointments_data = [
        # Hoje
        {"client": clients[0], "service": services[0], "delta_days": 0,  "hour": 9,  "minute": 0},
        {"client": clients[1], "service": services[2], "delta_days": 0,  "hour": 10, "minute": 0},
        {"client": clients[2], "service": services[1], "delta_days": 0,  "hour": 11, "minute": 0},
        # Amanhã
        {"client": clients[3], "service": services[0], "delta_days": 1,  "hour": 14, "minute": 0},
        {"client": clients[4], "service": services[3], "delta_days": 1,  "hour": 15, "minute": 30},
        # Depois de amanhã
        {"client": clients[0], "service": services[2], "delta_days": 2,  "hour": 9,  "minute": 30},
    ]

    for a in appointments_data:
        scheduled = datetime(
            today.year, today.month, today.day,
            a["hour"], a["minute"]
        ) + timedelta(days=a["delta_days"])

        apt = Appointment(
            barbershop_id=shop.id,
            barber_id=joao.id,
            client_id=a["client"].id,
            service_id=a["service"].id,
            scheduled_at=scheduled,
            status="confirmed",
        )
        db.session.add(apt)

    db.session.commit()

    # ─── Resumo ───────────────────────────────────────────────
    print("\n✅ Seed concluído!")
    print("─" * 40)
    print(f"  Barbearia : {shop.name}")
    print(f"  Slug      : /b/{shop.slug}")
    print(f"  Login     : joao@barberia.com")
    print(f"  Senha     : 123456")
    print(f"  Serviços  : {len(services)}")
    print(f"  Clientes  : {len(clients)}")
    print(f"  Agendamentos: {len(appointments_data)}")
    print("─" * 40)
    print("\nAcesse: http://localhost:5000/auth/login")
    print("Página pública: http://localhost:5000/b/barbearia-do-joao\n")
