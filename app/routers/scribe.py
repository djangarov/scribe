from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.params import File, Form
from app.config import settings
from app.helpers import language
from app.model.scribe import Result as ScribeResult
from app.services import tesseract
from app.services.analyzer import analyze_image


router = APIRouter(
    prefix='/v1/scribe',
    tags=['scribe']
)

def _validate_image(file: UploadFile) -> None:
    if file.content_type not in settings.allowed_image_types:
        raise HTTPException(status_code=415, detail=f'Unsupported content type: {file.content_type}')


async def _get_image_bytes(file: UploadFile) -> bytes:
    contents = await file.read()
    if len(contents) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail='File too large (max 10 MB)')

    return contents


@router.post('/ocr', response_model=ScribeResult)
async def ocr(file: UploadFile = File(...), lang: str = Form('en')) -> ScribeResult:
    _validate_image(file)
    contents = await _get_image_bytes(file)

    try:
        processed = tesseract.preprocess(contents)
    except Exception as e:
        raise HTTPException(status_code=422, detail='Failed to process image: {e}') from e

    try:
        lang = language.resolve(lang)
        result = tesseract.run_ocr(processed, lang=lang['tesseract'], psm=6)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'OCR failed: {e}') from e

    return result


@router.post('/llm', response_model=ScribeResult)
async def llm(file: UploadFile = File(...), lang: str = Form('en')) -> ScribeResult:
    _validate_image(file)
    contents = await _get_image_bytes(file)

    try:
        lang = language.resolve(lang)
        result = await analyze_image(contents, lang, file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Parsing failed: {e}') from e

    return result

