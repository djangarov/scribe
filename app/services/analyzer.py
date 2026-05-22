from app.llms import get_llm_client

async def analyze_image(image_bytes: bytes, language: dict, mime_type: str) -> str:
    client = get_llm_client()

    return await client.analyze_image(image_bytes, language, mime_type)
