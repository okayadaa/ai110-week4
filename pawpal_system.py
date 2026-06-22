from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class PetInfo:
    name: str
    age: int
    breed: str

    def get_pet_info(self) -> str:
        pass


@dataclass
class ToDo:
    task: str
    priority: int
    time: str
    availability: str

    def set_priority(self) -> None:
        pass


class Owner:
    def __init__(self, name: str, availability: str) -> None:
        self.name = name
        self.availability = availability
        self.pets: list[PetInfo] = []
        self.todos: list[ToDo] = []
        self.day_plans: list[DayPlan] = []

    def add_pet(self) -> None:
        pass


class DayPlan:
    def __init__(
        self,
        date: date,
        task_list: list[ToDo] | None = None,
        total_duration: int = 0,
    ) -> None:
        self.date = date
        self.task_list: list[ToDo] = task_list if task_list is not None else []
        self.total_duration = total_duration

    def display_schedule(self) -> None:
        pass

    def sort_by_priority(self) -> None:
        pass
