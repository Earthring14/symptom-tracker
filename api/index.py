from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from app.logic import transcribe_audio, extract_fields, save_record

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"record": None},
        request=request
    )


@app.post("/", response_class=HTMLResponse)
async def process_form(
    request: Request,
    session_number: str = Form(...),
    patient_name: str = Form(...),
    audiofile: UploadFile = File(...)
):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{audiofile.filename}"
    with open(file_path, "wb") as f:
        f.write(await audiofile.read())

    transcript = transcribe_audio(file_path)
    extracted = extract_fields(transcript)
    record = save_record(extracted, patient_name, session_number)

    return templates.TemplateResponse(
        name="index.html",
        context={"record": record},
        request=request
    )
