
import json
from pathlib import Path


class AcademiaDocumentClassificationReader:

    def __init__(self):
        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "document_classification_results.json"
        )

    def load(self):

        if not self.data_path.exists():
            return []

        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def display(self):

        records = self.load()

        print("\nACADEMIA Document Analysis History")
        print("=" * 55)

        if not records:
            print("No analysis history found.")
            return

        for index, record in enumerate(records, start=1):

            print(f"\nAnalysis {index}")
            print("-" * 45)
            print("Analysis ID:", record.get("analysis_id", "N/A"))
            print("Original Text:", record.get("original_text", "N/A"))
            print("Total Words:", record.get("total_words", 0))
            print("Review Required:", record.get("review_count", 0))

            for result in record.get("results", []):

                print(
                    f"{result.get('word', 'N/A')} | "
                    f"{result.get('category', 'N/A')} | "
                    f"Confidence: {result.get('confidence', 'N/A')} | "
                    f"Review: {result.get('review_required', 'N/A')}"
                )


if __name__ == "__main__":

    reader = AcademiaDocumentClassificationReader()
    reader.display()
