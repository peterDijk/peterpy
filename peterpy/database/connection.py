from sqlalchemy import create_engine

connection_string = "mysql+mysqlconnector://root:root@mysql:3306/peterpy"

engine = create_engine(connection_string, echo=True)
