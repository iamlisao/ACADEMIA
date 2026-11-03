
from .review_word_analyzer import AcademiaReviewWordAnalyzer
from .review_learning_storage import AcademiaReviewLearningStorage


class AcademiaReviewLearningDashboard:

    def __init__(self):
        self.analyzer = AcademiaReviewWordAnalyzer()
        self.storage = AcademiaReviewLearningStorage()

    def display(self):
        review_words = self.analyzer.get_review_words()
        learning_records = self.storage.load()

        unique_words = {}

        for item in review_words:
            word = item["word"].lower()
            unique_words[word] = item

        print("\nACADEMIA Review Learning Dashboard")
        print("=" * 65)

        for word, item in unique_words.items():
            record = learning_records.get(word, {})
            status = record.get("status", "Not Started")
            confidence = item.get("confidence", 0)

            priority = (
                "High" if confidence < 0.5
                else "Medium" if confidence < 0.8
                else "Low"
            )

            print(
                f"{word} | Priority: {priority} | "
                f"Status: {status}"
            )

        print("\nTotal review words:", len(unique_words))


if __name__ == "__main__":
    dashboard = AcademiaReviewLearningDashboard()
    dashboard.display()
