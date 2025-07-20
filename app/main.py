import os
from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates
from app import crud, models, schemas, database
from sqlalchemy.orm import Session
import bcrypt
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "supersecurefallbackkey123"))

templates = Jinja2Templates(directory="app/templates")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Admin login page
@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

# Admin login POST
@app.post("/admin/login")
async def admin_login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin = crud.get_admin_by_email(db, email=email)
    if not admin or not bcrypt.checkpw(password.encode(), admin.hashed_password.encode()):
        return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid credentials"})
    request.session["admin_email"] = admin.email
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_302_FOUND)

# Admin dashboard
@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    if "admin_email" not in request.session:
        return RedirectResponse(url="/admin/login")
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "admin_email": request.session["admin_email"]})

# Logout route
@app.get("/admin/logout")
async def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/admin/login")

# Example: send notification email when user registers
def send_registration_notification(user_email: str):
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    msg = EmailMessage()
    msg["Subject"] = "New User Registration"
    msg["From"] = smtp_user
    msg["To"] = smtp_user  # Admin receives notification
    msg.set_content(f"New user registered with email: {user_email}")

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

# User registration example
@app.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    crud.create_user(db, email=email, hashed_password=hashed_pw)
    send_registration_notification(email)
    return {"message": "Registration successful"}

# Root route (example)
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})