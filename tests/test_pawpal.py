from datetime import date, time

import pytest

from pawpal_system import (
    AvailabilityError,
    AvailabilityWindow,
    Owner,
    PetInfo,
    ScheduleConflictError,
    Scheduler,
    ToDo,
    WEEKDAYS,
    availability_conflicts,
    task_schedule_conflicts,
)


def _weekday_availability() -> AvailabilityWindow:
    return AvailabilityWindow(WEEKDAYS, time(9, 0), time(18, 0))


def test_mark_complete_changes_task_status():
    todo = ToDo("Morning walk", 3, 30, "08:00")

    assert todo.status == "pending"

    todo.mark_complete()

    assert todo.status == "complete"


def test_adding_task_increases_pet_task_count():
    owner = Owner("Alex", _weekday_availability())
    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    owner.add_pet(buddy)

    assert len(owner.get_tasks_for_pet(buddy)) == 0

    owner.add_todo(ToDo("Morning walk", 3, 30, "10:00", buddy))
    assert len(owner.get_tasks_for_pet(buddy)) == 1

    owner.add_todo(ToDo("Feed breakfast", 2, 15, "11:00", buddy))
    assert len(owner.get_tasks_for_pet(buddy)) == 2


def test_add_todo_blocks_outside_availability():
    owner = Owner("Alex", _weekday_availability())
    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    owner.add_pet(buddy)

    with pytest.raises(AvailabilityError, match="before your window"):
        owner.add_todo(ToDo("Morning walk", 3, 30, "08:00", buddy))

    assert len(owner.todos) == 0


def test_generate_day_plan_blocks_when_task_conflicts():
    owner = Owner("Alex", _weekday_availability())
    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    owner.add_pet(buddy)
    owner.todos.append(ToDo("Morning walk", 3, 30, "08:00", buddy))

    with pytest.raises(AvailabilityError, match="Cannot build schedule"):
        owner.generate_day_plan(date(2026, 6, 22))


def test_availability_conflict_before_window():
    window = _weekday_availability()
    conflicts = availability_conflicts(
        window, date(2026, 6, 22), "08:00", 30, "Morning walk"
    )
    assert any("before your window" in message for message in conflicts)


def test_availability_conflict_after_window():
    window = _weekday_availability()
    conflicts = availability_conflicts(
        window, date(2026, 6, 22), "18:00", 25, "Evening grooming"
    )
    assert any("after your window" in message for message in conflicts)


def test_availability_no_conflict_inside_window():
    window = _weekday_availability()
    conflicts = availability_conflicts(
        window, date(2026, 6, 22), "12:00", 20, "Play session"
    )
    assert conflicts == []


def test_sort_by_time_orders_tasks_chronologically():
    owner = Owner("Alex", _weekday_availability())
    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    owner.add_pet(buddy)
    owner.add_todo(ToDo("Afternoon play", 1, 20, "14:00", buddy))
    owner.add_todo(ToDo("Morning walk", 3, 30, "09:00", buddy))
    owner.add_todo(ToDo("Lunch feeding", 2, 15, "12:00", buddy))

    sorted_tasks = Scheduler.sort_by_time(owner.todos)

    assert [todo.task for todo in sorted_tasks] == [
        "Morning walk",
        "Lunch feeding",
        "Afternoon play",
    ]


def test_filter_tasks_by_status():
    owner = Owner("Alex", _weekday_availability())
    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    owner.add_pet(buddy)
    pending = ToDo("Morning walk", 3, 30, "10:00", buddy)
    done = ToDo("Feed breakfast", 2, 15, "11:00", buddy)
    done.mark_complete()
    owner.todos.extend([pending, done])

    pending_tasks = Scheduler.filter_tasks(owner.todos, status="pending")
    complete_tasks = Scheduler.filter_tasks(owner.todos, status="complete")

    assert [todo.task for todo in pending_tasks] == ["Morning walk"]
    assert [todo.task for todo in complete_tasks] == ["Feed breakfast"]


def test_filter_tasks_by_pet_name():
    owner = Owner("Alex", _weekday_availability())
    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    luna = PetInfo("Luna", 5, "Siamese")
    owner.add_pet(buddy)
    owner.add_pet(luna)
    owner.add_todo(ToDo("Morning walk", 3, 30, "10:00", buddy))
    owner.add_todo(ToDo("Play session", 1, 20, "12:00", luna))

    buddy_tasks = Scheduler.filter_tasks(owner.todos, pet_name="Buddy")

    assert len(buddy_tasks) == 1
    assert buddy_tasks[0].task == "Morning walk"


def test_recurring_task_resets_after_checkoff():
    todo = ToDo("Morning walk", 3, 30, "09:00", recurring=True)

    todo.mark_complete()

    assert todo.status == "pending"


def test_non_recurring_task_stays_complete():
    todo = ToDo("One-time vet visit", 3, 60, "15:00")

    todo.mark_complete()

    assert todo.status == "complete"


def test_task_schedule_conflicts_detects_overlap():
    owner = Owner("Alex", _weekday_availability())
    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    walk = ToDo("Morning walk", 3, 30, "10:00", buddy)
    grooming = ToDo("Grooming", 2, 30, "10:15", buddy)

    conflicts = task_schedule_conflicts([walk, grooming], date(2026, 6, 22))

    assert len(conflicts) == 1
    assert "overlaps with" in conflicts[0]


def test_add_todo_blocks_overlapping_tasks():
    owner = Owner("Alex", _weekday_availability())
    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    owner.add_pet(buddy)
    owner.add_todo(ToDo("Morning walk", 3, 30, "10:00", buddy))

    with pytest.raises(ScheduleConflictError, match="overlaps with"):
        owner.add_todo(ToDo("Grooming", 2, 30, "10:15", buddy))

    assert len(owner.todos) == 1


def test_generate_day_plan_sorts_by_time():
    owner = Owner("Alex", _weekday_availability())
    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    owner.add_pet(buddy)
    owner.add_todo(ToDo("Afternoon play", 1, 20, "14:00", buddy))
    owner.add_todo(ToDo("Morning walk", 3, 30, "09:00", buddy))

    owner.generate_day_plan(date(2026, 6, 22))

    assert [todo.task for todo in owner.todos] == ["Morning walk", "Afternoon play"]
