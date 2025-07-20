from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    client_email = request.cookies.get("client_email")
    if not client_email:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Please log in to view dashboard."})

    client = db.query(Client).filter(Client.email == client_email).first()
    if not client:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Account not found."})

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "client": client,
    })