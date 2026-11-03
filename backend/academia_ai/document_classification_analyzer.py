
import json
from pathlib import Path

from .context_analyzer import AcademiaContextAnalyzer
from .classification_evaluator import AcademiaClassificationEvaluator
from .document_classification_storage import (
    AcademiaDocumentClassificationStorage
)


class AcademiaDocumentClassificationAnalyzer:

    def __init__(self):
        self.context_analyzer = AcademiaContextAnalyzer()
        self.evaluator = AcademiaClassificationEvaluator()
        self.storage = AcademiaDocumentClassificationStorage()

        vocabulary_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "academic_vocabulary.json"
        )

        with open(vocabulary_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.registered_vocabulary = {
            item["word"].lower(): item
            for item in data["vocabulary"]
        }

    def analyze(self, text):

        context_results = self.context_analyzer.analyze(text)
        classification_results = []

        for item in context_results:

            result = self.evaluator.evaluate(
                word=item["word"],
                part_of_speech=item["part_of_speech"],
                grammatical_role=item["grammatical_role"],
                context=item["context"]
            )

            word = item["word"].lower()
            registered = self.registered_vocabulary.get(word)

            if registered:
                category_map = {
                    "academic_skills": "Academic Vocabulary",
                    "academic_descriptions": "Academic Vocabulary",
                    "technical": "Technical Vocabulary",
                    "general": "General Vocabulary"
                }

                category = category_map.get(registered.get("category"))

                if category:
                    result["category"] = category
                    result["classification_source"] = "registered_vocabulary"
                    result["evidence"] = [
                        "Matched ACADEMIA registered vocabulary"
                    ]
                    result["confidence"] = 0.99
                    result["review_required"] = False
                    result["registered_word"] = True
                    result["japanese"] = registered.get("japanese")
                    result["definition"] = registered.get("definition")
                    result["level"] = registered.get("level")

            else:
                result["registered_word"] = False

            result["original_word"] = item["original_word"]
            result["head_word"] = item["head_word"]

            classification_results.append(result)

        saved_record = self.storage.save(
            original_text=text,
            results=classification_results
        )

        print("\nACADEMIA Document Classification")
        print("=" * 60)

        for result in classification_results:
            print(
                f"{result['word']} | "
                f"{result['category']} | "
                f"Confidence: {result.get('confidence', 'N/A')} | "
                f"Review: {result['review_required']}"
            )

        print("\nAnalysis saved successfully!")
        print("Analysis ID:", saved_record["analysis_id"])
        print("Total words:", saved_record["total_words"])
        print("Review required:", saved_record["review_count"])

        return saved_record


if __name__ == "__main__":

    sample_text = """
    University students must develop critical thinking skills.
    They need to interpret information, compare different perspectives,
    and support their conclusions with reliable evidence.
    """

    analyzer = AcademiaDocumentClassificationAnalyzer()
    analyzer.analyze(sample_text)
