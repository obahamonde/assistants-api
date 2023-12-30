import os
import subprocess
from uuid import uuid4

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


class DeploymentScript(BaseModel):
    account: str = Field(default_factory=lambda: "obahamonde")
    repo: str = Field(default_factory=lambda: "assistants-app")
    domain: str = Field(default_factory=lambda: "app.oscarbahamonde.com")
    tag: str = Field(default_factory=lambda: uuid4().hex)

    def from_env(self):
        return Environment(loader=FileSystemLoader("kubernetes"), trim_blocks=True)

    def render(self, template: str):
        return self.from_env().get_template(f"{template}.j2").render(**self.dict())

    def run(self):
        tag = uuid4().hex
        build = self.render("build")
        subprocess.run(["bash", "-c", build], check=True)
        deployment = self.render("deployment")
        with open(tag + ".yaml", "w") as f:
            f.write(deployment)
        subprocess.run(["kubectl", "apply", "-f", tag + ".yaml"], check=True)
        os.remove(tag + ".yaml")


if __name__ == "__main__":
    DeploymentScript().run()
