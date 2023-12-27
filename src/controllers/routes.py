from fastapi import File, UploadFile
from sse_starlette.sse import EventSourceResponse

from ..resources import (
    AssistantRequest,
    AssistantResponse,
    AssistantService,
    FileObjectRequest,
    FileObjectResponse,
    FileObjectService,
    Run,
    RunResource,
    ThreadMessageRequest,
    ThreadMessageService,
    ThreadRequest,
    ThreadResponse,
    ThreadService,
)
from ..resources import ThreadMessage as ThreadMessageResponse
from ._controller import APIRouter, Controller
from .auth import app as auth_app


def setup_routes():
    """
    Set up the routes for the router.
    """
    assistants = Controller[AssistantRequest, AssistantResponse](
        prefix="/assistants", tags=["assistants"]
    )
    threads = Controller[ThreadRequest, ThreadResponse](
        prefix="/threads", tags=["threads"]
    )
    thread_messages = Controller[ThreadMessageRequest, ThreadMessageResponse](
        prefix="/thread_messages", tags=["thread_messages"]
    )
    file_objects = Controller[FileObjectRequest, FileObjectResponse](
        prefix="/file_objects", tags=["file_objects"]
    )
    run = APIRouter(prefix="/run", tags=["run"])

    @run.get("/{thread_id}")
    async def _(thread_id: str, run_id: str, user_id: str):
        async def __():
            async for event in RunResource.exec_run(
                run=await RunResource.get(run_id=run_id, thread_id=thread_id),
                user_id=user_id,
            ):
                yield event

        return EventSourceResponse(__())

    @run.post("/{thread_id}", response_model=Run)
    async def _(thread_id: str, assistant_id: str):
        return await RunResource(thread_id=thread_id, assistant_id=assistant_id).post()

    @assistants.get("/", response_model=list[AssistantResponse])
    async def _(user: str):
        return await AssistantService().list_(key=user)

    @assistants.post("/", response_model=AssistantResponse)
    async def _(user: str, data: AssistantRequest):
        return await AssistantService().create_(data=data, key=user)

    @assistants.get("/{assistant_id}", response_model=AssistantResponse)
    async def _(user: str, assistant_id: str):
        return await AssistantService().get_(key=user, sort=assistant_id)

    @assistants.put("/{assistant_id}", response_model=AssistantResponse)
    async def _(
        user: str, assistant_id: str, data: AssistantRequest
    ) -> AssistantResponse:
        return await AssistantService().update_(key=user, sort=assistant_id, data=data)

    @assistants.delete("/{assistant_id}")
    async def _(user: str, assistant_id: str):
        await AssistantService().delete_(key=user, sort=assistant_id)

    @threads.get("/", response_model=list[ThreadResponse])
    async def _(user: str):
        return await ThreadService().list_(key=user)

    @threads.post("/", response_model=ThreadResponse)
    async def _(user: str, data: ThreadRequest):
        return await ThreadService().create_(key=user, data=data)  ####

    @threads.get("/{thread_id}", response_model=ThreadResponse)
    async def _(user: str, thread_id: str):
        return await ThreadService().get_(key=user, sort=thread_id)

    @threads.put("/{thread_id}", response_model=ThreadResponse)
    async def _(user: str, thread_id: str, data: ThreadRequest) -> ThreadResponse:
        return await ThreadService().update_(key=user, sort=thread_id, data=data)

    @threads.delete("/{thread_id}")
    async def _(user: str, thread_id: str):
        return await ThreadService().delete_(key=user, sort=thread_id)

    @thread_messages.get("/", response_model=list[ThreadMessageResponse])
    async def _(user: str):
        return await ThreadMessageService().list_(key=user)

    @thread_messages.post("/", response_model=ThreadMessageResponse)
    async def _(user: str, data: ThreadMessageRequest):
        return await ThreadMessageService().create_(data=data, key=user)

    @thread_messages.get("/{thread_message_id}", response_model=ThreadMessageResponse)
    async def _(user: str, thread_message_id: str):
        return await ThreadMessageService().get_(key=user, sort=thread_message_id)

    @thread_messages.put("/{thread_message_id}", response_model=ThreadMessageResponse)
    async def _(user: str, thread_message_id: str, data: ThreadMessageRequest):
        return await ThreadMessageService().update_(
            key=user, sort=thread_message_id, data=data
        )

    @thread_messages.delete("/{thread_message_id}")
    async def _(user: str, thread_message_id: str):
        return await ThreadMessageService().delete_(key=user, sort=thread_message_id)

    @file_objects.get("/", response_model=list[FileObjectResponse])
    async def _(user: str):
        return await FileObjectService().list_(key=user)

    @file_objects.post("/", response_model=FileObjectResponse)
    async def _(user: str, file: UploadFile = File(...)):
        data = FileObjectRequest(file=file)
        return await FileObjectService().create_(data=data, key=user)

    @file_objects.get("/{file_object_id}", response_model=FileObjectResponse)
    async def _(user: str, file_id: str):
        return await FileObjectService().get_(key=user, sort=file_id)

    @file_objects.put("/{file_object_id}", response_model=FileObjectResponse)
    async def _(user: str, file_id: str, data: FileObjectRequest):
        return await FileObjectService().update_(key=user, sort=file_id, data=data)

    @file_objects.delete("/{file_object_id}")
    async def _(user: str, file_object_id: str):
        return await FileObjectService().delete_(key=user, sort=file_object_id)

    router = APIRouter(prefix="/api")

    router.include_router(assistants)
    router.include_router(threads)
    router.include_router(thread_messages)
    router.include_router(file_objects)
    router.include_router(run)
    router.include_router(auth_app)
    return router
