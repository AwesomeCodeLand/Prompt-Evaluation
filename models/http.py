from pydantic import BaseModel
from typing import List, Dict, Optional

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

class Stand(BaseModel):
    answer: str

class GptRequest(BaseModel):
    eval: Eval
    stand: Stand
