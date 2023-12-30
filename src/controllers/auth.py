import json

from dynamodm import DynaModel  # type: ignore
from fastapi import APIRouter
from google_auth_oauthlib.flow import Flow  # type: ignore
from httpx import AsyncClient
from pydantic import BaseModel, Field  # pylint: disable=E0611


class GoogleUserInfo(DynaModel):
    id: str = Field(pk=True)
    name: str
    given_name: str
    family_name: str
    picture: str
    locale: str = Field(default="en", sk=True)


class WebConfig(BaseModel):
    client_id: str
    project_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_secret: str
    redirect_uris: list[str]
    javascript_origins: list[str]


class Code(BaseModel):
    code: str


class Config(BaseModel):
    web: WebConfig


def get_flow():
    config_data = json.loads(open("config.json").read())
    config = Config(**config_data)
    flow = Flow.from_client_config(  # type: ignore
        client_config={"web": config.web.dict()},
        scopes=[
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/calendar.events",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/presentations",
            "https://www.googleapis.com/auth/forms",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ],
        redirect_uri="https://app.oscarbahamonde.com",
    )
    return flow


app = APIRouter(prefix="/auth", tags=["google"])


@app.get("/authorize")
async def forward_oauth_url():
    flow = get_flow()
    auth_url, _ = flow.authorization_url(prompt="consent")  # type: ignore
    assert isinstance(auth_url, str)
    return {"url": auth_url}


@app.post("/token")
async def get_current_user(code: Code):
    flow = get_flow()
    flow.fetch_token(code=code.code)  # type: ignore
    credentials = flow.credentials
    token = credentials.token  # type: ignore
    assert isinstance(token, str)
    async with AsyncClient(headers={"Authorization": f"Bearer {token}"}) as client:
        response = await client.get("https://www.googleapis.com/oauth2/v2/userinfo")
        response.raise_for_status()
        data = response.json()
        user_info = GoogleUserInfo(**data)
        user = await user_info.put()
        return {"token": token, "user_info": user}
