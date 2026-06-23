from datetime import date, time

from pawpal_system import (
    AvailabilityWindow,
    Owner,
    PetInfo,
    Scheduler,
    ToDo,
    WEEKDAYS,
    format_time,
)


def print_todays_schedule(owner: Owner) -> None:
    plan = owner.generate_day_plan(date.today())

    print("Today's Schedule")
    print(f"Date: {plan.date}")
    print(f"Owner: {owner.name}")
    print("-" * 60)

    for todo in Scheduler.sort_by_time(owner.todos):
        pet_name = todo.pet.name if todo.pet else "—"
        print(
            f"{format_time(todo.time):>10}  |  {pet_name:<12}  |  "
            f"Priority {todo.priority}  |  {todo.task} ({todo.duration_minutes} min)"
        )

    print("-" * 60)
    print(f"Total duration: {plan.total_duration} minutes")


def main() -> None:
    owner = Owner(
        "Alex",
        AvailabilityWindow(WEEKDAYS, time(9, 0), time(18, 0)),
    )

    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    luna = PetInfo("Luna", 5, "Siamese")
    owner.add_pet(buddy)
    owner.add_pet(luna)

    owner.add_todo(ToDo("Morning walk", 3, 30, "09:00", buddy))
    owner.add_todo(ToDo("Feed breakfast", 2, 15, "09:30", buddy))
    owner.add_todo(ToDo("Play session", 1, 20, "12:00", luna))
    owner.add_todo(ToDo("Evening grooming", 2, 25, "17:00", luna))

    print_todays_schedule(owner)


if __name__ == "__main__":
    main()
