from app.api.product import router as router_product
from app.api.task import router as router_task

all_routers = [
    router_task,
    router_product
]
