import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared_kernel.infra.db.db import Base


class BaseTable:
    id: Mapped[PgUUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_code: Mapped[str] = mapped_column(unique=True)
    is_aggregated: Mapped[bool] = mapped_column(default=False)
    aggregated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))


class CubesTable(BaseTable, Base):
    __tablename__ = "cubes"

    task: Mapped["TaskTable"] = relationship(back_populates="cubes")


class ProductTable(BaseTable, Base):
    __tablename__ = "products"

    task: Mapped["TaskTable"] = relationship(back_populates="products")


class TaskTable(Base):
    __tablename__ = "tasks"

    id: Mapped[PgUUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    status_closed: Mapped[bool]
    shift_task_representation: Mapped[str]
    line: Mapped[str]
    shift: Mapped[str]
    brigade: Mapped[str]
    batch_number: Mapped[int]
    batch_date: Mapped[date] = mapped_column(Date)
    nomenclature: Mapped[str]
    code_ekn: Mapped[str]
    identifier_rc: Mapped[str]
    shift_start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    shift_end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    products: Mapped[list[ProductTable]] = relationship(back_populates="task")
    cubes: Mapped[list[CubesTable]] = relationship(back_populates="task")

    __table_args__ = (
        UniqueConstraint(
            "batch_number", "batch_date", name="_unique_batch_number_date"
        ),
    )
