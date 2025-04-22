from typing import Optional
from sqlmodel import Field, SQLModel


class PulseModel(SQLModel, table=True):
    """Modelo de banco de dados para representar pulsos de consumo.

    Herda de SQLModel para integração com SQL e define a tabela no banco de dados.

    Attributes:
        id (Optional[int]): ID único do registro (chave primária). Gerado automaticamente se None.
        tenant (str): Identificador da organização. Deve ter entre 1 e 50 caracteres.
        product_sku (str): Código SKU do produto. Deve ter entre 1 e 50 caracteres.
        use_unity (str): Unidade de medida. Deve ter entre 1 e 10 caracteres.
        used_amount (int): Quantidade utilizada do produto. Deve ser maior que 0.
    """

    __tablename__ = "pulse" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant: str = Field(
        title="Identificador da organização", min_length=1, max_length=50
    )
    product_sku: str = Field(
        title="Código SKU do produto associado ao pulso.", min_length=1, max_length=50
    )
    use_unity: str = Field(
        title="Unidade de medida da quantidade utilizada.", min_length=1, max_length=10
    )
    used_amount: int = Field(title="Unidade de medida da quantidade utilizada.", gt=0)
