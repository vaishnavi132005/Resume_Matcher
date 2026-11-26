import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parser import read_resume, estimate_years
from skills import extract_skills
from matcher import rank_jobs

app = FastAPI(title="Resume Job Matching API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MAX_BYTES = 5 * 1024 * 1024


@app.get("/")
def home():
    return {"message": "Resume Job Matching API is running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in (".pdf", ".docx"):
        raise HTTPException(400, "Please upload a PDF or DOCX resume.")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(400, "File is too large (max 5 MB).")
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(data)
        path = tmp.name
    try:
        text = read_resume(path, ext)
    except Exception:
        raise HTTPException(400, "Could not read this file. Is it a valid resume?")
    finally:
        os.remove(path)
    if len(text) < 50:
        raise HTTPException(400, "No readable text found. Scanned resumes are not supported yet.")
    skills = extract_skills(text)
    years = estimate_years(text)
    return {
        "profile": {"skills": skills, "years": years, "characters": len(text)},
        "jobs": rank_jobs(text, skills, years),
    }

from fastapi.staticfiles import StaticFiles
app.mount("/app", StaticFiles(directory="static", html=True), name="static")
