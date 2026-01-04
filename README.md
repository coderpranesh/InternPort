# Internship Application Portal

A full-stack web application where **students apply for internships** and **companies manage applications**.

## Tech Stack
- Backend: Flask, SQLAlchemy, Flask-Security  
- Frontend: Vue.js, Axios  
- Database: SQLite  
- Optional: Celery + Redis  

## Features
- User registration & token-based login
- Role-based access (Student, Company)
- Companies post and manage internships
- Students apply and track application status
- Secure REST APIs

## Roles
- **Student**: View internships, apply, track status  
- **Company**: Create internships, view applicants, update status  

## API Endpoints
**Auth**
- `POST /register`
- `POST /login`

**Company**
- `POST /api/internships`
- `PUT /api/internships/<id>`
- `GET /api/applications/<internship_id>`
- `PUT /api/application/<id>/status`

**Student**
- `GET /api/internships`
- `POST /api/apply/<internship_id>`
- `GET /api/my-applications`

## Run Locally
```bash
# Backend
pip install -r requirements.txt
python app.py

# Frontend
npm install
npm run dev
