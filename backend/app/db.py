from sqlmodel import create_engine, SQLModel, Session

class DBConnector():
    def __init__(self):
        self.sqlite_file_name = "database.db"
        self.sqlite_url = f"sqlite:///{self.sqlite_file_name}"

        self.connect_args = {"check_same_thread": False}
        self.engine = create_engine(self.sqlite_url, connect_args=self.connect_args)


    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)


    def get_session(self):
        with Session(self.engine) as session:
            yield session
    