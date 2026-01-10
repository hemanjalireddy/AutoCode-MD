import instructor
from groq import Groq
from loguru import logger
from src.backend.core.settings import settings
from src.backend.database.vector_store import VectorDBManager
from src.backend.models import NoteStructure, BillableCode

class CodingService:
    def __init__(self, api_key: str = settings.GROQ_API_KEY, model: str = settings.CODING_MODEL):
        self.client = instructor.patch(
            Groq(api_key=api_key),
            mode=instructor.Mode.JSON
        )
        self.model = model
        
        # Connect to the Vector Knowledge Base (Memory)
        self.knowledge_base = VectorDBManager()

    def _retrieve_guidelines(self, query_text: str) -> str:
        """
        Helper: Searches the Vector DB for relevant ICD-10 guidelines.
        """
        logger.info(f"RAG Retrieval: Searching guidelines for '{query_text}'...")
        
        # 1. Search Vector DB
        results = self.knowledge_base.search(query_text, k=3)
        
        if not results:
            return "No specific guidelines found."

        # 2. Format results for the Prompt
        context_block = "\n".join(
            [f"--- RULE (Source: Page {doc.metadata.get('page', '?')}) ---\n{doc.page_content}" 
             for doc in results]
        )
        return context_block

    def generate_codes(self, extracted_data: NoteStructure) -> BillableCode:
        """
        Accepts structured data (Vision), retrieves guidelines (RAG), 
        and uses Llama 3 to determine billing codes.
        """
        
        # --- STEP 1: RETRIEVAL (The "Look Up") ---
        # Construct a search query based on the diagnosis
        search_query = f"ICD-10 coding guidelines for {extracted_data.diagnosis_text}"
        if extracted_data.procedure_text:
            search_query += f" and {extracted_data.procedure_text}"

        retrieved_rules = self._retrieve_guidelines(search_query)

        # --- STEP 2: AUGMENTATION (The Prompt) ---
        system_prompt = f"""
        You are a Certified Professional Coder (CPC) specializing in Emergency Medicine.
        
        ### KNOWLEDGE BASE (OFFICIAL GUIDELINES)
        The following rules are retrieved from the Official ICD-10 Guidelines. 
        You MUST follow these rules when assigning codes:
        
        {retrieved_rules}
        
        ### YOUR TASK
        Assign the most specific ICD-10-CM diagnosis code based on the clinical notes provided.
        
        ### RULES
        1. Always prefer SPECIFIC codes over UNSPECIFIED ones.
        2. If an 'Excludes1' note appears in the guidelines above, do NOT use that code.
        3. Provide clear reasoning citing the specific guideline used.
        """

        user_content = f"""
        Analyze this clinical data:
        - Chief Complaint: {extracted_data.chief_complaint}
        - Diagnosis/Impression: {extracted_data.diagnosis_text}
        - Procedures/Interventions: {extracted_data.procedure_text}
        """

        logger.info("Generating codes with RAG support...")

        # --- STEP 3: GENERATION (The Answer) ---
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_model=BillableCode,
                temperature=0.1 # Low temp for factual accuracy
            )
            return response

        except Exception as e:
            logger.error(f"Error in coding service: {e}")
            raise e