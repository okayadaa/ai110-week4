from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

WEEKDAYS = {0, 1, 2, 3, 4}
WEEKENDS = {5, 6}
ALL_DAYS = set(range(7))

DAY_PRESETS: dict[str, set[int]] = {
    "Weekdays (Mon–Fri)": WEEKDAYS,
    "Weekends (Sat–Sun)": WEEKENDS,
    "Every day": ALL_DAYS,
}


@dataclass
class AvailabilityWindow:
    days: set[int]
    start: time
    end: time


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
    recurring: bool = False

    @property
    def time(self) -> time:
        return parse_task_time(self.availability)

    def set_priority(self, priority: int) -> None:
        self.priority = priority

    def mark_complete(self) -> None:
        self.status = "complete"
        if self.recurring:
            self.status = "pending"


class AvailabilityError(ValueError):
    pass


class ScheduleConflictError(ValueError):
    pass


class Owner:
    def __init__(self, name: str, availability: AvailabilityWindow) -> None:
        self.name = name
        self.availability = availability
        self.pets: list[PetInfo] = []
        self.todos: list[ToDo] = []
        self.day_plans: list[DayPlan] = []

    def add_pet(self, pet: PetInfo) -> None:
        self.pets.append(pet)

    def add_todo(self, todo: ToDo, plan_date: date | None = None) -> None:
        if todo.pet is not None and todo.pet not in self.pets:
            raise ValueError(
                f"Pet {todo.pet.name!r} is not registered with this owner"
            )
        when = plan_date or date.today()
        conflicts = self.check_todo_availability(todo, when)
        if conflicts:
            raise AvailabilityError(conflicts[0])
        overlap = task_schedule_conflicts(self.todos + [todo], when)
        if overlap:
            raise ScheduleConflictError(overlap[0])
        self.todos.append(todo)

    def get_tasks_for_pet(self, pet: PetInfo) -> list[ToDo]:
        return [todo for todo in self.todos if todo.pet is pet]

    def get_all_pet_tasks(self) -> list[ToDo]:
        return [todo for todo in self.todos if todo.pet in self.pets]

    def check_todo_availability(self, todo: ToDo, plan_date: date) -> list[str]:
        return availability_conflicts(
            self.availability,
            plan_date,
            todo.availability,
            todo.duration_minutes,
            todo.task,
        )

    def generate_day_plan(self, plan_date: date) -> DayPlan:
        for todo in self.todos:
            conflicts = self.check_todo_availability(todo, plan_date)
            if conflicts:
                raise AvailabilityError(
                    f"Cannot build schedule: {conflicts[0]}"
                )
        overlap = task_schedule_conflicts(self.todos, plan_date)
        if overlap:
            raise ScheduleConflictError(
                f"Cannot build schedule: {overlap[0]}"
            )
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

    def sort_by_time(self) -> None:
        self.owner.todos.sort(key=lambda t: t.time)

    def display_schedule(self) -> None:
        pass


class Scheduler:
    def _get_tasks(self, owner: Owner) -> list[ToDo]:
        return [
            todo
            for todo in owner.todos
            if todo.pet in owner.pets or todo.pet is None
        ]

    @staticmethod
    def sort_by_time(tasks: list[ToDo]) -> list[ToDo]:
        return sorted(tasks, key=lambda t: t.time)

    @staticmethod
    def filter_tasks(
        tasks: list[ToDo],
        *,
        status: str | None = None,
        pet_name: str | None = None,
    ) -> list[ToDo]:
        filtered = tasks
        if status is not None:
            filtered = [todo for todo in filtered if todo.status == status]
        if pet_name is not None:
            filtered = [
                todo
                for todo in filtered
                if todo.pet is not None and todo.pet.name == pet_name
            ]
        return filtered

    def build_plan(self, owner: Owner, plan_date: date) -> DayPlan:
        tasks = self._get_tasks(owner)
        plan = DayPlan(plan_date, owner)
        if tasks:
            plan.sort_by_time()
        owner.day_plans.append(plan)
        return plan


def parse_task_time(time_str: str) -> time:
    text = time_str.strip()
    if not text:
        raise ValueError(f"Invalid time format: {time_str!r}")

    normalized = text.upper()
    for fmt in ("%I:%M %p", "%I:%M%p", "%H:%M"):
        for candidate in (text, normalized):
            try:
                return datetime.strptime(candidate, fmt).time()
            except ValueError:
                continue
    raise ValueError(f"Invalid time format: {time_str!r}")


def format_time(value: time) -> str:
    hour = value.hour % 12 or 12
    return f"{hour}:{value.minute:02d} {value.strftime('%p')}"


def describe_days(days: set[int]) -> str:
    if days == WEEKDAYS:
        return "weekdays"
    if days == WEEKENDS:
        return "weekends"
    if days == ALL_DAYS:
        return "every day"
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return ", ".join(names[d] for d in sorted(days))


def availability_conflicts(
    window: AvailabilityWindow,
    task_date: date,
    time_str: str,
    duration_minutes: int,
    task_name: str = "Task",
) -> list[str]:
    try:
        start_time = parse_task_time(time_str)
    except (ValueError, IndexError):
        return [
            f"{task_name}: could not parse time {time_str!r} "
            f"(use a time like 9:00 AM or 17:30)."
        ]

    conflicts: list[str] = []
    task_start = datetime.combine(task_date, start_time)
    task_end = task_start + timedelta(minutes=duration_minutes)
    window_label = (
        f"{format_time(window.start)}–{format_time(window.end)} "
        f"on {describe_days(window.days)}"
    )

    if task_date.weekday() not in window.days:
        conflicts.append(
            f"{task_name} is on {task_date.strftime('%A')}, "
            f"but you're only available {describe_days(window.days)}."
        )

    if start_time < window.start:
        conflicts.append(
            f"{task_name} at {format_time(start_time)} is before your window "
            f"({window_label})."
        )
    elif start_time > window.end:
        conflicts.append(
            f"{task_name} at {format_time(start_time)} is after your window "
            f"({window_label})."
        )
    elif task_end.time() > window.end:
        conflicts.append(
            f"{task_name} ends at {format_time(task_end.time())}, after your window "
            f"({format_time(window.end)})."
        )

    return conflicts


def _task_interval(todo: ToDo, plan_date: date) -> tuple[datetime, datetime]:
    start = datetime.combine(plan_date, todo.time)
    end = start + timedelta(minutes=todo.duration_minutes)
    return start, end


def task_schedule_conflicts(
    tasks: list[ToDo], plan_date: date
) -> list[str]:
    active = [todo for todo in tasks if todo.status != "complete"]
    conflicts: list[str] = []

    for index, first in enumerate(active):
        first_start, first_end = _task_interval(first, plan_date)
        for second in active[index + 1 :]:
            second_start, second_end = _task_interval(second, plan_date)
            if first_start < second_end and second_start < first_end:
                conflicts.append(
                    f"{first.task} ({format_time(first.time)}) overlaps with "
                    f"{second.task} ({format_time(second.time)})."
                )

    return conflicts
