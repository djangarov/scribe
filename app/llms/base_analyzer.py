from abc import ABC, abstractmethod


class BaseLLMAnalyzerClient(ABC):

    @abstractmethod
    async def analyze_image(self, image_bytes: bytes, language: dict, mime_type: str) -> str:
        """Analyze an image and return the transcribed text."""
        ...

    def _build_system_prompt(self, lang: dict) -> str:
        return f"""
            Transcribe the handwritten {lang['name']} text in this image exactly as written.
            Preserve all letters, line breaks, and punctuation.
            If a letter is ambiguous between similar forms ({lang['hints']}),
            choose based on word context. Mark illegible portions as [illegible].
            Return a JSON object with these fields:
            - "text": the full transcription as a single string, preserving line breaks as
            - "average_confidence": a number from 0 to 100 estimating how legible the
            handwriting was overall (100 = perfectly clear, 0 = completely illegible)
            - "word_count": leave this as null; it will be computed separately
            Output only the JSON object, no commentary or markdown fences.
        """
