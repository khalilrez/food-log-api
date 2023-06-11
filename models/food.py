from pydantic import BaseModel
from datetime import datetime
from typing import Any

from passlib.context import CryptContext

AVG_HUMAN_CALORIES_PER_DAY = 2250


class Food(BaseModel):
    id: int
    name: str
    serving_size: str
    kcal_per_serving: int
    protein_grams: float
    fibre_grams: float = 0


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


class User(BaseModel):
    id: int
    username: str
    password: str
    max_daily_calories: int = AVG_HUMAN_CALORIES_PER_DAY

    def __init__(self, **data):
        super().__init__(**data)
        self.password = get_password_hash(self.password)


class FoodEntry(BaseModel):
    id: int
    user: User
    food: Food
    date_added: datetime = datetime.now()
    number_servings: float

    @property
    def total_calories(self) -> float:
        return self.number_servings * self.food.kcal_per_serving


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
