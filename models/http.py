from pydantic import BaseModel
from typing import List, Dict, Optional
import json


class Message(BaseModel):
    role: str
    content: str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Eval(BaseModel):
    model: str
    messages: List[Message]
    temperature: float
    max_tokens: int
    frequency_penalty: float
    presence_penalty: float
    n: Optional[int] = None
    stop: Optional[List[str]] = None
    top_n: Optional[float] = None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Stand(BaseModel):
    answer: str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class GptRequest(BaseModel):
    eval: Eval
    stand: Stand
    response: Optional[str] = None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class GptRequestEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GptRequest):
            return obj.toJSON()
        return json.JSONEncoder.default(self, obj)
