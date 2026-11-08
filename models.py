from pydantic import BaseModel, Field

class CreateZadanie(BaseModel):
    tytul: str = Field(
        min_length=1,
        max_length=100,
    )

    opis:str | None = Field(
        default=None,
        max_length=500,
    )

class UpdateZadanie(BaseModel):
    tytul: str = Field(
        min_length=1,
        max_length=100,
    )

    opis: str | None = Field(
        default=None,
        max_length=500,
    )

    wykonane: bool

class ZadaniePatch(BaseModel):
    wykonane: bool