from pydantic import BaseModel

class PulseModel(BaseModel):
    tenant: str
    product_sku: str
    used_amount: int
    use_unity: str
