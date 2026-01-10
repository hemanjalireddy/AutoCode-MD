import base64
import os
import instructor
from groq import Groq
from loguru import logger
from src.backend.core.settings import settings
from src.backend.models import NoteStructure

class VisionService:
    def __init__(self, api_key: str = settings.GROQ_API_KEY, model: str = settings.VISION_MODEL):
        self.client = instructor.patch(
            Groq(api_key=api_key),
            mode=instructor.Mode.JSON
        )
        self.model = model

    def _encode_image(self, image_bytes: bytes) -> str:
        return base64.b64encode(image_bytes).decode('utf-8')
    def analyze_medical_note(self, image_bytes: bytes) -> NoteStructure:
        """
        Sends image to Llama 3.2 Vision and extracts structured JSON.
        """
        logger.info(f"Vision Service: Analyzing image using {self.model}...")
        
        base64_image = self._encode_image(image_bytes)
        
        system_prompt = """
        You are an expert EMS (Emergency Medical Services) Data Digitizer.
        Your job is to extract structured data from handwritten Ambulance Run Sheets.

        RULES:
        1. EXTRACT 'Field Impression', 'Provider Impression', or 'Assessment' as the diagnosis_text.
           - If it says "Impression: STEMI", extract "STEMI".
        2. EXTRACT 'Interventions', 'Rx', or 'Treatments' as the procedure_text.
           - Look for terms like: IV, O2, Splint, Bandaging, Meds given.
        3. If the handwriting is messy, use context to infer the correct word.
        4. Return null if a specific field is completely missing.
        """

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": system_prompt},
                            {
                                "type": "image_url", 
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            },
                        ],
                    }
                ],
                model=self.model,
                temperature=0.0,
                response_model=NoteStructure 
            )
            
            logger.success("Vision extraction successful")
            return response 

        except Exception as e:
            logger.exception(f"Vision Service Error: {e}")
            raise e