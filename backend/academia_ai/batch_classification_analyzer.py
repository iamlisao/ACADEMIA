import spacy

from classification_evaluator import (
    AcademiaClassificationEvaluator
)


class AcademiaBatchClassificationAnalyzer:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.evaluator = AcademiaClassificationEvaluator()

    def analyze(self, text):

        doc = self.nlp(text)
        results = []

        for token in doc:

            # Analyze only meaningful English words
            if not token.is_alpha:
                continue

            if token.pos_ not in {"NOUN", "VERB", "ADJ"}:
                continue

            word = token.lemma_.lower()

            # Extract nearby context
            start = max(0, token.i - 3)
            end = min(len(doc), token.i + 4)

            context = " ".join(
                item.text for item in doc[start:end]
            )

            result = self.evaluator.evaluate(
                word=word,
                part_of_speech=token.pos_,
                grammatical_role=token.dep_,
                context=context
            )

            results.append(result)

        return results


if __name__ == "__main__":

    analyzer = AcademiaBatchClassificationAnalyzer()

    sample_text = """
    Researchers analyze evidence to evaluate different arguments.
    Scientists investigate complex problems and develop new methods.
    """

    results = analyzer.analyze(sample_text)

    print("\nACADEMIA Batch Classification Analysis")
    print("=" * 60)

    for result in results:

        print(f"\nWord: {result['word']}")
        print(f"POS: {result['part_of_speech']}")
        print(f"Category: {result['category']}")
        print(f"Source: {result['classification_source']}")
        print(f"Evidence: {result['evidence']}")
        print(f"Review Required: {result['review_required']}")

    print("\n" + "=" * 60)
    print(f"Total analyzed words: {len(results)}")