import json

from pydantic import BaseModel, Field

class Composer(BaseModel):
    type: str
    license: str
    minimum_stability: str = Field(str, alias="minimum-stability")
    prefer_stable: bool = Field(False, alias="prefer-stable")
    require: dict[str, str]
    require_dev: dict[str, str]
    scripts: dict[str, str|list[str]|dict[str, str]]

    @classmethod
    def from_json(cls, json_path: str):
        with open(json_path, "r") as file:
            data = json.load(file)
            require = data.pop("require", [])
            require_dev = data.pop("require-dev", [])
            # require = {package:Package(name=package, version=version) for package, version in data.pop("require", []).items()}
            # require_dev = {package:Package(name=package, version=version) for package, version in data.pop("require-dev", []).items()}
            return cls(require_dev=require_dev, require=require, **data)

    @property
    def manual_scripts(self) -> list[str]:
        exclude = ("auto-scripts", "post-install-cmd", "post-update-cmd")
        return list(filter(lambda x: x not in exclude, list(self.scripts.keys())))
        # return list(self.scripts.keys())
