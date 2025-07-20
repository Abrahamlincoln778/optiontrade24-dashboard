from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
import bcrypt
import os

from app import models, database, schemas, crud

app = FastAPI()

# Middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "fallbacksecret"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
ADMIN_EMAIL = "optiontrade24.online@gmail.com"

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h2>OptionTrade24 API is running</h2>"

@app.get("/reset-admin", response_class=HTMLResponse)
async def reset_admin_form(request: Request):
    return HTMLResponse("""
      <form method="post">
        <label>New Password:</label><br/>
        <input name="password" type="password" required/><br/><br/>
        <button>Reset Admin Password</button>
      </form>
    """)

@app.post("/reset-admin")
async def reset_admin(request: Request, password: str = Form(...), db: Session = Depends(database.get_db)):
    admin = db.query(models.User).filter(models.User.email == ADMIN_EMAIL).first()
    if not admin:
        return {"error": "Admin account not found"}
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    admin.hashed_password = hashed.decode("utf-8")
    db.commit()
    return RedirectResponse(url="/login", status_code=302)

# Include other routers (auth, dashboard, support)
from app.routers import auth, dashboard, support

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(support.router)
