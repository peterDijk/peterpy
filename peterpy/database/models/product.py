from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column, DateTime, String

from peterpy.database.models.base import Base


# pylint: disable=too-few-public-methods
class Product(Base):
    __tablename__ = "products"

    product_id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(BigInteger, nullable=False)
    date_added = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return (
            f"Product(id={self.product_id!r}, name={self.name!r}, "
            "price={self.price!r}, date_added={self.date_added!r})"
        )
