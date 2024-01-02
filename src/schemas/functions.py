import base64
import json
from abc import ABC, abstractmethod
from functools import lru_cache, singledispatch
from typing import Any, Generic, TypeVar, cast

from fastapi import HTTPException
from glob_utils._decorators import robust, setup_logging  # type: ignore
from openai import AsyncOpenAI
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from openai.types.beta.threads.runs.function_tool_call import FunctionToolCall
from openai.types.chat.completion_create_params import Function
from pydantic import BaseModel  # pylint: disable=E0611

T = TypeVar("T", bound=BaseModel)
R = TypeVar("R")

logger = setup_logging()


@singledispatch
def parse_output(output: Any) -> str:
    return str(output)


@parse_output.register
def _(output: BaseModel) -> str:
    return output.json()


@parse_output.register
def _(output: bytes) -> str:
    return base64.b64encode(output).decode("utf-8")


@parse_output.register
def _(output: dict) -> str:  # type: ignore
    return json.dumps({k: parse_output(v) for k, v in output.items()})  # type: ignore


@parse_output.register
def _(output: list) -> str:  # type: ignore
    return json.dumps([parse_output(item) for item in output])  # type: ignore


class OpenAIFunctionCall(BaseModel, Generic[R]):
    function: str
    data: R


class OpenAIFunction(BaseModel, Generic[R], ABC):
    """Base class for OpenAI functions should be subclassed for each function"""

    @classmethod
    @lru_cache
    def definition(cls) -> Function:
        assert cls.__doc__ is not None, "OpenAIFunction must have a docstring"
        _schema = cls.schema()  # type: ignore
        _name = cls.__name__.lower()
        _description = cls.__doc__
        _parameters = cast(
            dict[str, object],
            (
                {
                    "type": "object",
                    "properties": {
                        k: v for k, v in _schema["properties"].items() if k != "self"
                    },
                    "required": _schema.get("required", []),
                }
            ),
        )
        return Function(name=_name, description=_description, parameters=_parameters)

    @property
    def name_(self) -> str:
        return self.__class__.__name__.lower()

    @classmethod
    def ai(cls) -> AsyncOpenAI:
        return AsyncOpenAI()

    @abstractmethod
    async def run(self) -> R:
        raise NotImplementedError

    @robust
    async def __call__(self) -> OpenAIFunctionCall[R]:
        logger.info("Calling %s", self.__class__.__name__.lower())
        response = await self.run()
        return OpenAIFunctionCall(function=self.name_, data=response)

    @classmethod
    @robust
    async def submit_output(cls, call: FunctionToolCall) -> ToolOutput:
        instance = cls.parse_raw(call.function.arguments)
        result = await instance.run()
        return ToolOutput(tool_call_id=call.id, output=parse_output(result))

    @classmethod
    @robust
    async def exec(cls, text: str):
        response = await cls.ai().chat.completions.create(
            messages=[{"content": text, "role": "user"}],
            model="gpt-4-1106-preview",
            functions=[cls.definition() for cls in cls.__subclasses__()],
        )
        if len(response.choices) == 0:
            raise HTTPException(status_code=500, detail="No response from OpenAI")
        for choice in response.choices:
            function_call = choice.message.function_call
            if function_call is None:
                model_output = choice.message.content
                if model_output is None:
                    raise HTTPException(
                        status_code=500, detail="No response from OpenAI"
                    )
                return model_output
            function_name = function_call.name
            arguments = function_call.arguments
            for func in cls.__subclasses__():
                if func.__name__.lower() == function_name:
                    instance = func.parse_raw(arguments)
                    return await instance()
