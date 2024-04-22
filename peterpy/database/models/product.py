from datetime import datetime
from uuid import UUID
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
)

# from sqlalchemy.orm import Mapped, mapped_column

from peterpy.database.models.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    # name = Mapped[str] = mapped_column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    date_added = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r}, price={self.price!r}, date_added={self.date_added!r})"
