from aggregate.presentation.rest.cubes import router as cube
from aggregate.presentation.rest.products import router as product
from aggregate.presentation.rest.tasks import router as task

all_routers = [task, product, cube]
