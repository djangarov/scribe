from fastapi import APIRouter


router = APIRouter(
    prefix='/v1/internal',
    tags=['internal']
)

@router.get('/health')
async def health():
    return {'status': 'ok'}
