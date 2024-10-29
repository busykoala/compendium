from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
import os

from compendium.embeddings import get_documents, load_embeddings
from compendium.predict import suggest_medication
from compendium.split_from_all import get_medications

app = FastAPI()
app.add_middleware(
    SessionMiddleware, secret_key="ZHx579kzsILbuvhi")

templates = Jinja2Templates(directory="templates")

USERNAME = "test"
PASSWORD = os.getenv("PASSWORD", "test")

medications = get_medications()
documents = get_documents(medications)
vectorstore = load_embeddings()

def get_current_user(request: Request):
    if not request.session.get("user"):
        return RedirectResponse(url="/login")
    return request.session["user"]

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == USERNAME and password == PASSWORD:
        request.session["user"] = username
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request, user=Depends(get_current_user)):
    if isinstance(user, RedirectResponse):
        return user
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/suggest", response_class=HTMLResponse)
async def suggest(request: Request, symptoms: str = Form(...), age: int = Form(...), sex: str = Form(...), user=Depends(get_current_user)):
    if isinstance(user, RedirectResponse):
        return user
    result = suggest_medication(
        symptoms,
        vectorstore,
        age=age,
        sex=sex,
    )
    return templates.TemplateResponse("index.html", {"request": request, "result": result})
