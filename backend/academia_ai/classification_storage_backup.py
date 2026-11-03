
import json
from pathlib import Path
from datetime import datetime, timezone


class AcademiaClassificationStorage:

    def __init__(self):
        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "classification_results.json"
        )

    def save(self, result):

        self.data_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if self.data_path.exists():
            with open(self.data_path, "r", encoding="utf-8") as file:
                records = json.load(file)
        else:
            records = []

        record = {
            **result,
            "analyzed_at": datetime.now(timezone.utc).isoformat()
        }

        records.append(record)

        with open(self.data_path, "w", encoding="utf-8") as file:
            json.dump(
                records,
                file,
                ensure_ascii=False,
                indent=4
            )

        return record


if __name__ == "__main__":

    storage = AcademiaClassificationStorage()

    sample_result = {
        "word": "support",
        "part_of_speech": "VERB",
        "grammatical_role": "ROOT",
        "category": "Academic Vocabulary",
        "evidence": [
            "Matched academic context clue"
        ]
    }

    saved_record = storage.save(sample_result)

    print("\nACADEMIA Classification Storage")
    print("=" * 50)
    print("Saved successfully!")
    print(saved_record)
    print(f"\nFile location: {storage.data_path}")
