import pytesseract
from fastapi.responses import JSONResponse
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
        raise HTTPException(415, f'Unsupported content type: {file.content_type}')

    contents = await file.read()
    if len(contents) > settings.max_upload_bytes:
        raise HTTPException(413, 'File too large (max 10 MB)')

    try:
        processed = tesseract.preprocess(contents)
        result = tesseract.run_ocr(processed, lang=lang, psm=6)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except pytesseract.TesseractError as e:
        raise HTTPException(500, f'Tesseract error: {e}')

    return result
