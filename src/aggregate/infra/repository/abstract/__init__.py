"""
Абстрактные repositories
"""

from .base import BaseRepository
from .cubes import CubesRepository
from .items import ItemsRepository
from .products import ProductsRepository
from .tasks import TasksRepository

__all__ = [
    "CubesRepository",
    "ProductsRepository",
    "TasksRepository",
    "BaseRepository",
    "ItemsRepository",
]
