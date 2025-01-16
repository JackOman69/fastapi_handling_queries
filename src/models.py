from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Application(Base):
    __tablename__ = "applications_table"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    def __repr__(self) -> str:
        return f"Application(id={self.id})"