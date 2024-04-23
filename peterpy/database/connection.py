import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


connection_string = "mysql+mysqlconnector://root:root@mysql:3306/peterpy"

engine = create_engine(connection_string, echo=False)


class DatabaseConnection:
    def __enter__(self):

        connection_string = "mysql+mysqlconnector://root:root@mysql:3306/peterpy"

        try:
            self.engine = create_engine(connection_string, echo=True)
            self.connection = engine.connect()
            logging.info("Connected to database")

            return self.connection

        except Exception as e:
            print(f"Error connecting to database: {e}")


class DatabaseSession:
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = Session(engine)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        return False
