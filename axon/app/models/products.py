from app.db.db import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ProductTable(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_code = Column(String, unique=True, nullable=False)
    is_aggregated = Column(Boolean, default=False)
    aggregated_at = Column(DateTime)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    tasks = relationship("TaskTable", back_populates='products')
