
from .learning_task_tracker import AcademiaLearningTaskTracker


class AcademiaLearningTaskUpdater:

    def __init__(self):
        self.tracker = AcademiaLearningTaskTracker()

    def run(self):
        tasks = self.tracker.load_tasks()

        print("\nACADEMIA Learning Task Updater")
        print("=" * 55)

        if not tasks:
            print("No learning tasks found.")
            return

        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task['activity']}")

        try:
            selection = int(input("\nSelect task number: "))
            if selection < 1 or selection > len(tasks):
                print("Invalid selection.")
                return
        except ValueError:
            print("Please enter a number.")
            return

        task_name = tasks[selection - 1]["activity"]

        print("\n1. Not Started")
        print("2. In Progress")
        print("3. Completed")

        status_options = {
            "1": "Not Started",
            "2": "In Progress",
            "3": "Completed"
        }

        choice = input("\nSelect status: ").strip()

        if choice not in status_options:
            print("Invalid selection.")
            return

        result = self.tracker.update_status(
            task_name,
            status_options[choice]
        )

        print("\nTask updated successfully!")
        print(result)


if __name__ == "__main__":
    updater = AcademiaLearningTaskUpdater()
    updater.run()
