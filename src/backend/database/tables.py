from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from src.backend.database.database import Base 
from src.backend.core.settings import settings

class MedicalNote(Base):
    __tablename__ = settings.TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    
    # Metadata
    filename = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Extracted Data (From Vision)
    patient_id = Column(String, nullable=True)
    date_of_service = Column(String, nullable=True)
    chief_complaint = Column(Text, nullable=True)
    diagnosis_text = Column(Text, nullable=True)
    procedure_text = Column(Text, nullable=True)
    
    # Coding Results (From Logic)
    icd10_code = Column(String, nullable=True)
    icd10_description = Column(String, nullable=True)
    reasoning = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)

    