import random
import uuid
from datetime import date, datetime, timezone
from typing import Optional

from shared_kernel.infra.uow.base import UnitOfWork

from aggregate.domain.entity import Cube, Product, Task

num = random.randint(1000, 99999999)


def make_task(
        status_closed: bool,
        shift_task_representation: str,
        line: str,
        shift: str,
        brigade: str,
        batch_number: int,
        batch_date: date,
        nomenclature: str,
        code_ekn: str,
        identifier_rc: str,
        shift_start_time: datetime,
        shift_end_time: datetime,
        closed_at: bool,

) -> Task:
    task = Task(
        id=uuid.uuid4(),
        status_closed=status_closed,
        shift_task_representation=shift_task_representation,
        line=line,
        shift=shift,
        brigade=brigade,
        batch_number=batch_number,
        batch_date=batch_date,
        nomenclature=nomenclature,
        code_ekn=code_ekn,
        identifier_rc=identifier_rc,
        shift_start_time=shift_start_time,
        shift_end_time=shift_end_time,
        closed_at=closed_at,
        products=[],
        cubes=[]
    )
    return task


async def add_task(
        uow: UnitOfWork,
        status_closed: bool = False,
        shift_task_representation: str = f"Создание задания {num}",
        line: str = f"Линия {num}",
        shift: str = f"Смена {num}",
        brigade: str = f"Бригада {num}",
        batch_number: int = num,
        batch_date: date = date.today(),
        nomenclature: str = f"№ {num}",
        code_ekn: str = "654651",
        identifier_rc: str = "6553661",
        shift_start_time: datetime = datetime.now(timezone.utc),
        shift_end_time: datetime = datetime.now(timezone.utc),
        closed_at: Optional[bool] = None
) -> Task:
    async with uow:
        task = make_task(
            status_closed,
            shift_task_representation,
            line,
            shift,
            brigade,
            batch_number,
            batch_date,
            nomenclature,
            code_ekn,
            identifier_rc,
            shift_start_time,
            shift_end_time,
            closed_at,
        )
        await uow.tasks.create(task)
        await uow.commit()
        return task


def make_cube(
        task_id: uuid.UUID,
        product_code: str,
        is_aggregated: Optional[bool],
        aggregated_at: Optional[datetime],
) -> Cube:
    cube = Cube(
        id=uuid.uuid4(),
        product_code=product_code,
        is_aggregated=is_aggregated,
        aggregated_at=aggregated_at,
        task_id=task_id
    )
    return cube


async def add_cube(
        uow: UnitOfWork,
        task: Task,
        product_code: str = f'{num}',
        is_aggregated: Optional[bool] = None,
        aggregated_at: Optional[datetime] = None,
) -> Cube:
    async with uow:
        cube = make_cube(
            task.id,
            product_code,
            is_aggregated,
            aggregated_at,
        )
        await uow.cubes.create(cube)
        await uow.commit()
        return cube


def make_product(
        task_id: uuid.UUID,
        product_code: str,
        is_aggregated: Optional[bool],
        aggregated_at: Optional[datetime],
) -> Product:
    product = Product(
        id=uuid.uuid4(),
        product_code=product_code,
        is_aggregated=is_aggregated,
        aggregated_at=aggregated_at,
        task_id=task_id
    )
    return product


async def add_product(
        uow: UnitOfWork,
        task: Task,
        product_code: str = f'{num}',
        is_aggregated: Optional[bool] = None,
        aggregated_at: Optional[datetime] = None,
) -> Product:
    async with uow:
        product = make_product(
            task.id,
            product_code,
            is_aggregated,
            aggregated_at,
        )
        await uow.products.create(product)
        await uow.commit()
        return product
