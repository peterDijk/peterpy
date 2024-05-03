import logging

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

connection_string = "mysql+mysqlconnector://root:root@localhost:3306/peterpy"


class DatabaseConnection:
    def __init__(self):
        try:
            self.engine = create_engine(connection_string, echo=False)
            self.connection = self.engine.connect()
            logging.info("Connected to database")

        except Exception as e:
            print(f"Error connecting to database: {e}")

    def __enter__(self) -> Engine:
        return self.engine

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info("Closing database connection")
        self.connection.close()
        return False


class DatabaseSession:
    def __init__(self):
        self.connection = DatabaseConnection()
        self.engine = self.connection.__enter__()

    # 'with' statement calls __enter__ and __exit__ methods
    # for the object. The __enter__ method is called when
    # the 'with' statement is executed, and the __exit__
    # method is called when the 'with' statement is exited.
    # The __exit__ method is called even if an exception
    # is raised in the 'with' block.

    # https://docs.python.org/3/reference/compound_stmts.html#with
    def __enter__(self):
        logging.info("Opening database session")
        self.session = Session(self.engine)
        return self.session

    # exc_type, exc_val, exc_tb are used to handle exceptions
    # raised in the 'with' block. If the __exit__ method returns
    # True, the exception is suppressed. If it returns False,
    # the exception is propagated.
    # *args is used to accept any number of positional arguments
    # and is a tuple of all the positional arguments passed to
    # the __exit__ method.
    def __exit__(self, exc_type, exc_val, exc_tb, *args):
        logging.info("Closing database session")
        self.session.close()
        self.connection.__exit__(exc_type, exc_val, exc_tb)
        return False
