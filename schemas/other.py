from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class Response(BaseModel):
    data: str

class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    
