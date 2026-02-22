from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class CreateGameficationRecord(BaseModel):
    user_id: int
    
    xp: int
    level: int
    currency: int

class LevelUpdate(BaseModel):
    level: int

class XPUpdate(BaseModel):
    xp: int

class CurrencyUpdate(BaseModel):
    currency: int


