
from .document_classification_reader import (
    AcademiaDocumentClassificationReader
)


class AcademiaReviewWordAnalyzer:

    def __init__(self):
        self.reader = AcademiaDocumentClassificationReader()

    def get_review_words(self):

        records = self.reader.load()
        review_words = {}

        for record in records:
            for result in record.get("results", []):

                if result.get("review_required", False):

                    word = result.get("word", "").lower()

                    if word not in review_words:
                        review_words[word] = {
                            "word": word,
                            "category": result.get("category"),
                            "context": result.get("context"),
                            "confidence": result.get("confidence"),
                            "occurrences": 1
                        }
                    else:
                        review_words[word]["occurrences"] += 1

        return list(review_words.values())

    def prioritize_review_words(self):

        review_words = self.get_review_words()

        for item in review_words:

            confidence = item.get("confidence", 0)

            if confidence < 0.5:
                item["priority"] = "High"

            elif confidence < 0.8:
                item["priority"] = "Medium"

            else:
                item["priority"] = "Low"

        return sorted(
            review_words,
            key=lambda item: item["confidence"]
        )


if __name__ == "__main__":

    analyzer = AcademiaReviewWordAnalyzer()

    review_words = analyzer.prioritize_review_words()

    print("\nACADEMIA Review Word Analysis")
    print("=" * 55)

    for item in review_words:

        print(
            f"{item['word']} | "
            f"{item['category']} | "
            f"Priority: {item['priority']} | "
            f"Confidence: {item['confidence']} | "
            f"Occurrences: {item['occurrences']} | "
            f"Context: {item['context']}"
        )

    print("\nUnique review words:", len(review_words))
