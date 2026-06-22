from pawpal_system import Owner, PetInfo, ToDo


def test_mark_complete_changes_task_status():
    todo = ToDo("Morning walk", 3, 30, "08:00")

    assert todo.status == "pending"

    todo.mark_complete()

    assert todo.status == "complete"


def test_adding_task_increases_pet_task_count():
    owner = Owner("Alex", "weekdays 9am–6pm")
    buddy = PetInfo("Buddy", 3, "Golden Retriever")
    owner.add_pet(buddy)

    assert len(owner.get_tasks_for_pet(buddy)) == 0

    owner.add_todo(ToDo("Morning walk", 3, 30, "08:00", buddy))
    assert len(owner.get_tasks_for_pet(buddy)) == 1

    owner.add_todo(ToDo("Feed breakfast", 2, 15, "08:30", buddy))
    assert len(owner.get_tasks_for_pet(buddy)) == 2
