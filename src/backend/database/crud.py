from sqlalchemy.orm import Session
from src.backend.database.tables import MedicalNote  
from src.backend.models import NoteStructure, BillableCode

def create_medical_note(
    db: Session, 
    extracted_data: NoteStructure, 
    coding_result: BillableCode, 
    filename: str = "unknown"
):
    """
    Takes the Pydantic models (extracted_data, coding_result) 
    and saves them into the PostgreSQL 'medical_notes' table.
    """
    
    # Map Pydantic fields to SQLAlchemy Columns
    db_note = MedicalNote(
        filename=filename,
        
        # Vision Data
        patient_id=extracted_data.patient_id,
        date_of_service=extracted_data.date_of_service,
        chief_complaint=extracted_data.chief_complaint,
        diagnosis_text=extracted_data.diagnosis_text,
        procedure_text=extracted_data.procedure_text,
        
        # Coding Data
        icd10_code=coding_result.icd10_code,
        icd10_description=coding_result.icd10_description,
        reasoning=coding_result.reasoning,
        confidence_score=coding_result.confidence_score
    )
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note