from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class NoteDB(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    is_public = Column(Boolean, default=False)