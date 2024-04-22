from datetime import datetime
from uuid import UUID
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, ForeignKey, String

from peterpy.database.models.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    date_added = Column(DateTime(timezone=True), default=datetime.utcnow)
