from app.api.task import router as router_task
from app.api.product import router as router_product

all_routers = [
    router_task,
    router_product
]
