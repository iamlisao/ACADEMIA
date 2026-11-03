from batch_classification_analyzer import (
    AcademiaBatchClassificationAnalyzer
)

from batch_classification_storage import (
    AcademiaBatchClassificationStorage
)


class AcademiaFullClassificationPipeline:

    def __init__(self):
        self.analyzer = AcademiaBatchClassificationAnalyzer()
        self.storage = AcademiaBatchClassificationStorage()

    def run(self, text):

        # Step 1: Analyze the input text
        results = self.analyzer.analyze(text)

        # Step 2: Save classification results
        saved_record = self.storage.save(results)

        # Step 3: Return analysis and storage information
        return {
            "total_words": len(results),
            "results": results,
            "saved_at": saved_record["analyzed_at"],
            "saved_file": str(self.storage.file_path)
        }


if __name__ == "__main__":

    pipeline = AcademiaFullClassificationPipeline()

    sample_text = """
    Researchers analyze evidence to evaluate different arguments.
    Scientists investigate complex problems and develop new methods.
    """

    result = pipeline.run(sample_text)

    print("\nACADEMIA Full Classification Pipeline")
    print("=" * 60)

    print(f"Total analyzed words: {result['total_words']}")

    print("\nClassification Results")
    print("-" * 60)

    for item in result["results"]:

        print(
            f"{item['word']} | "
            f"{item['category']} | "
            f"Review: {item['review_required']}"
        )

    print("\nStorage Information")
    print("-" * 60)

    print(f"Saved at: {result['saved_at']}")
    print(f"Saved file: {result['saved_file']}")

    print("\nACADEMIA Pipeline Completed!")