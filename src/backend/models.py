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