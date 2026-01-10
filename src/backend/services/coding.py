import instructor
from groq import Groq
from src.backend.core.settings import settings
from src.backend.models import NoteStructure, BillableCode

class CodingService:
    def __init__(self, api_key: str = settings.GROQ_API_KEY , model: str = settings.CODING_MODEL):
        self.client = instructor.patch(
            Groq(api_key=api_key),
            mode=instructor.Mode.JSON
        )
    
        self.model = model

    def generate_codes(self, extracted_data: NoteStructure) -> BillableCode:
        """
        Accepts the structured data from the Vision service (NoteStructure)
        and uses Llama 3 70B to determine the correct billing codes.
        """
        
        system_prompt = """
        You are a Certified Professional Coder (CPC) specializing in Emergency Medicine.
        
        YOUR TASK:
        Assign the most specific ICD-10-CM diagnosis code based on the clinical notes provided.
        
        RULES:
        1. Always prefer SPECIFIC codes over UNSPECIFIED ones. 
           (Example: Use 'I21.3' for Anterior MI instead of just 'I21.9' if the location is known).
        2. If the text mentions 'STEMI', look for location (Inferior, Anterior, etc.) to refine the code.
        3. Provide clear reasoning for your choice.
        """

        # 👇 REMOVED THE INVALID FIELD AND COMBINED CONTEXT
        user_content = f"""
        Analyze this clinical data:
        - Chief Complaint: {extracted_data.chief_complaint}
        - Diagnosis/Impression: {extracted_data.diagnosis_text}
        - Procedures/Interventions (Check for meds here): {extracted_data.procedure_text}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_model=BillableCode,
            temperature=0.0
        )
        
        return response