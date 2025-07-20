from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import hashlib

app = FastAPI()

# Secret key for session (change to your own long random string)
app.add_middleware(SessionMiddleware, secret_key="your_super_secret_key_here")

templates = Jinja2Templates(directory="app/frontend")

# Admin credentials (email + hashed password)
ADMIN_EMAIL = "optiontrade24.online@gmail.com"
ADMIN_PASSWORD_HASH = hashlib.sha256("Lincoln818762".encode()).hexdigest()

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if email == ADMIN_EMAIL and password_hash == ADMIN_PASSWORD_HASH:
        request.session["admin_logged_in"] = True
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    if not request.session.get("admin_logged_in"):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")
