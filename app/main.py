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

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "verysecretkey123"))

templates = Jinja2Templates(directory="app/frontend/templates")
app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
async def admin_login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin_email = "optiontrade24.online@gmail.com"
    
    # Hashed version of: Lincoln818762
    admin_password_hash = "$2b$12$XYBQAKSmO1nLPAVwnBrTeO4qDoIGALC56jaNMK57Wf4USZ0qZ3D5i"

    if email != admin_email:
        return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid email"})
    
    if not bcrypt.checkpw(password.encode(), admin_password_hash.encode()):
        return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid password"})
    
    request.session["admin"] = True
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_302_FOUND)

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

@app.get("/admin/logout")
async def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)