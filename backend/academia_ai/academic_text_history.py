
import json
from pathlib import Path


class AcademiaAcademicTextHistory:

    def __init__(self):
        self.history_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "academic_text_analysis_history.json"
        )

    def load_history(self):
        if not self.history_path.exists():
            return []

        with open(self.history_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def display(self):
        history = self.load_history()

        print("\nACADEMIA Academic Text History")
        print("=" * 55)

        if not history:
            print("No analysis history found.")
            return

        for index, record in enumerate(history, start=1):
            results = record.get("vocabulary_analysis", [])

            review_count = sum(
                1 for item in results
                if item.get("review_required", False)
            )

            print(f"\nAnalysis {index}")
            print("ID:", record.get("analysis_id"))
            print("Date:", record.get("analyzed_at"))
            print("Total words:", record.get("total_words"))
            print("Vocabulary analyzed:", len(results))
            print("Words to review:", review_count)
            print("Original Text:")
            print(record.get("original_text", "").strip())

if __name__ == "__main__":
    history = AcademiaAcademicTextHistory()
    history.display()
