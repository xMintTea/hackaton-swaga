from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class LevelUpdate(BaseModel):
    level: int

class XPUpdate(BaseModel):
    xp: int

class CurrencyUpdate(BaseModel):
    currency: int


