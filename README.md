# Job Tracker API

A production-ready REST API for tracking job applications, built with FastAPI, PostgreSQL, and JWT authentication.

**Live API:** https://job-tracker-api-735d.onrender.com/docs  
**Frontend:** https://job-tracker-ui-sand.vercel.app

---

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL, SQLAlchemy ORM, Alembic migrations
- **Auth:** JWT (python-jose), bcrypt password hashing
- **Testing:** pytest — 8 tests passing
- **Containerization:** Docker, Docker Compose
- **Deployment:** Render

---

## Features

- JWT Authentication (register, login, protected routes)
- Full CRUD for job applications
- Jobs filtered per user — users only see their own jobs
- Status tracking (Applied → OA → Interview → Offer → Rejected)
- Alembic database migrations
- 8 automated tests with pytest
- Fully containerized with Docker Compose

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /auth/register | Create account | No |
| POST | /auth/login | Get JWT token | No |
| GET | /users/me | Get current user | Yes |
| GET | /jobs | Get all my jobs | Yes |
| POST | /jobs | Create a job | Yes |
| PUT | /jobs/{id} | Update a job | Yes |
| DELETE | /jobs/{id} | Delete a job | Yes |

---

## Running Locally

```bash
git clone https://github.com/anaghakalyanaraman/job-tracker-api
cd job-tracker-api
docker compose up --build
```

API docs at `http://localhost:8000/docs`

---

## Running Tests

```bash
pip install -r requirements.txt
pytest -v
```
