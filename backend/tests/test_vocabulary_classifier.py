import sys
from pathlib import Path

# backendフォルダをPythonの検索対象に追加
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR / "academia_ai"))

from vocabulary_classifier import AcademiaVocabularyClassifier

def test_vocabulary_classification():

    classifier = AcademiaVocabularyClassifier()

    test_cases = [
        ("analyze", "Academic Vocabulary"),
        ("hypothesis", "Academic Vocabulary"),
        ("student", "General Vocabulary"),
        ("photosynthesis", "Technical Vocabulary"),
        ("beautiful", "Needs Review"),
    ]

    correct = 0

    print("\nACADEMIA Vocabulary Classification Test")
    print("=" * 55)

    for word, expected in test_cases:

        actual = classifier.classify(word)

        if actual == expected:
            result = "PASS"
            correct += 1
        else:
            result = "FAIL"

        print(f"{word}: Expected={expected} | Actual={actual} | {result}")

    total = len(test_cases)
    accuracy = (correct / total) * 100

    print("\nTest Summary")
    print("-" * 55)
    print(f"Correct: {correct}/{total}")
    print(f"Accuracy: {accuracy:.1f}%")


if __name__ == "__main__":
    test_vocabulary_classification()