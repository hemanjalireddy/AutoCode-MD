from pydantic import BaseModel, Field
from typing import Optional


class NoteStructure(BaseModel):
    patient_id: Optional[str] = Field(
        None, description="The Patient ID, Run Number, or Incident Number found on the form."
    )
    date_of_service: Optional[str] = Field(
        None, description="The date of the ambulance run or emergency call."
    )
    chief_complaint: Optional[str] = Field(
        None, description="The 'CC', 'Nature of Call', or primary reason for dispatch (e.g., 'Chest Pain', 'MVC')."
    )
    diagnosis_text: Optional[str] = Field(
        None, description="The 'Field Impression', 'Provider Impression', or 'Assessment' section (e.g., 'STEMI', 'Open Fracture', 'Hypoglycemia')."
    )
    procedure_text: Optional[str] = Field(
        None, description="List of interventions or treatments performed by EMS (e.g., 'IV started', 'Splint applied', 'CPR', 'Intubation')."
    )

class BillableCode(BaseModel):
    """
    Represents the final medical code assigned to the patient note.
    """
    icd10_code: str = Field(
        ..., 
        description="The most specific ICD-10-CM diagnosis code (e.g., 'I21.9', 'S82.401')."
    )
    icd10_description: str = Field(
        ..., 
        description="The official description of the code from the ICD-10 standard."
    )
    cpt_code: Optional[str] = Field(
        None, 
        description="The CPT procedural code if applicable (e.g., '99285' for emergency visit)."
    )
    reasoning: str = Field(
        ..., 
        description="A short explanation of why this code was selected based on the clinical evidence."
    )
    confidence_score: float = Field(
        ..., 
        description="A confidence score between 0.0 and 1.0 indicating how certain the model is."
    )