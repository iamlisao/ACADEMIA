
from .vocabulary_analyzer import AcademiaVocabularyAnalyzer
from .context_analyzer import AcademiaContextAnalyzer
from .classification_evaluator import AcademiaClassificationEvaluator


class AcademiaIntegratedAnalyzer:

    def __init__(self):
        self.vocabulary_analyzer = AcademiaVocabularyAnalyzer()
        self.context_analyzer = AcademiaContextAnalyzer()
        self.classification_evaluator = AcademiaClassificationEvaluator()

    def analyze(self, text):

        print("\nACADEMIA Integrated Analysis")
        print("=" * 50)

        # 1. Vocabulary analysis
        self.vocabulary_analyzer.analyze(text)

        # 2. Context analysis
        context_results = self.context_analyzer.analyze(text)

        print("\nIntegrated Classification")
        print("-" * 50)

        # 3. Context-based classification and evaluation
        for result in context_results:

            evaluation = self.classification_evaluator.evaluate(
                word=result["word"],
                part_of_speech=result["part_of_speech"],
                grammatical_role=result["grammatical_role"],
                context=result["context"]
            )

            print(
                f"{evaluation['word']} | "
                f"{evaluation['category']} | "
                f"Confidence: {evaluation['confidence']} | "
                f"Review: {evaluation['review_required']}"
            )

        print("\nACADEMIA Analysis Completed!")


if __name__ == "__main__":

    sample_text = """
    Researchers develop new methods to investigate complex problems.
    Students analyze evidence to evaluate different arguments.
    Scientists demonstrate how education influences society.
    """

    analyzer = AcademiaIntegratedAnalyzer()
    analyzer.analyze(sample_text)
