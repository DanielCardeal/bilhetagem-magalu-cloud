from sqlmodel import Field
from pydantic import BaseModel


class PulseBase(BaseModel):
    """Modelo com os parâmetros básicos de identificação de um pulso.

    Attributes:
        tenant (str): Identificador da organização. Deve ter pelo menos 1 caractere.
        product_sku (str): Código SKU do produto associado ao pulso. Deve ter pelo menos 1 caractere.
        use_unity (str): Unidade de medida da quantidade utilizada. Deve ter pelo menos 1 caractere.
    """

    tenant: str = Field(title="Identificador da organização", min_length=1)
    product_sku: str = Field(
        title="Código SKU do produto associado ao pulso.", min_length=1
    )
    use_unity: str = Field(
        title="Unidade de medida da quantidade utilizada.", min_length=1
    )


class PulseCreate(PulseBase):
    """Modelo para criação de um novo pulso de consumo, herdando de PulseBase.

    Adiciona o atributo de quantidade utilizada.

    Attributes:
        used_amount (int): Quantidade utilizada do produto. Deve ser maior que 0.
    """

    used_amount: int = Field(title="Quantidade utilizada do produto", gt=0)


class PulseAggregate(PulseBase):
    """Modelo para representar dados agregados de pulsos de consumo.

    Adiciona o atributo de quantidade agregada utilizada.

    Attributes:
        aggregate_amount (int): Soma total das quantidades utilizadas. Deve ser maior que 0.
    """

    aggregate_amount: int = Field(title="Soma total das quantidades utilizadas.", gt=0)
