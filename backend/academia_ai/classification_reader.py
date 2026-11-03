import json
from pathlib import Path


class AcademiaClassificationReader:

    def __init__(self):
        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "classification_results.json"
        )

    def load(self):

        if not self.data_path.exists():
            return []

        with open(self.data_path, "r", encoding="utf-8") as file:
            records = json.load(file)

        return records

    def display(self):

        records = self.load()

        print("\nACADEMIA Classification History")
        print("=" * 55)

        if not records:
            print("No classification records found.")
            return

        for index, record in enumerate(records, start=1):

            print(f"\nRecord {index}")
            print("-" * 40)

            print(f"Word: {record['word']}")
            print(f"Category: {record['category']}")
            print(f"Part of Speech: {record['part_of_speech']}")
            print(f"Grammatical Role: {record['grammatical_role']}")
            print(f"Evidence: {record['evidence']}")
            print(f"Analyzed At: {record['analyzed_at']}")


if __name__ == "__main__":

    reader = AcademiaClassificationReader()
    reader.display()