from app.db.db import Base
from sqlalchemy import (Boolean, Column, Date, DateTime, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship


class TaskTable(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    status_closed = Column(Boolean, nullable=False)
    shift_task_representation = Column(String, nullable=False)
    line = Column(String, nullable=False)
    shift = Column(String, nullable=False)
    brigade = Column(String, nullable=False)
    batch_number = Column(Integer, nullable=False)
    batch_date = Column(Date, nullable=False)
    nomenclature = Column(String, nullable=False)
    code_ekn = Column(String, nullable=False)
    identifier_rc = Column(String, nullable=False)
    shift_start_time = Column(DateTime(timezone=True), nullable=False)
    shift_end_time = Column(DateTime(timezone=True), nullable=False)
    closed_at = Column(DateTime(timezone=True))
    products = relationship("ProductTable", back_populates='tasks')

    __table_args__ = (
        UniqueConstraint(
            'batch_number', 'batch_date', name='_unique_batch_number_date'
        ),
    )
