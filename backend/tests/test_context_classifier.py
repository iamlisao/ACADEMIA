from academia_ai.context_vocabulary_classifier import (
    AcademiaContextVocabularyClassifier
)


def test_context_classification():

    classifier = AcademiaContextVocabularyClassifier()

    test_cases = [
        {
            "word": "support",
            "pos": "VERB",
            "role": "ROOT",
            "context": "evidence support the theory",
            "expected": "Academic Vocabulary"
        },
        {
            "word": "support",
            "pos": "NOUN",
            "role": "ROOT",
            "context": "my family gives me support",
            "expected": "Needs Review"
        },
        {
            "word": "molecule",
            "pos": "NOUN",
            "role": "ROOT",
            "context": "chemical molecule structure",
            "expected": "Technical Vocabulary"
        },
        {
            "word": "beautiful",
            "pos": "ADJ",
            "role": "amod",
            "context": "a beautiful day",
            "expected": "Needs Review"
        }
    ]

    correct = 0

    print("\nACADEMIA Context Classification Test")
    print("=" * 60)

    for case in test_cases:

        actual = classifier.classify(
            case["word"],
            case["pos"],
            case["role"],
            case["context"]
        )

        expected = case["expected"]

        if actual == expected:
            result = "PASS"
            correct += 1
        else:
            result = "FAIL"

        print(
            f'{case["word"]} | '
            f'Expected: {expected} | '
            f'Actual: {actual} | {result}'
        )

    total = len(test_cases)
    accuracy = (correct / total) * 100

    print("\nTest Summary")
    print("-" * 60)
    print(f"Correct: {correct}/{total}")
    print(f"Accuracy: {accuracy:.1f}%")


if __name__ == "__main__":
    test_context_classification()