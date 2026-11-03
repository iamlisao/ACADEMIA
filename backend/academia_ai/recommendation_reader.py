
import json
from pathlib import Path


class AcademiaRecommendationReader:

    def __init__(self):
        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "learning_recommendations.json"
        )

    def load(self):
        if not self.data_path.exists():
            return []

        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def display(self):
        records = self.load()

        print("\nACADEMIA Learning Recommendation History")
        print("=" * 55)

        if not records:
            print("No recommendations found.")
            return

        for index, record in enumerate(records, start=1):
            print(f"\nSession {index}")
            print("Saved at:", record["saved_at"])

            for item in record["recommendations"]:
                print(f'\nActivity: {item["activity"]}')
                print(f'Task: {item["task"]}')
                print(f'Duration: {item["duration"]}')

        print("\nTotal sessions:", len(records))


if __name__ == "__main__":
    reader = AcademiaRecommendationReader()
    reader.display()
