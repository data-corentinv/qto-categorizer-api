from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Prediction(Base):
    """Schema db"""

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type_of_payment = Column(String)
    merchant_name = Column(String)
    description = Column(String)
    prediction = Column(String)
    model_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db(database_url: str):
    """Init db for traceability."""
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
