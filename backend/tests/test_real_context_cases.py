
from academia_ai.context_vocabulary_classifier import (
    AcademiaContextVocabularyClassifier
)

classifier = AcademiaContextVocabularyClassifier()

test_cases = [
    # Same word, different contexts
    (
        "support",
        "VERB",
        "ROOT",
        "the evidence supports the researcher's argument",
        "Academic Vocabulary"
    ),
    (
        "support",
        "VERB",
        "ROOT",
        "my family supports my decision",
        "Needs Review"
    ),
    (
        "significant",
        "ADJ",
        "amod",
        "the research produced significant results",
        "Academic Vocabulary"
    ),
    (
        "different",
        "ADJ",
        "amod",
        "the results were different from our expectations",
        "Needs Review"
    ),

    # Academic contexts
    (
        "evaluate",
        "VERB",
        "ROOT",
        "students evaluate the research evidence",
        "Academic Vocabulary"
    ),
    (
        "hypothesis",
        "NOUN",
        "dobj",
        "the experiment tests the hypothesis",
        "Academic Vocabulary"
    ),

    # Everyday contexts
    (
        "beautiful",
        "ADJ",
        "amod",
        "the garden looks beautiful",
        "Needs Review"
    ),
    (
        "change",
        "NOUN",
        "dobj",
        "she made a change to her outfit",
        "General Vocabulary"
    ),
]

correct = 0

print("ACADEMIA Real Context Test")
print("=" * 75)

for word, pos, role, context, expected in test_cases:
    actual = classifier.classify(word, pos, role, context)

    result = "PASS" if actual == expected else "FAIL"

    if result == "PASS":
        correct += 1

    print(f"\nWord: {word}")
    print(f"Context: {context}")
    print(f"Expected: {expected}")
    print(f"Actual: {actual}")
    print(f"Result: {result}")

total = len(test_cases)
accuracy = correct / total * 100

print("\nTest Summary")
print("=" * 75)
print(f"Correct: {correct}/{total}")
print(f"Accuracy: {accuracy:.1f}%")
