from pydantic import BaseModel, Field, AliasPath
from models.size import Size


class Product(BaseModel):
    id: int
    name: str = Field(alias="name", default="")
    sizes: list[Size]
    supplier: str = Field(alias="supplier")
    supplier_id: int = Field(alias="supplierId")
    total_quantity: int = Field(alias="totalQuantity")
    rating: float = Field(alias="reviewRating")
    feedbacks: int
    pics: int
