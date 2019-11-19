from sqlalchemy import create_engine


class Engine:
    engine = create_engine(
        "postgresql://postgres:@localhost:3000/kronika")

    def startEngine(self):
        self.engine.connect()
