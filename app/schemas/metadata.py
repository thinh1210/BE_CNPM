from pydantic import BaseModel
from typing import Optional


class Metadata(BaseModel):
    page: int =1
    perpage: int = 10
    total: int = 0
    total_page: int = 0