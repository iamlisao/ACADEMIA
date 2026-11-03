
from collections import Counter


class AcademiaDocumentAnalysisSummary:

    def summarize(self, results):

        categories = [
            item.get("category", "Unknown")
            for item in results
        ]

        counts = Counter(categories)

        total_words = len(results)

        review_count = sum(
            1 for item in results
            if item.get("review_required", False)
        )

        summary = {
            "total_words": total_words,
            "academic_vocabulary": counts.get(
                "Academic Vocabulary", 0
            ),
            "general_vocabulary": counts.get(
                "General Vocabulary", 0
            ),
            "technical_vocabulary": counts.get(
                "Technical Vocabulary", 0
            ),
            "needs_review": counts.get(
                "Needs Review", 0
            ),
            "review_count": review_count
        }

        return summary


if __name__ == "__main__":

    sample_results = [
        {"category": "Academic Vocabulary", "review_required": False},
        {"category": "Academic Vocabulary", "review_required": False},
        {"category": "General Vocabulary", "review_required": False},
        {"category": "Technical Vocabulary", "review_required": False},
        {"category": "Needs Review", "review_required": True}
    ]

    analyzer = AcademiaDocumentAnalysisSummary()

    summary = analyzer.summarize(sample_results)

    print("\nACADEMIA Document Analysis Summary")
    print("=" * 50)

    for key, value in summary.items():
        print(f"{key}: {value}")
