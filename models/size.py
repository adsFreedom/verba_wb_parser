from pydantic import BaseModel, Field, AliasPath


class Size(BaseModel):
    name: str = Field(validation_alias=AliasPath("name"))
    orig_name: str = Field(validation_alias=AliasPath("origName"))

    price_base: int = Field(validation_alias=AliasPath("price", "basic"))
    price_prod: int = Field(validation_alias=AliasPath("price", "product"))
