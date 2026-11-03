import json
from pathlib import Path
from datetime import datetime, timezone


class AcademiaBatchClassificationStorage:

    def __init__(self):
        self.file_path = (
            Path(__file__).parent.parent
            / "data"
            / "batch_classification_results.json"
        )

    def save(self, results):

        # Create the data folder if it does not exist
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Load existing records
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as file:
                records = json.load(file)
        else:
            records = []

        # Create a new analysis record
        new_record = {
            "analyzed_at": datetime.now(
                timezone.utc
            ).isoformat(),

            "total_words": len(results),

            "results": results
        }

        records.append(new_record)

        # Save all records
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                records,
                file,
                ensure_ascii=False,
                indent=4
            )

        return new_record


if __name__ == "__main__":

    sample_results = [
        {
            "word": "analyze",
            "part_of_speech": "VERB",
            "grammatical_role": "ROOT",
            "context": "Students analyze evidence",
            "category": "Academic Vocabulary",
            "classification_source": "academic_word_list",
            "evidence": [
                "Matched academic vocabulary list"
            ],
            "review_required": False
        },
        {
            "word": "beautiful",
            "part_of_speech": "ADJ",
            "grammatical_role": "amod",
            "context": "a beautiful day",
            "category": "Needs Review",
            "classification_source": "no_matching_rule",
            "evidence": [
                "No matching classification clues found"
            ],
            "review_required": True
        }
    ]

    storage = AcademiaBatchClassificationStorage()

    saved_record = storage.save(sample_results)

    print("\nACADEMIA Batch Classification Storage")
    print("=" * 55)
    print("Saved successfully!")
    print(f"Total words: {saved_record['total_words']}")
    print(f"File location: {storage.file_path}")