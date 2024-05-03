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

    # thank you copilot

    #     The !r inside the curly braces tells Python to use the repr() function to convert the value to a string. The repr() function returns a string that represents a printable version of the object, which could be used to recreate the object using the eval() function. This is different from the str() function, which returns a string that is intended to be human-readable.

    # So, this line of code returns a string that looks something like this:

    # "Product(id=1, name='Product Name', price=9.99, date_added=datetime.datetime(2022, 1, 1, 0, 0))"

    # This string could be useful for debugging, as it gives a clear representation of the Product object. It might also be used when implementing the __repr__() method in the Product class, which is a special method in Python that is supposed to return a string representation of the object for debugging.
    def __repr__(self) -> str:
        # pylint: disable=line-too-long
        return f"Product(id={self.product_id!r}, name={self.name!r}, price={self.price!r}, date_added={self.date_added!r})"
