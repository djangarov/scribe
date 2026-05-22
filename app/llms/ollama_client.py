import json

from ollama import AsyncClient, ChatResponse
from app.llms.base_analyzer import BaseLLMAnalyzerClient
from app.model.scribe import Result as ScribeResult

class OllamaClient(BaseLLMAnalyzerClient):

    def __init__(self, model: str = 'gemma4', base_url: str = 'http://localhost:11434'):
        self.model = model
        self.client = AsyncClient(host=base_url)

    async def analyze_image(self, image_bytes: bytes, language: dict, mime_type: str) -> str:
        response: ChatResponse = await self.client.chat(
            model=self.model,
            messages=[
                {'role': 'system', 'content': self._build_system_prompt(language)},
                {'role': 'user', "images": [image_bytes]}
            ],
            format='json',
            stream=False
        )

        print('Ollama response:', response.message.content)

        data = json.loads(response.message.content)

        print('Ollama response 2:', data.text)


        return ScribeResult(data.text.split(), data.average_confidence, len(data.text.split()))
