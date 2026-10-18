from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime


engine = create_engine("sqlite:///data/factory.db")

Base = declarative_base()


class Machine(Base):

    __tablename__ = "machines"

    id = Column(Integer, primary_key=True)

    machine_id = Column(String)

    temperature = Column(Float)

    vibration = Column(Float)

    pressure = Column(Float)

    rpm = Column(Float)

    health = Column(Float)

    status = Column(String)

    timestamp = Column(DateTime, default=datetime.now)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()


print("Database Ready")