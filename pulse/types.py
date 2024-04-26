from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from typing import List


@dataclass
class APIErrorData(JSONWizard):
    error: str
    code: str


@dataclass
class APIResponse(JSONWizard):
    errors: List[APIErrorData]


@dataclass
class ClassifyPayload(JSONWizard):
    token: str
    site_key: str
    secret_key: str


@dataclass
class ClassifyResponse(APIResponse):
    is_bot: bool
