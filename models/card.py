from pydantic import BaseModel, Field

class Charc(BaseModel):
    """Model for characteristics"""
    name: str = Field(alias="name")
    value: str = Field(alias="value")

class GroupOption(BaseModel):
    options: list[Charc] = Field(default_factory=list,
                                 alias="options")

class Card(BaseModel):
    id: int = Field(alias="nm_id")
    name: str = Field(alias="imt_name")
    descr: str = Field(alias="description", default="")
    options: list[Charc] = Field(default_factory=list, alias="options")
    group_options: list[GroupOption] = Field(default_factory=list,
                                             alias="grouped_options")
