import os
from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from app import crud, models, schemas, database
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import bcrypt

load_dotenv()

app = FastAPI()

# Add session middleware with secret key from env
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "fallbacksecret"))

# Set up templates folder
templates = Jinja2Templates(directory="app/frontend/templates")

# Mount static files if you have any
app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root route serves index.html
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Admin login page GET
@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

# Admin login POST
@app.post("/admin/login")
async def admin_login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Replace below with your real admin email and hashed password check
    admin_email = os.getenv("ADMIN_EMAIL", "optiontrade24.online@gmail.com")
    admin_password_hash = os.getenv("ADMIN_PASSWORD_HASH")  # store hashed password in env
    
    if email != admin_email:
        return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid email"})
    
    if not admin_password_hash:
        return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Admin password not set"})
    
    if not bcrypt.checkpw(password.encode(), admin_password_hash.encode()):
        return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid password"})
    
    # On success, create session
    request.session["admin"] = True
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_302_FOUND)

# Admin dashboard (protected)
@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

# Admin logout
@app.get("/admin/logout")
async def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

# Add more routes below (email support, client dashboard, etc.) as needed