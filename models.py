from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Kriteria(Base):
    __tablename__ = "kriteria"

    id = Column(Integer, primary_key=True, index=True)
    nama_kriteria = Column(String, nullable=False)
    jenis = Column(String, nullable=False)
    bobot = Column(Numeric, nullable=False)

class Alternatif(Base):
    __tablename__ = "alternatif"

    id = Column(Integer, primary_key=True, index=True)
    nama_alternatif = Column(String, nullable=False)

class NilaiKriteria(Base):
    __tablename__ = "nilai_kriteria"

    id = Column(Integer, primary_key=True, index=True)
    alternatif_id = Column(Integer, ForeignKey("alternatif.id", ondelete="CASCADE"))
    kriteria_id = Column(Integer, ForeignKey("kriteria.id", ondelete="CASCADE"))
    nilai = Column(Numeric, nullable=False)
