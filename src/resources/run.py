from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

from glob_utils._decorators import robust, setup_logging  # type: ignore
from openai import AsyncOpenAI
from openai.types.beta.assistant_create_params import (
    ToolAssistantToolsCode,
    ToolAssistantToolsFunction,
    ToolAssistantToolsRetrieval,
)
from openai.types.beta.threads.run import Run
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module
from typing_extensions import override

from .functions import OpenAIFunction
from .thread_message import ThreadMessageModel

T = TypeVar("T", bound=BaseModel)
logger = setup_logging(__name__)
basic_tools = [
    ToolAssistantToolsCode(type="code_interpreter"),
    ToolAssistantToolsRetrieval(type="retrieval"),
    *(
        ToolAssistantToolsFunction(type="function", function=func.definition())
        for func in OpenAIFunction.__subclasses__()
    ),
]


class BaseResource(
    BaseModel,
    Generic[T],
    ABC,
):
    metadata: Optional[dict[str, Any]] = Field(default=None)

    @classmethod
    def ai(cls):
        return AsyncOpenAI()

    @abstractmethod
    @robust
    async def post(self) -> T:
        ...

    @override
    def dict(self, *args: Any, **kwargs: Any):
        return super().dict(*args, exclude_none=True, **kwargs)


class RunResource(BaseResource[Run]):
    thread_id: str = Field(...)
    assistant_id: str = Field(...)
    instructions: Optional[str] = Field(default=None)
    model: Optional[str] = Field(default=None)
    tools: Optional[list[ToolAssistantToolsFunction]] = Field(default=None)

    async def post(self) -> Run:
        if self.tools is None:
            self.tools = basic_tools  # type: ignore
        else:
            self.tools = basic_tools + self.tools  # type: ignore
        return await self.ai().beta.threads.runs.create(
            **self.dict(),
        )

    @classmethod
    @robust
    async def get(cls, *, run_id: str, thread_id: str) -> Run:
        return await cls.ai().beta.threads.runs.retrieve(
            run_id=run_id, thread_id=thread_id
        )

    @classmethod
    @robust
    async def delete(cls, *, run_id: str, thread_id: str):
        return await cls.ai().beta.threads.runs.cancel(
            run_id=run_id, thread_id=thread_id
        )

    @classmethod
    @robust
    async def list(cls, *, thread_id: str, run_id: str):
        return await cls.ai().beta.threads.runs.steps.list(
            thread_id=thread_id, run_id=run_id
        )

    @classmethod
    async def exec_run(cls, run: Run, user_id: str):
        messages_api = cls.ai().beta.threads.messages
        while True:
            response = await cls.list(thread_id=run.thread_id, run_id=run.id)
            async for step in response:
                run = await cls.get(run_id=run.id, thread_id=run.thread_id)
                await asyncio.sleep(1.25)
                if run.status == "completed":
                    if step.step_details.type == "message_creation":
                        message_id = step.step_details.message_creation.message_id
                        message = await messages_api.retrieve(
                            message_id=message_id, thread_id=run.thread_id
                        )
                        if message.content:
                            await ThreadMessageModel(
                                key=user_id,
                                sort=message.id,
                                data=message,
                            ).put()
                            yield message.json()
                        yield {"event": "done", "data": ""}
                        return
                if run.status in ("queued", "in_progress", "requires_action"):
                    if step.step_details.type == "tool_calls":
                        for tool_call in step.step_details.tool_calls:
                            if tool_call.type == "function":
                                outputs = await asyncio.gather(
                                    *[
                                        func.submit_output(call=tool_call)
                                        for func in OpenAIFunction.__subclasses__()
                                    ]
                                )
                                await cls.ai().beta.threads.runs.submit_tool_outputs(
                                    run_id=run.id,
                                    thread_id=run.thread_id,
                                    tool_outputs=outputs,
                                )
                    elif step.step_details.type == "message_creation":
                        message_id = step.step_details.message_creation.message_id
                        message = await messages_api.retrieve(
                            message_id=message_id, thread_id=run.thread_id
                        )
                        if message.content:
                            await ThreadMessageModel(
                                key=user_id,
                                sort=message.id,
                                data=message,
                            ).put()
                            yield message.json()
