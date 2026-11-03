
import json
from pathlib import Path
from datetime import datetime, timezone


class AcademiaReviewLearningStorage:

    VALID_STATUSES = {
        "Not Started",
        "Learning",
        "Mastered"
    }

    def __init__(self):

        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "review_learning_status.json"
        )

    def load(self):

        if not self.data_path.exists():
            return {}

        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, records):

        self.data_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(self.data_path, "w", encoding="utf-8") as file:
            json.dump(
                records,
                file,
                ensure_ascii=False,
                indent=4
            )

    def update_status(self, word, status):

        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid learning status")

        records = self.load()

        normalized_word = word.lower().strip()

        records[normalized_word] = {
            "word": normalized_word,
            "status": status,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        self.save(records)

        return records[normalized_word]


if __name__ == "__main__":

    storage = AcademiaReviewLearningStorage()

    result = storage.update_status(
        word="scientific",
        status="Learning"
    )

    print("\nACADEMIA Review Learning Storage")
    print("=" * 55)
    print("Saved successfully!")
    print(result)
    print("\nFile location:")
    print(storage.data_path)
