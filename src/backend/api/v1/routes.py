from fastapi import APIRouter, UploadFile, File, HTTPException
from src.backend.services.vision import VisionService

router = APIRouter()
vision_service = VisionService()

@router.post("/digitize")
async def digitize_note(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG/PNG allowed.")
    
    content = await file.read()
    try:
        result = vision_service.analyze_medical_note(content)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))