from pydantic import BaseModel, Field
from typing import Optional


class NoteBase(BaseModel):
    title: str = Field(..., min_length=5)
    content: str = Field(..., min_length=1)
    is_public: bool = False


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int

from typing import Optional

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5)
    content: Optional[str] = Field(None, min_length=1)
    is_public: Optional[bool] = None
