from typing import Generic, TypeVar

from fastapi import APIRouter
from pydantic import BaseModel  # pylint: disable=E0611

from ..schemas._service import Service

I = TypeVar("I", bound=BaseModel)
O = TypeVar("O", bound=BaseModel)


class Controller(APIRouter, Generic[I, O]):
    @property
    def service(self) -> Service[I, O]:
        return Service[I, O]()  # pylint: disable=E0110 # type: ignore

    async def post_(self, *, key: str, data: I):
        return await self.service.create_(key=key, data=data)

    async def list_(self, *, key: str):
        return await self.service.list_(key=key)

    async def get_(self, *, key: str, sort: str):
        return await self.service.get_(key=key, sort=sort)

    async def put_(self, *, key: str, sort: str, data: I):
        return await self.service.update_(key=key, sort=sort, data=data)

    async def delete_(self, *, key: str, sort: str):
        await self.service.delete_(key=key, sort=sort)
