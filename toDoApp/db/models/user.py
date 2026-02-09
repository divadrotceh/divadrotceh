from toDoApp.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import mapped_column
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped

class User(Base):
  #Table Name
  __tablename__ = "user_account"
  
  #Columns
  user_name: Mapped(str)
  password_hash: Mapped(str)
  id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  
  def __repr__(self):
    return f"User Name: {self.user_name}, id: {self.id}"
