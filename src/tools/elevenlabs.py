from os import environ

from glob_utils import APIClient  # type: ignore
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


class TextToSpeechRequestVoiceSettings(BaseModel):
    stability: float = Field(default=0.5)
    similarity_boost: float = Field(default=0.5)


class TextToSpeechRequest(BaseModel):
    text: str
    voice_settings: TextToSpeechRequestVoiceSettings = Field(
        default_factory=TextToSpeechRequestVoiceSettings
    )


class ElevenLabsAPIClient(APIClient):
    base_url: str = Field(default="https://api.elevenlabs.io")
    headers: dict[str, str] = Field(
        default={"xi-api-key": f"{environ['ELEVENLABS_API_KEY']}"}
    )

    async def text_to_speech(
        self, *, text: str, voice_id: str = "5ao2fgWmmpWM04HZmPUz"
    ):
        data = TextToSpeechRequest(text=text)
        response = await self.fetch(
            "v1/text-to-speech/" + voice_id,
            method="POST",
            json=data.dict(),
        )
        async for chunk in response.aiter_bytes():
            yield chunk

    async def text_to_speech_stream(
        self, *, text: str, voice_id: str = "5ao2fgWmmpWM04HZmPUz"
    ):
        data = TextToSpeechRequest(text=text)
        response = await self.fetch(
            "v1/text-to-speech/" + voice_id + "/stream",
            method="POST",
            json=data.dict(),
        )
        async for chunk in response.aiter_bytes():
            yield chunk
