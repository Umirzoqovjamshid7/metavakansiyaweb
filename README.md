# Vakansiya ariza formasi — PostgreSQL

Python 3.10+ va PostgreSQL kerak.

## 1. PostgreSQL bazasini tayyorlash

PostgreSQL superuser orqali (pgAdmin Query Tool yoki psql) quyidagilarni **alohida** bajaring:

```sql
CREATE USER vakansiya_user WITH PASSWORD 'BU_YERGA_KUCHLI_PAROL';
CREATE DATABASE vakansiya_db OWNER vakansiya_user;
```

Parolni o'zingiz tanlang, GitHubga joylamang. Jadval ilova ishga tushganda avtomatik yaratiladi.

## 2. VS Code PowerShell

```powershell
cd vakansiya_form
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL='postgresql://vakansiya_user:BU_YERGA_KUCHLI_PAROL@localhost:5432/vakansiya_db'
$env:ADMIN_TOKEN='OzingizTanlaganUzunMaxfiyToken'
uvicorn main:app --reload
```

Agar parolda @, :, /, # yoki % belgisi bo'lsa, URL ichida percent-encode qiling.

Forma: http://127.0.0.1:8000
Admin: http://127.0.0.1:8000/admin

## 3. Tekshirish

```sql
SELECT id, created_at, data FROM applications ORDER BY id DESC;
```

**Muhim:** `.env.example` faqat namuna. Ilova `DATABASE_URL` va `ADMIN_TOKEN` ni muhit o'zgaruvchilaridan oladi. Serverga chiqarishdan oldin HTTPS, rate limit, haqiqiy admin autentifikatsiyasi, ma'lumotlarni saqlash siyosati, rozilik va backup qo'shing. Admin token brauzerda vaqtincha qo'lda kiritiladi. Bu demo MVP.

Dropdown variantlari skrinshotda ko'rinmagani sababli hozircha vaqtincha Ha/Yo'q. Bitrix24 integratsiyasi mavjud emas.
