from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import (
    get_kriteria, add_kriteria, delete_kriteria,
    get_alternatif, add_alternatif, delete_alternatif,
    get_nilai_kriteria
)
from models import Base

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency: Session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root: Dashboard
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# CRUD Kriteria
@app.get("/kriteria/", response_class=HTMLResponse)
def read_kriteria(request: Request, db: Session = Depends(get_db)):
    kriteria_list = get_kriteria(db)
    return templates.TemplateResponse("kriteria.html", {"request": request, "kriteria_list": kriteria_list})

@app.post("/kriteria/add")
def create_kriteria(nama_kriteria: str = Form(...), jenis: str = Form(...), bobot: float = Form(...), db: Session = Depends(get_db)):
    add_kriteria(db, nama_kriteria, jenis, bobot)
    return {"message": "Kriteria berhasil ditambahkan"}

@app.get("/kriteria/delete/{kriteria_id}")
def delete_kriteria_endpoint(kriteria_id: int, db: Session = Depends(get_db)):
    delete_kriteria(db, kriteria_id)
    return {"message": "Kriteria berhasil dihapus"}

# CRUD Alternatif
@app.get("/alternatif/", response_class=HTMLResponse)
def read_alternatif(request: Request, db: Session = Depends(get_db)):
    alternatif_list = get_alternatif(db)
    return templates.TemplateResponse("alternatif.html", {"request": request, "alternatif_list": alternatif_list})

@app.post("/alternatif/add")
def create_alternatif(nama_alternatif: str = Form(...), db: Session = Depends(get_db)):
    add_alternatif(db, nama_alternatif)
    return {"message": "Alternatif berhasil ditambahkan"}

@app.get("/alternatif/delete/{alternatif_id}")
def delete_alternatif_endpoint(alternatif_id: int, db: Session = Depends(get_db)):
    delete_alternatif(db, alternatif_id)
    return {"message": "Alternatif berhasil dihapus"}

# Matriks Keputusan
@app.get("/matriks/", response_class=HTMLResponse)
def matriks_keputusan(request: Request, db: Session = Depends(get_db)):
    kriteria_list = get_kriteria(db)
    alternatif_list = get_alternatif(db)
    nilai_kriteria = get_nilai_kriteria(db)

    # Proses matriks
    matriks = []
    for alternatif in alternatif_list:
        row = {"nama_alternatif": alternatif.nama_alternatif, "nilai_kriteria": []}
        for kriteria in kriteria_list:
            nilai = next((nk.nilai for nk in nilai_kriteria if nk.alternatif_id == alternatif.id and nk.kriteria_id == kriteria.id), 0)
            row["nilai_kriteria"].append(nilai)
        matriks.append(row)

    # Normalisasi Matriks dan Ranking
    normalisasi = []
    for kriteria in kriteria_list:
        nilai_kolom = [row["nilai_kriteria"][kriteria.id - 1] for row in matriks]
        if kriteria.jenis.lower() == "benefit":
            divisor = max(nilai_kolom)
        else:  # Cost
            divisor = min(nilai_kolom)

        for i, row in enumerate(matriks):
            if len(normalisasi) <= i:
                normalisasi.append({"nama_alternatif": row["nama_alternatif"], "nilai": []})
            normalisasi[i]["nilai"].append(row["nilai_kriteria"][kriteria.id - 1] / divisor if divisor != 0 else 0)

    # Hitung Preferensi dan Ranking
    preferensi = []
    for row in normalisasi:
        total = sum(
            norm * kriteria_list[i].bobot if kriteria_list[i].jenis.lower() == "benefit" else -norm * kriteria_list[i].bobot
            for i, norm in enumerate(row["nilai"])
        )
        preferensi.append({"nama_alternatif": row["nama_alternatif"], "preferensi": total})

    preferensi.sort(key=lambda x: x["preferensi"], reverse=True)
    for rank, pref in enumerate(preferensi, start=1):
        pref["ranking"] = rank

    return templates.TemplateResponse(
        "matriks.html",
        {"request": request, "kriteria_list": kriteria_list, "matriks": matriks, "ranking": preferensi}
    )
