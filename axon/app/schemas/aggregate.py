from pydantic import BaseModel


class Aggregation(BaseModel):
    task_id: int
    product_code: str
