import json
from pathlib import Path
from datetime import datetime, timezone


class AcademiaLearningTaskTracker:

    VALID_STATUSES = {
        "Not Started",
        "In Progress",
        "Completed"
    }

    def __init__(self):
        base_path = Path(__file__).resolve().parent.parent / "data"

        self.recommendation_path = base_path / "learning_recommendations.json"
        self.status_path = base_path / "learning_task_status.json"

    def load_tasks(self):
        if not self.recommendation_path.exists():
            return []

        with open(self.recommendation_path, "r", encoding="utf-8") as file:
            sessions = json.load(file)

        unique_tasks = {}

        for session in sessions:
            for task in session.get("recommendations", []):
                unique_tasks[task["activity"]] = task

        return list(unique_tasks.values())

    def load_statuses(self):
        if not self.status_path.exists():
            return {}

        with open(self.status_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def update_status(self, task_name, status):
        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid task status.")

        statuses = self.load_statuses()

        statuses[task_name] = {
            "status": status,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        self.status_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.status_path, "w", encoding="utf-8") as file:
            json.dump(statuses, file, ensure_ascii=False, indent=4)

        return statuses[task_name]

    def display(self):
        tasks = self.load_tasks()
        statuses = self.load_statuses()

        print("\nACADEMIA Learning Task Tracker")
        print("=" * 55)

        for index, task in enumerate(tasks, start=1):
            name = task["activity"]
            status = statuses.get(name, {}).get("status", "Not Started")

            print(f"\n{index}. {name}")
            print("Task:", task["task"])
            print("Duration:", task["duration"])
            print("Status:", status)

        print("\nTotal unique tasks:", len(tasks))


if __name__ == "__main__":
    tracker = AcademiaLearningTaskTracker()
    tracker.display()
