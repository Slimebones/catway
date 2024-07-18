from typing import Self

from pydantic import BaseModel
from pykit.obj import get_fully_qualified_name


class ErrDto(BaseModel):
    """
    Represents an error as data transfer object.
    """
    codeid: int | None = None
    """
    Is none for errors without assigned fcode.
    """
    name: str
    msg: str

    @classmethod
    def create(cls, err: Exception, codeid: int | None = None) -> Self:
        name = get_fully_qualified_name(err)
        msg = ", ".join([str(a) for a in err.args])
        return cls(codeid=codeid, msg=msg, name=name)
