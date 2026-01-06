from fastapi import APIRouter, UploadFile, File, HTTPException
from src.backend.services.vision import VisionService
from src.backend.services.coding import CodingService
from loguru import logger

router = APIRouter()
vision_service = VisionService()
coding_service = CodingService()

@router.post("/digitize")
async def digitize_note(file: UploadFile = File(...)):
    """
    1. Uploads an image.
    2. Vision Service extracts text (Eyes).
    3. Coding Service assigns ICD-10 codes (Brain).
    """
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG/PNG allowed.")
    
    content = await file.read()
    try:
        logger.info("Step 1: Extracting text from image...")
        extracted_data = vision_service.analyze_medical_note(content)

        logger.info("Step 2: Assigning medical codes...")
        coding_result = coding_service.generate_codes(extracted_data)
        logger.info("Digitization and coding complete.")
        
        return {
            "status": "success",
            "data": {
                "extracted_data": extracted_data,
                "coding_result": coding_result
            }
        }
    except Exception as e:
        logger.error(f"Error processing note: {e}")
        raise HTTPException(status_code=500, detail=str(e))