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
    duration_minutes: int
    availability: str
    pet: PetInfo | None = None
    status: str = "pending"

    def set_priority(self, priority: int) -> None:
        self.priority = priority

    def mark_complete(self) -> None:
        self.status = "complete"


class Owner:
    def __init__(self, name: str, availability: str) -> None:
        self.name = name
        self.availability = availability
        self.pets: list[PetInfo] = []
        self.todos: list[ToDo] = []
        self.day_plans: list[DayPlan] = []

    def add_pet(self, pet: PetInfo) -> None:
        self.pets.append(pet)

    def add_todo(self, todo: ToDo) -> None:
        if todo.pet is not None and todo.pet not in self.pets:
            raise ValueError(
                f"Pet {todo.pet.name!r} is not registered with this owner"
            )
        self.todos.append(todo)

    def get_tasks_for_pet(self, pet: PetInfo) -> list[ToDo]:
        return [todo for todo in self.todos if todo.pet is pet]

    def get_all_pet_tasks(self) -> list[ToDo]:
        pet_set = set(self.pets)
        return [todo for todo in self.todos if todo.pet in pet_set]

    def generate_day_plan(self, plan_date: date) -> DayPlan:
        return Scheduler().build_plan(self, plan_date)


class DayPlan:
    def __init__(self, plan_date: date, owner: Owner) -> None:
        self.date = plan_date
        self.owner = owner

    @property
    def total_duration(self) -> int:
        return sum(todo.duration_minutes for todo in self.owner.todos)

    def sort_by_priority(self) -> None:
        self.owner.todos.sort(key=lambda t: t.priority)

    def display_schedule(self) -> None:
        pass


class Scheduler:
    def _get_tasks(self, owner: Owner) -> list[ToDo]:
        return [
            todo
            for todo in owner.todos
            if todo.pet in owner.pets or todo.pet is None
        ]

    def build_plan(self, owner: Owner, plan_date: date) -> DayPlan:
        tasks = self._get_tasks(owner)
        plan = DayPlan(plan_date, owner)
        if tasks:
            plan.sort_by_priority()
        owner.day_plans.append(plan)
        return plan
