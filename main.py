import os, secrets
from pathlib import Path
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

ROOT = Path(__file__).parent
app = FastAPI(title='Vakansiya arizalari')

class Application(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    phone: str
    extra_phone: str
    birth_date: str
    address: str
    tashkent: str
    telegram: str
    full_time: str
    workplaces: str
    education: str
    languages: str
    genres: str
    achievements: str
    programs: str
    books: str
    skills: str
    additional: str

def connect():
    url = os.getenv('DATABASE_URL')
    if not url:
        raise RuntimeError('DATABASE_URL muhit o‘zgaruvchisi sozlanmagan')
    return psycopg.connect(url, row_factory=dict_row)

@app.on_event('startup')
def create_table():
    with connect() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS applications (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            data JSONB NOT NULL
        )''')

@app.get('/')
def home():
    return FileResponse(ROOT / 'index.html')

@app.post('/api/applications', status_code=201)
def submit(application: Application):
    data = application.model_dump()
    if any(not str(value).strip() for value in data.values()):
        raise HTTPException(422, 'Barcha maydonlarni to‘ldiring')
    if not all(data[key].startswith('+998') and len(''.join(filter(str.isdigit, data[key]))) == 12 for key in ('phone', 'extra_phone')):
        raise HTTPException(422, 'Telefon raqam +998 bilan 12 ta raqamdan iborat bo‘lishi kerak')
    with connect() as db:
        row = db.execute('INSERT INTO applications (data) VALUES (%s) RETURNING id', (Jsonb(data),)).fetchone()
    return {'message': 'Arizangiz qabul qilindi', 'id': row['id']}

@app.get('/admin')
def admin_page():
    return FileResponse(ROOT / 'admin.html')

@app.get('/api/applications')
def applications(x_admin_token: str | None = Header(default=None)):
    token = os.getenv('ADMIN_TOKEN')
    if not token or not x_admin_token or not secrets.compare_digest(token, x_admin_token):
        raise HTTPException(401, 'Admin token noto‘g‘ri')
    with connect() as db:
        rows = db.execute('SELECT id, created_at, data FROM applications ORDER BY id DESC').fetchall()
    return [{'id': row['id'], 'created_at': row['created_at'].isoformat(), **row['data']} for row in rows]
