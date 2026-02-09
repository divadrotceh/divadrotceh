from toDoApp.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped
from typing import List, Optional
from sqlalchemy import ForeignKey, String
import uuid

class User(Base):
  #Table Name
  __tablename__ = "user_account"
  
  #Columns
  user_name: Mapped(str)
  password_hash: Mapped(str)
  id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  
  def __repr__(self):
    return f"User Name: {self.user_name}, id: {self.id}"
