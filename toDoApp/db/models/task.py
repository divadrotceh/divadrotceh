from toDoApp.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
import uuid

class Task(Base):
  #Table Name
  __tablename__ = "tasks"

  #Comlumns
  task_name: Mapped(str)
  id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  priority: Mapped(str)
  user_id: Mapped(int) = mapped_column(ForeignKey("user_account.id")) 

  def __repr__(self):
    return "Task Name: {task_name}, id: {id}, priority: {priority}"
