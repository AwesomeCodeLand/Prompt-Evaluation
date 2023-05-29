from pydantic import BaseModel
from typing import List, Dict, Optional
import json

# class GptRequest(BaseModel):
# {
#     "eval": {
#         "model": "gpt-3.5-turbo",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": ""
#             }
#         ],
#         "temperature": 0,
#         "max_tokens": 2300,
#         "frequency_penalty": 0,
#         "presence_penalty": 2
#     },
#     "stand": {
#         "answer": ""
#     }
# }


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
