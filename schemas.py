from pydantic import BaseModel


class Iris(BaseModel):
    sepal_l: float
    sepal_w: float
    petal_l: float
    petal_w: float