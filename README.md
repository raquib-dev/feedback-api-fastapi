# 📝 Feedback API – FastAPI + JWT + Docker

A secure, async backend service for submitting and moderating user feedback. Built with FastAPI, SQLAlchemy, and JWT authentication. Ready for production with Docker support.

---

## 🚀 Features

- 🧾 Users can register and log in (JWT-based)
- ✍️ Submit feedback tied to logged-in users
- ✅ Admin can approve/reject feedback
- 🔐 Role-based access control (user/admin)
- 📜 View only approved feedback publicly
- 🧠 Fully async using SQLAlchemy 2.0
- 🐳 Dockerized with environment configs
- 📁 Logs with automatic cleanup

---

## 🧪 API Overview

| Endpoint                       | Method | Access       | Description                     |
|-------------------------------|--------|--------------|---------------------------------|
| `/auth/register`              | POST   | Public       | Register a new user             |
| `/auth/login`                 | POST   | Public       | Login and receive JWT token     |
| `/feedback`                   | POST   | Auth (user)  | Submit feedback                 |
| `/feedback`                   | GET    | Public       | View approved feedback          |
| `/feedback/admin`             | GET    | Admin only   | View all feedback (moderation) |
| `/feedback/admin/{id}`        | PUT    | Admin only   | Approve/reject feedback         |

---

## 🔐 Authentication

All protected routes require:

```
Authorization: Bearer <your_token>
```

---

## 🐳 Dockerized Setup

### 1. Clone the Repo
```bash
git clone https://github.com/raquib-dev/feedback-api-fastapi.git
cd feedback-api-fastapi
```

### 2. Configure Environment
Edit `.env`:

```env
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Build & Run with Docker
```bash
docker compose up --build
```

The API will be live at: [http://localhost:8000](http://localhost:8000)

---

## 🧱 Tech Stack

- FastAPI
- SQLAlchemy (async)
- SQLite / PostgreSQL
- JWT (via python-jose)
- passlib (bcrypt)
- Docker & Compose

---

## 📁 Project Structure

```
app/
├── main.py            # App entrypoint
├── auth.py            # Auth + JWT logic
├── database.py        # DB setup
├── models.py          # ORM models
├── schemas.py         # Pydantic validation
├── routes/            # Route modules
│   ├── users.py       # Auth routes
│   └── feedback.py    # Feedback routes
├── logger.py          # Central logging
logs/
└── app.log            # Auto-created logs
```

---

## 📌 Future Enhancements

- Email verification
- Soft delete review
- Admin dashboard UI
- PostgreSQL + Alembic migrations

---

## 💼 Made with ❤️ by [raquib-dev](https://github.com/raquib-dev)