from compendium.embeddings import get_documents
from compendium.embeddings import load_embeddings
from compendium.predict import suggest_medication
from compendium.split_from_all import get_medications
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

medications = get_medications()
documents = get_documents(medications)
vectorstore = load_embeddings(medications)

def mock_suggest_medication(symptoms):
    return f"Mocked suggestion for symptoms: {symptoms}"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/suggest", response_class=HTMLResponse)
async def suggest(request: Request, symptoms: str = Form(...)):
    result = suggest_medication(
        symptoms,
        vectorstore,
        documents)
    return templates.TemplateResponse("index.html", {"request": request, "result": result})
