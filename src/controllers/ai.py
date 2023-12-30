import json
from typing import Any, AsyncIterable, Literal

from fastapi import APIRouter  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from openai import AsyncOpenAI
from sse_starlette.sse import EventSourceResponse  # type: ignore

from ..services import ElevenLabsAPIClient, PineCone  # type: ignore

HDRS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/50.0.2661.102 Safari/537.36"
}


class AIController(APIRouter):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    @property
    def ai(self):
        """
        Returns an instance of the AsyncOpenAI class.
        """
        return AsyncOpenAI()

    @property
    def images(self):
        """
        Returns the images associated with the AI object.
        """
        return self.ai.images

    @property
    def audio(self):
        """Returns the audio associated with the AI."""
        return self.ai.audio

    @property
    def chat(self):
        """
        Returns the completions for the chat AI.
        """
        return self.ai.chat.completions

    @property
    def xilabs(self):
        """
        Returns an instance of the ElevenLabsAPIClient class.
        """
        return ElevenLabsAPIClient()

    def vectordb(self, *, namespace: str):
        """
        Create a PineCone instance for the specified namespace.

        Args:
                namespace (str): The namespace for the PineCone instance.

        Returns:
                PineCone: An instance of the PineCone class.

        """
        return PineCone(namespace=namespace)

    async def generate_images(
        self,
        *,
        prompt: str,
        model: Literal["dall-e-2", "dall-e-3"] = "dall-e-3",
        size: Literal[
            "256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"
        ] = "1024x1024",
        response_format: Literal["url", "b64_json"] = "b64_json",
        n: int = 1,
        style: Literal["vivid", "natural"] = "vivid",
    ) -> list[str]:
        """
        Generates image(s) based on the given prompt using the specified model, size, response format, number of images, and style.

        Args:
                prompt (str): The prompt for generating the image(s).
                model (Literal["dall-e-2", "dall-e-3"], optional): The model to use for image generation. Defaults to "dall-e-3".
                size (Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], optional): The size of the generated image(s). Defaults to "1024x1024".
                response_format (Literal["url", "b64_json"], optional): The format of the response. Defaults to "b64_json".
                n (int, optional): The number of images to generate. Defaults to 1.
                style (Literal["vivid", "natural"], optional): The style of the generated image(s). Defaults to "vivid".

        Returns:
                list[str]: A list of generated image URLs or base64-encoded JSON strings, depending on the response format.
        """
        response = await self.images.generate(
            model=model,
            size=size,
            prompt=prompt,
            response_format=response_format,
            n=n,
            style=style,
        )
        if response_format == "url":
            return [r.url for r in response.data if r.url]
        return [r.b64_json for r in response.data if r.b64_json]

    async def text_to_speech(
        self,
        *,
        input: str,
        response_format: Literal["mp3", "opus", "aac", "flac"] = "opus",
        voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "nova",
        model: Literal["tts-1", "tts-1-hd"] = "tts-1",
        speed: float = 1,
    ) -> AsyncIterable[bytes]:
        """
        Transcribes the given audio input using the specified parameters.

        Args:
                input (str): The path or URL of the audio file to transcribe.
                response_format (Literal["mp3", "opus", "aac", "flac"], optional): The format of the transcribed audio response. Defaults to "opus".
                voice (Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"], optional): The voice to use for the transcription. Defaults to "nova".
                model (Literal["tts-1", "tts-1-hd"], optional): The model to use for the transcription. Defaults to "tts-1".
                speed (float, optional): The speed of the transcription. Defaults to 1.

        Yields:
                AsyncIterable[bytes]: A stream of transcribed audio chunks.

        Returns:
                AsyncIterable[bytes]: A stream of transcribed audio chunks.
        """
        response = await self.audio.speech.create(
            input=input,
            response_format=response_format,
            voice=voice,
            model=model,
            speed=speed,
        )
        iterable = await response.aiter_bytes()
        async for chunk in iterable:
            yield chunk

    async def visualize_images(self, *, text: str, url: list[str]) -> str:
        """
        Visualizes the given image URL.

        Args:
                url (str): The URL of the image to visualize.

        Returns:
                StreamingResponse: A streaming response of the image.
        """
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {"type": "image_url", "image_url": {"url": url}},
                ],
            }
        ]
        response = await self.chat.create(
            messages=messages, model="gpt-4-vision-preview"  # type: ignore
        )
        for choice in response.choices:
            content = choice.message.content
            if content:
                return content
        raise ValueError("No content found in response.")

    async def similarity_search(self, *, text: str, namespace: str):
        """
        Searches for similar text in the given namespace.

        Args:
                text (str): The text to search for.
                namespace (str): The namespace to search in.

        Returns:
                list[dict]: A list of similar text.
        """
        pinecone = self.vectordb(namespace=namespace)
        return await pinecone.query(text=text)

    async def text_to_voice(self, *, text: str) -> AsyncIterable[bytes]:
        """
        Generates text-to-speech audio chunks using the Xi Labs API.

        Args:
            text (str): The text to be converted to speech.

        Yields:
            bytes: Audio chunks generated from the text-to-speech conversion.
        """
        async for chunk in self.xilabs.text_to_speech_stream(text=text):
            yield chunk

    async def chatgpt(self, *, text: str, namespace: str) -> AsyncIterable[str]:
        """
        Generates a response to the given text using the ChatGPT API.

        Args:
            text (str): The text to generate a response to.

        Yields:
            str: A response to the given text.
        """
        retrieved = await self.similarity_search(text=text, namespace=namespace)
        context_window = "\n".join(r.json() for r in retrieved or [])
        stream = await self.chat.create(
            messages=[
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": f"Relevant results from knowledge base:\n{context_window}",
                },
            ],
            model="gpt-4-1106-preview",
            stream=True,
        )
        async for message in stream:
            for choice in message.choices:
                chunk = choice.delta.content
                if chunk:
                    yield chunk
        yield {"event": "done", "data": ""}  # type: ignore


