import logging

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from peterpy.config import config

connection_string = f"mysql+mysqlconnector://root:{config["MYSQL_ROOT_PASSWORD"]}@{config["MYSQL_HOST"]}:{config["MYSQL_TCP_PORT"]}/{config["MYSQL_DATABASE"]}"


class DatabaseConnection:
    def __init__(self):
        try:
            self._engine = create_engine(connection_string, echo=False)
            self.connection = self._engine.connect()
            logging.info("Connected to database")

        except Exception as e:
            print(f"Error connecting to database: {e}")

    def engine(self) -> Engine:
        return self._engine

    def close(self, exc_type, exc_val, exc_tb):
        logging.info("Closing database connection")
        self.connection.close()
        return False


class DatabaseSession:
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
