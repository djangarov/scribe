import numpy as np
import cv2
import pytesseract
from PIL import Image
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.params import File, Form
from app.config import settings

router = APIRouter(
    prefix='/v1/scribe',
    tags=['scribe']
)


def preprocess(image_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError('Could not decode image')

    img = cv2.fastNlMeansDenoising(img, h=30)
    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10,
    )
    return img


def run_ocr(image: np.ndarray, lang: str, psm: int) -> dict:
    config = f'--psm {psm} --oem 3'
    pil_img = Image.fromarray(image)

    text = pytesseract.image_to_string(pil_img, lang=lang, config=config)
    data = pytesseract.image_to_data(
        pil_img, lang=lang, config=config,
        output_type=pytesseract.Output.DICT,
    )

    # Average confidence across recognized words
    confidences = [int(c) for c in data['conf'] if c != '-1']
    avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

    return {
        'text': text.strip(),
        'average_confidence': round(avg_conf, 2),
        'word_count': len([w for w in data['text'] if w.strip()]),
    }

@router.post('/ocr')
async def ocr(file: UploadFile = File(...), lang: str = Form('bul')):
    if file.content_type not in settings.allowed_image_types:
        raise HTTPException(415, f'Unsupported content type: {file.content_type}')

    contents = await file.read()
    if len(contents) > settings.max_upload_bytes:
        raise HTTPException(413, 'File too large (max 10 MB)')

    try:
        processed = preprocess(contents)
        result = run_ocr(processed, lang=lang, psm=6)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except pytesseract.TesseractError as e:
        raise HTTPException(500, f'Tesseract error: {e}')

    return JSONResponse({
        'filename': file.filename,
        'language': lang,
        **result,
    })
