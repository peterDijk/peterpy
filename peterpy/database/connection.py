import logging
from sqlalchemy import create_engine, Engine
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

    def __exit__(self):
        logging.info("Closing database connection")
        self.connection.close()
        return False


class DatabaseSession:
    def __init__(self):
        self.connection = DatabaseConnection()
        self.engine = self.connection.__enter__()

    def __enter__(self):
        self.session = Session(self.engine)
        return self.session

    def __exit__(self):
        logging.info("Closing database session")
        self.session.close()
        return False
