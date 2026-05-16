from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.params import File, Form
from app.config import settings
from app.model.scribe import OCRResult
from app.services import tesseract


router = APIRouter(
    prefix='/v1/scribe',
    tags=['scribe']
)


@router.post('/ocr', response_model=OCRResult)
async def ocr(file: UploadFile = File(...), lang: str = Form('eng')):
    if file.content_type not in settings.allowed_image_types:
        raise HTTPException(status_code=415, detail=f'Unsupported content type: {file.content_type}')

    contents = await file.read()
    if len(contents) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail='File too large (max 10 MB)')

    try:
        processed = tesseract.preprocess(contents)
    except Exception as e:
        raise HTTPException(status_code=422, detail='Failed to process image: {e}') from e

    try:
        result = tesseract.run_ocr(processed, lang=lang, psm=6)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'OCR failed: {e}') from e

    return result
