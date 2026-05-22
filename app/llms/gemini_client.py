import json

from cv2 import data
from google import genai
from google.genai import types
from app.llms.base_analyzer import BaseLLMAnalyzerClient
from app.model.scribe import Result as ScribeResult

class GeminiClient(BaseLLMAnalyzerClient):

    def __init__(self, api_key: str, model: str = 'gemini-2.5-flash'):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def analyze_image(self, image_bytes: bytes, language: dict, mime_type: str) -> str:
        response: types.GenerateContentResponse = await self.client.aio.models.generate_content(
            model=self.model,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            ],
            config=self._build_config(language)
        )

        print('Gemini response:', response)

        data = json.loads(response.text)

        return ScribeResult(data.text.split(), data.average_confidence, len(data.text.split()))

    def _build_config(self, language: str | None = None) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            system_instruction=self._build_system_prompt(language),
            response_mime_type='application/json'
        )