def setup_ai_routes():
    ai = AIController(
        prefix="/api/ai", tags=["ai"], responses={404: {"description": "Not found"}}
    )

    @ai.get("/images")
    async def _(
        *,
        text: str,
        model: Literal["dall-e-2", "dall-e-3"] = "dall-e-3",
        size: Literal[
            "256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"
        ] = "1024x1024",
        response_format: Literal["url", "b64_json"] = "b64_json",
        n: int = 1,
        style: Literal["vivid", "natural"] = "vivid",
    ):
        """
        Generates image(s) based on the given prompt using the specified model, size, response format, number of images, and style.

        Args:
                prompt (str): The prompt for generating the image(s).
                model (Literal["dall-e-2", "dall-e-3"], optional): The model to use for image generation. Defaults to "dall-e-3".
                size (Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], optional): The size of the generated image(s). Defaults to "1024x1024".
                response_format (Literal["url", "b64_json"], optional): The format of the response. Defaults to "b64_json".
                n (int, optional): The number of images to generate. Defaults to 1.
                style (Literal["vivid", "natural"], optional): The style of the generated image(s). Defaults to "vivid".

        Returns:
                list[str]: A list of generated image URLs or base64-encoded JSON strings, depending on the response format.
        """
        return await ai.generate_images(
            prompt=text,
            model=model,
            size=size,
            response_format=response_format,
            n=n,
            style=style,
        )

    @ai.get("/audio")
    async def _(text: str):
        return StreamingResponse(ai.text_to_speech(input=text), media_type="audio/opus")

    @ai.get("/vision")
    async def _(text: str, urls: list[str]):
        return await ai.visualize_images(text=text, url=urls)

    @ai.get("/search/{namespace}")
    async def _(text: str, namespace: str):
        return await ai.similarity_search(text=text, namespace=namespace)

    @ai.get("/chat/{namespace}")
    async def _(text: str, namespace: str):
        return EventSourceResponse(ai.chatgpt(text=text, namespace=namespace))

    @ai.get("/voice")
    async def _(text: str):
        return StreamingResponse(ai.text_to_voice(text=text), media_type="audio/opus")

    return ai
