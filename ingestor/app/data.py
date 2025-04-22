from dataclasses import dataclass


@dataclass(frozen=True)
class PulseData:
    tenant: str
    product_sku: str
    use_unity: str
    used_amount: int


@dataclass(frozen=True)
class AggregateData:
    tenant: str
    product_sku: str
    use_unity: str
    aggregate_amount: int
