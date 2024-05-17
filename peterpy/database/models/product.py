from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, String

from peterpy.database.models.base import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(BigInteger, nullable=False)
    date_added = Column(DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self) -> str:
        # pylint: disable=line-too-long
        return f"Product(id={self.product_id!r}, name={self.name!r}, price={self.price!r}, date_added={self.date_added!r})"
