
import json
from pathlib import Path
from datetime import datetime, timezone


class AcademiaStudentLearningAnalytics:

    def __init__(self):
        self.data_dir = Path(__file__).resolve().parent.parent / "data"

        self.document_path = (
            self.data_dir / "document_classification_results.json"
        )
        self.status_path = (
            self.data_dir / "review_learning_status.json"
        )
        self.analytics_path = (
            self.data_dir / "student_learning_analytics.json"
        )

    def load_json(self, path):
        if not path.exists():
            return []

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def analyze(self):
        documents = self.load_json(self.document_path)
        learning_status = self.load_json(self.status_path)

        results = []

        for document in documents:
            results.extend(document.get("results", []))

        categories = {
            "Academic Vocabulary": 0,
            "General Vocabulary": 0,
            "Technical Vocabulary": 0,
            "Needs Review": 0
        }

        for item in results:
            category = item.get("category")
            if category in categories:
                categories[category] += 1

        review_words = {
            item.get("word", "").lower()
            for item in results
            if item.get("review_required", False)
        }

        statuses = {
            "Not Started": 0,
            "Learning": 0,
            "Mastered": 0
        }

        for word in review_words:
            status = learning_status.get(
                word, {}
            ).get("status", "Not Started")

            if status in statuses:
                statuses[status] += 1

        return {
            "total_classified_words": len(results),
            "category_counts": categories,
            "unique_review_words": len(review_words),
            "learning_status": statuses
        }

    def save(self, report):
        self.data_dir.mkdir(parents=True, exist_ok=True)

        history = self.load_json(self.analytics_path)

        record = {
            "report": report,
            "saved_at": datetime.now(timezone.utc).isoformat()
        }

        history.append(record)

        with open(self.analytics_path, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)

        return record

    def display(self):
        report = self.analyze()
        self.save(report)

        print("\nACADEMIA Student Learning Analytics")
        print("=" * 55)
        print("Total classified words:", report["total_classified_words"])

        print("\nVocabulary Categories")
        for category, count in report["category_counts"].items():
            print(f"{category}: {count}")

        print("\nReview Word Progress")
        print("Unique review words:", report["unique_review_words"])

        for status, count in report["learning_status"].items():
            print(f"{status}: {count}")

        print("\nAnalytics saved:", self.analytics_path)


if __name__ == "__main__":
    analytics = AcademiaStudentLearningAnalytics()
    analytics.display()
