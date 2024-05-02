from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, String

from peterpy.database.models.base import Base

# from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    # name = Mapped[str] = mapped_column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    date_added = Column(DateTime(timezone=True), default=datetime.utcnow)

    # what does !r mean ?
    # https://stackoverflow.com/questions/1436703/difference-between-str-and-repr
    def __repr__(self) -> str:
        return f"Product(id={self.product_id!r}, name={self.name!r}, price={self.price!r}, date_added={self.date_added!r})"
