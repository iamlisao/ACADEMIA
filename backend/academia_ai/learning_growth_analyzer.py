
import json
from pathlib import Path


class AcademiaLearningGrowthAnalyzer:

    def __init__(self):
        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "student_learning_analytics.json"
        )

    def analyze(self):
        if not self.data_path.exists():
            print("No analytics history found.")
            return

        with open(self.data_path, "r", encoding="utf-8") as file:
            history = json.load(file)

        print("\nACADEMIA Learning Growth Analysis")
        print("=" * 55)

        if len(history) < 2:
            print("At least two analytics records are needed.")
            print("Current records:", len(history))
            return

        previous = history[-2]["report"]
        current = history[-1]["report"]

        print("\nPrevious Analysis")
        print("Classified words:",
              previous["total_classified_words"])
        print("Review words:",
              previous["unique_review_words"])

        print("\nLatest Analysis")
        print("Classified words:",
              current["total_classified_words"])
        print("Review words:",
              current["unique_review_words"])

        print("\nChanges")
        print(
            "Classified words:",
            current["total_classified_words"]
            - previous["total_classified_words"]
        )
        print(
            "Review words:",
            current["unique_review_words"]
            - previous["unique_review_words"]
        )


if __name__ == "__main__":
    analyzer = AcademiaLearningGrowthAnalyzer()
    analyzer.analyze()
