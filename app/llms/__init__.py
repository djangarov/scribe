from app.llms.base_analyzer import BaseLLMAnalyzerClient
from app.llms.gemini_client import GeminiClient
from app.llms.ollama_client import OllamaClient

from app.config import settings

def get_llm_client() -> BaseLLMAnalyzerClient:
    provider = settings.llm_provider

    match provider:
        case 'gemini':
            api_key = settings.gemini_api_key

            if not api_key:
                raise ValueError('GEMINI_API_KEY not found.')

            return GeminiClient(api_key=api_key)
        case 'ollama':
            return OllamaClient()
        case _:
            raise ValueError(f'Unknown LLM provider: {provider}')
