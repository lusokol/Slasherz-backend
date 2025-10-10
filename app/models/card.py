from sqlalchemy import Column, String, Integer, DateTime, Enum
from datetime import datetime
from app.database import Base
from app.models.enums import CardType, CardDimension, CardRarity

class Card(Base):
    __tablename__ = "cards"

    id = Column(String, primary_key=True, index=True)
    code = Column(String, nullable=False)
    image_name = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(Enum(CardType), nullable=False)
    dimension = Column(Enum(CardDimension), nullable=False)
    level = Column(Integer)
    score = Column(Integer)
    rarity = Column(Enum(CardRarity))
    last_updated = Column(DateTime, default=datetime.utcnow)
