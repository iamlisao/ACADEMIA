import json
from pathlib import Path


class AcademiaRecommendationHistory:

    def __init__(self):
        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "learning_recommendations.json"
        )

    def load_history(self):
        if not self.data_path.exists():
            return []

        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def display(self):
        history = self.load_history()

        print("\nACADEMIA Recommendation History")
        print("=" * 55)

        if not history:
            print("No recommendation history found.")
            return

        for index, session in enumerate(history, start=1):
            print(f"\nSession {index}")
            print("Saved at:", session["saved_at"])

            for task in session["recommendations"]:
                print(
                    f"- {task['activity']} "
                    f"| {task['duration']}"
                )

        print("\nTotal sessions:", len(history))


if __name__ == "__main__":
    history = AcademiaRecommendationHistory()
    history.display()