import json

from pydantic import BaseModel, Field

class Composer(BaseModel):
    type: str
    license: str
    minimum_stability: str = Field(str, alias="minimum-stability")
    prefer_stable: bool = Field(False, alias="prefer-stable")
    require: dict[str, str]
    require_dev: dict[str, str] = Field(alias="require-dev")

    @classmethod
    def from_json(cls, json_path: str):
        with open(json_path, "r") as file:
            return cls(**json.load(file))
