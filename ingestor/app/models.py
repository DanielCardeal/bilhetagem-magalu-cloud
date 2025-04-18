from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class PulseCreate(BaseModel):
    tenant: str
    product_sku: str
    used_amount: int
    use_unity: str

class Pulse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant: str
    product_sku: str
    used_amount: int
    use_unity: str
