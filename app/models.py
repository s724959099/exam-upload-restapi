from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    file_path: str
    content_type: str


engine = create_engine("sqlite:///sqlite.db")

SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
