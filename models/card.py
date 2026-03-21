from pydantic import BaseModel, Field


class Card(BaseModel):
    id: int = Field(alias="nm_id")
    name: str = Field(alias="imt_name")
    descr: str = Field(alias="description")
