from sqlmodel import Field, Session, SQLModel, create_engine, select


class Baby(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    given_name: str

# class BabyBase(SQLModel):
#     given_name: str

# class Baby(BabyBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)

# class BabyCreate(BabyBase):
#     pass