from collections.abc import Mapping
from typing import Any, Optional
from pydantic import BaseModel, Field, AliasChoices
import base64
import json

class AssumeRole_v1(BaseModel):
    aws: Optional[list[str]] = Field(..., validation_alias=AliasChoices('aws','AWS'), serialization_alias="AWS")
    service: Optional[list[str]] = Field(..., validation_alias=AliasChoices('service', 'Service'), serialization_alias="Service")
    federated: Optional[str] = Field(..., validation_alias=AliasChoices('federated', 'Federated'), serialization_alias="Federated")


class AwsIamRole(BaseModel):
    annotations: Optional[Mapping[Any, Any]] = {}
    assume_action: Optional[str] = "AssumeRole"
    assume_condition: Optional[str] = None
    assume_role: AssumeRole_v1
    identifier: str
    inline_policy: Optional[str] = None


class AppInterfaceInput(BaseModel):
    resource: AwsIamRole
    tags: dict[str,str]

def parse_input(b64input: str) -> AppInterfaceInput:
    str_input = base64.b64decode(b64input.encode("utf-8")).decode("utf-8")
    input = AppInterfaceInput.model_validate(json.loads(str_input))
    return input
