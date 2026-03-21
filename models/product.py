from pydantic import BaseModel, Field, AliasPath
from models.size import Size


class Product(BaseModel):
    id: int

    sizes: list[Size]

    # price_base: int = Field(validation_alias=AliasPath("price", "basic"))
    # price_prod: int = Field(validation_alias=AliasPath("price", "product"))