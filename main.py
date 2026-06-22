from datetime import date

from pawpal_system import Owner, PetInfo, ToDo


def print_todays_schedule(owner: Owner) -> None:
    plan = owner.generate_day_plan(date.today())

    print("Today's Schedule")
    print(f"Date: {plan.date}")
    print(f"Owner: {owner.name}")
    print("-" * 60)

    for todo in owner.todos:
        pet_name = todo.pet.name if todo.pet else "—"
        print(
            f"{todo.availability:>8}  |  {pet_name:<12}  |  "
            f"Priority {todo.priority}  |  {todo.task} ({todo.duration_minutes} min)"
        )

    print("-" * 60)
    print(f"Total duration: {plan.total_duration} minutes")


def main() -> None:
    owner = Owner("Alex", "weekdays 9am–6pm")

    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    luna = PetInfo("Luna", 5, "Siamese")
    owner.add_pet(buddy)
    owner.add_pet(luna)

    owner.add_todo(ToDo("Morning walk", 3, 30, "08:00", buddy))
    owner.add_todo(ToDo("Feed breakfast", 2, 15, "08:30", buddy))
    owner.add_todo(ToDo("Play session", 1, 20, "12:00", luna))
    owner.add_todo(ToDo("Evening grooming", 2, 25, "18:00", luna))

    print_todays_schedule(owner)


if __name__ == "__main__":
    main()
