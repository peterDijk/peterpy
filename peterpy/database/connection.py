import logging

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session


class DatabaseConnection:
    def __init__(self, connection_string: str):
        self._engine = create_engine(connection_string, echo=False)
        self.connection = self._engine.connect()
        logging.info("Connected to database")

    def engine(self) -> Engine:
        return self._engine

    def close(self):
        logging.info("Closing database connection")
        self.connection.close()
        return False


class DatabaseSession:
    session: Session

    def __init__(self, engine: Engine):
        self.engine = engine

    def __enter__(self):
        logging.info("Opening database session")
        self.session = Session(self.engine)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb, *args):
        logging.info("Closing database session")
        self.session.close()
        return False
