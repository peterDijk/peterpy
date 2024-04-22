from sqlalchemy import create_engine

connection_string = "mysql+mysqlconnector://root:root@mysql:3306/peterpy"

engine = create_engine(connection_string, echo=False)


class DatabaseConnection:
    def __init__(self):

        connection_string = "mysql+mysqlconnector://root:root@mysql:3306/peterpy"

        engine = create_engine(connection_string, echo=True)
        self.connection = engine.connect()

    def execute(self, query):
        return self.connection.execute(query)

    def close(self):
        self.connection.close()
