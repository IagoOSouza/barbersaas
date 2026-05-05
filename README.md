# BarberSaaS

SaaS de gestão para barbearias locais. Agenda, clientes e lembretes automáticos via WhatsApp.

## Stack

- **Backend:** Flask + SQLAlchemy
- **Banco:** PostgreSQL (Supabase)
- **Auth:** JWT via cookies
- **Frontend:** Jinja2 + Tailwind CSS + HTMX
- **WhatsApp:** Z-API / Evolution API
- **Deploy:** Railway / Render

---

## Setup local

### 1. Clone e crie o ambiente virtual

```bash
git clone <repo>
cd barbersaas
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

### 3. Configure o banco de dados

```bash
flask db init
flask db migrate -m "initial"
flask db upgrade
```

### 4. Rode o projeto

```bash
python run.py
```

Acesse: http://localhost:5000

---

## Estrutura

```
app/
├── models/          # Barbershop, Barber, Client, Appointment, Service
├── blueprints/      # auth, dashboard, appointments, clients, booking
├── services/        # whatsapp.py, scheduler.py
└── templates/       # HTML Jinja2
```

---

## URLs principais

| URL | Descrição |
|-----|-----------|
| `/auth/register` | Cadastro de nova barbearia |
| `/auth/login` | Login do barbeiro |
| `/dashboard` | Painel principal |
| `/appointments` | Agenda |
| `/clients` | Gestão de clientes |
| `/b/<slug>` | Página pública de agendamento |

---

## Deploy no Railway

1. Suba para o GitHub
2. Conecte o repo no Railway
3. Adicione as variáveis do `.env` no painel do Railway
4. Railway detecta o `Procfile` e faz o deploy automaticamente
# barbersaas
# barbersaas
# barbersaas
