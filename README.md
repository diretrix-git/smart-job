# Smart Job Recommendation System

A full-stack web application that matches users to jobs using **NLP skill extraction** and **cosine similarity**. Users upload their resume as a PDF, the system extracts skills using spaCy, and recommends jobs ranked by how closely the user's skills match each job's requirements.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, Vite, TailwindCSS, Axios, React Router |
| Backend | Python, FastAPI, Uvicorn |
| Database | PostgreSQL, SQLAlchemy ORM, Alembic |
| NLP / AI | spaCy (PhraseMatcher), scikit-learn (cosine similarity), PyMuPDF |
| Auth | JWT (python-jose) + bcrypt |
| Testing | pytest, httpx, FastAPI TestClient |

## Project Structure

```
smart-job/
├── backend/
│   ├── app/
│   │   ├── api/            # API route handlers (auth, resumes, recommendations)
│   │   ├── core/           # Config and security (JWT, bcrypt)
│   │   ├── crud/           # Database CRUD operations
│   │   ├── db/             # SQLAlchemy engine and session
│   │   ├── models/         # ORM models (User, Job, Skill, Course, Resume, Recommendation)
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   └── services/       # NLP extractor, PDF parser, recommendation engine
│   ├── data/               # Seed data (jobs.json, courses.json, skills.json, seed.py)
│   ├── tests/              # Unit and integration tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── context/        # AuthContext (JWT state management)
│   │   ├── pages/          # Dashboard, Login, Register, Profile
│   │   └── services/       # Axios API client
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## Prerequisites

Make sure you have the following installed before starting:

- **Python 3.10+** → [Download](https://www.python.org/downloads/)
- **Node.js 18+** and **npm** → [Download](https://nodejs.org/)
- **PostgreSQL 14+** → [Download](https://www.postgresql.org/download/)
- **Git** → [Download](https://git-scm.com/)

---

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/diretrix-git/smart-job.git
cd smart-job
```

---

### Step 2: Set Up PostgreSQL Database

1. Open your PostgreSQL shell (psql) or pgAdmin.

2. Create a new database:

```sql
CREATE DATABASE smart_job_db;
```

3. Note down your PostgreSQL credentials (username, password, host, port). The default is usually:
   - Host: `localhost`
   - Port: `5432`
   - Username: `postgres`
   - Password: *(whatever you set during PostgreSQL installation)*

---

### Step 3: Backend Setup

#### 3.1 — Navigate to the backend folder

```bash
cd backend
```

#### 3.2 — Create a Python virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> You should see `(venv)` at the start of your terminal prompt. This means the virtual environment is active.

#### 3.3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 3.4 — Download the spaCy English language model

```bash
python -m spacy download en_core_web_sm
```

#### 3.5 — Create the `.env` file

Create a file named `.env` inside the `backend/` folder with the following contents:

```env
SECRET_KEY=your-secret-key-here-change-this
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/smart_job_db
```

> **Important:** Replace `yourpassword` with your actual PostgreSQL password. Replace `your-secret-key-here-change-this` with any random string (used for JWT token signing).

#### 3.6 — Seed the database with sample data

This creates all the tables and loads jobs, skills, and courses from the JSON files:

```bash
python data/seed.py
```

You should see:
```
Dropping and recreating tables...
Seeding skills...
Seeding jobs...
Seeding courses...
Seeding complete.
```

#### 3.7 — Start the backend server

```bash
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

> ✅ The backend is now running at **http://localhost:8000**
>
> 📄 Auto-generated API docs are available at **http://localhost:8000/docs**

---

### Step 4: Frontend Setup

Open a **new terminal window** (keep the backend running in the first one).

#### 4.1 — Navigate to the frontend folder

```bash
cd frontend
```

*(If you're in the project root, run `cd frontend`. If you're in the `backend/` folder, run `cd ../frontend`.)*

#### 4.2 — Install Node.js dependencies

```bash
npm install
```

#### 4.3 — Start the frontend development server

```bash
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

> ✅ The frontend is now running at **http://localhost:5173**

---

## Running the Full Application

To run the complete application, you need **both servers running simultaneously** in separate terminals:

| Terminal | Command | URL |
|----------|---------|-----|
| Terminal 1 (Backend) | `cd backend && uvicorn app.main:app --reload --port 8000` | http://localhost:8000 |
| Terminal 2 (Frontend) | `cd frontend && npm run dev` | http://localhost:5173 |

### Usage Flow

1. Open **http://localhost:5173** in your browser.
2. **Register** a new account.
3. **Log in** with your credentials.
4. **Upload your resume** (PDF format) on the Dashboard.
5. The system will extract your skills using NLP and display **job recommendations** ranked by match score.

---

## Running Tests

From the `backend/` directory (with the virtual environment activated):

```bash
pytest tests/ -v
```

This runs all 16 unit tests:
- `test_recommender.py` — Cosine similarity, vector building, missing skills, job matching
- `test_nlp.py` — PhraseMatcher construction, case-insensitive matching, deduplication
- `test_api_integration.py` — Full API endpoint integration test

---

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Secret key for JWT token signing | `my-super-secret-key-123` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/smart_job_db` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | *(Optional)* Token expiry in minutes. Default: `1440` (24 hours) | `1440` |

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register a new user | No |
| POST | `/api/v1/auth/login` | Login and get JWT token | No |
| GET | `/api/v1/auth/me` | Get current user profile | Yes |
| PUT | `/api/v1/auth/me` | Update current user profile | Yes |
| POST | `/api/v1/resumes/upload` | Upload resume PDF for skill extraction | Yes |
| GET | `/api/v1/resumes/skills` | Get current user's extracted skills | Yes |
| GET | `/api/v1/recommendations/jobs` | Get job recommendations with match scores | Yes |

---

## Team

| Member | Role |
|--------|------|
| **Krish** | Lead Developer — Backend Architecture, NLP Pipeline, Recommendation Engine |
| **Shishir** | Co-Lead Developer — Authentication, Database, Testing, Data Seeding |
| **Prajjwal** | Frontend Developer — React Pages, Routing, TailwindCSS Styling |
| **Sahil** | Frontend Developer — API Integration, AuthContext, State Management |

---

## License

MIT License
