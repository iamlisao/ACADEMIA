
from academia_ai.context_vocabulary_classifier import (
    AcademiaContextVocabularyClassifier
)

classifier = AcademiaContextVocabularyClassifier()

test_cases = [
    # Academic Vocabulary
    (
        "significant",
        "ADJ",
        "amod",
        "the study found a significant difference",
        "Academic Vocabulary"
    ),
    (
        "analyze",
        "VERB",
        "ROOT",
        "students analyze the research results",
        "Academic Vocabulary"
    ),
    (
        "support",
        "VERB",
        "ROOT",
        "the evidence support the theory",
        "Academic Vocabulary"
    ),

    # General Vocabulary
    (
        "student",
        "NOUN",
        "nsubj",
        "the student reads a book",
        "General Vocabulary"
    ),
    (
        "change",
        "NOUN",
        "dobj",
        "the weather caused a change",
        "General Vocabulary"
    ),

    # Technical Vocabulary
    (
        "photosynthesis",
        "NOUN",
        "nsubj",
        "photosynthesis occurs in plants",
        "Technical Vocabulary"
    ),
    (
        "algorithm",
        "NOUN",
        "dobj",
        "the computer uses an algorithm",
        "Technical Vocabulary"
    ),

    # Needs Review
    (
        "beautiful",
        "ADJ",
        "amod",
        "a beautiful day",
        "Needs Review"
    ),
    (
        "different",
        "ADJ",
        "amod",
        "different colors of flowers",
        "Needs Review"
    ),
    (
        "new",
        "ADJ",
        "amod",
        "a new notebook",
        "Needs Review"
    ),
]

correct = 0

print("ACADEMIA Extended Context Accuracy Test")
print("=" * 65)

for word, pos, role, context, expected in test_cases:
    actual = classifier.classify(word, pos, role, context)

    result = "PASS" if actual == expected else "FAIL"

    if result == "PASS":
        correct += 1

    print(
        f"{word:18} | Expected: {expected:23} "
        f"| Actual: {actual:23} | {result}"
    )

total = len(test_cases)
accuracy = correct / total * 100

print("\nTest Summary")
print("-" * 65)
print(f"Correct: {correct}/{total}")
print(f"Accuracy: {accuracy:.1f}%")
