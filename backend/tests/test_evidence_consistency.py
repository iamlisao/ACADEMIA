
from academia_ai.classification_evaluator import (
    AcademiaClassificationEvaluator
)

evaluator = AcademiaClassificationEvaluator()

test_cases = [
    ("analyze", "VERB", "ROOT", "students analyze data"),
    ("support", "VERB", "ROOT", "evidence supports the theory"),
    ("beautiful", "ADJ", "amod", "a beautiful garden"),
    ("photosynthesis", "NOUN", "ROOT", "photosynthesis in plants"),
    ("student", "NOUN", "nsubj", "the student reads a book"),
]

print("\nACADEMIA Evidence Consistency Test")
print("=" * 60)

correct = 0

for word, pos, role, context in test_cases:

    result = evaluator.evaluate(word, pos, role, context)

    category = result["category"]
    source = result["classification_source"]
    evidence = result["evidence"]
    review = result["review_required"]

    valid = (
        bool(category)
        and bool(source)
        and len(evidence) > 0
        and review == (category == "Needs Review")
    )

    if valid:
        correct += 1

    print(f"\nWord: {word}")
    print(f"Category: {category}")
    print(f"Source: {source}")
    print(f"Evidence: {evidence}")
    print(f"Review Required: {review}")
    print(f"Consistency: {'PASS' if valid else 'FAIL'}")

print("\nTest Summary")
print("=" * 60)
print(f"Consistent: {correct}/{len(test_cases)}")
