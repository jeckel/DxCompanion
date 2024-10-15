import json

from pydantic import BaseModel, Field

class Package(BaseModel):
    name: str
    version: str

class Composer(BaseModel):
    type: str
    license: str
    minimum_stability: str = Field(str, alias="minimum-stability")
    prefer_stable: bool = Field(False, alias="prefer-stable")
    require: dict[str, Package]
    require_dev: dict[str, Package]

    @classmethod
    def from_json(cls, json_path: str):
        with open(json_path, "r") as file:
            data = json.load(file)
            require = {package:Package(name=package, version=version) for package, version in data.pop("require", []).items()}
            require_dev = {package:Package(name=package, version=version) for package, version in data.pop("require-dev", []).items()}
            return cls(require_dev=require_dev, require=require, **data)
