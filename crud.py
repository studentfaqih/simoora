from sqlalchemy.orm import Session
from models import Kriteria, Alternatif, NilaiKriteria

# Kriteria
def get_kriteria(db: Session):
    return db.query(Kriteria).all()

def add_kriteria(db: Session, nama_kriteria: str, jenis: str, bobot: float):
    new_kriteria = Kriteria(nama_kriteria=nama_kriteria, jenis=jenis, bobot=bobot)
    db.add(new_kriteria)
    db.commit()
    db.refresh(new_kriteria)
    return new_kriteria

def delete_kriteria(db: Session, kriteria_id: int):
    kriteria = db.query(Kriteria).filter(Kriteria.id == kriteria_id).first()
    if kriteria:
        db.delete(kriteria)
        db.commit()
        return True
    return False

# Alternatif
def get_alternatif(db: Session):
    return db.query(Alternatif).all()

def add_alternatif(db: Session, nama_alternatif: str):
    new_alternatif = Alternatif(nama_alternatif=nama_alternatif)
    db.add(new_alternatif)
    db.commit()
    db.refresh(new_alternatif)
    return new_alternatif

def delete_alternatif(db: Session, alternatif_id: int):
    alternatif = db.query(Alternatif).filter(Alternatif.id == alternatif_id).first()
    if alternatif:
        db.delete(alternatif)
        db.commit()
        return True
    return False

# Nilai Kriteria
def get_nilai_kriteria(db: Session):
    return db.query(NilaiKriteria).all()

def add_nilai_kriteria(db: Session, alternatif_id: int, kriteria_id: int, nilai: float):
    new_nilai = NilaiKriteria(alternatif_id=alternatif_id, kriteria_id=kriteria_id, nilai=nilai)
    db.add(new_nilai)
    db.commit()
    db.refresh(new_nilai)
    return new_nilai

def delete_nilai_kriteria(db: Session, nilai_id: int):
    nilai = db.query(NilaiKriteria).filter(NilaiKriteria.id == nilai_id).first()
    if nilai:
        db.delete(nilai)
        db.commit()
        return True
    return False
