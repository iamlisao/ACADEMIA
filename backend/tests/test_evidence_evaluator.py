
from academia_ai.classification_evaluator import (
    AcademiaClassificationEvaluator
)

evaluator = AcademiaClassificationEvaluator()

test_cases = [
    (
        "analyze",
        "VERB",
        "ROOT",
        "students analyze the research results"
    ),
    (
        "support",
        "VERB",
        "ROOT",
        "the evidence supports the theory"
    ),
    (
        "beautiful",
        "ADJ",
        "amod",
        "the garden looks beautiful"
    ),
    (
        "photosynthesis",
        "NOUN",
        "ROOT",
        "photosynthesis occurs in plants"
    ),
    (
        "student",
        "NOUN",
        "nsubj",
        "the student reads a book"
    )
]

print("\nACADEMIA Evidence Evaluation Test")
print("=" * 60)

for word, pos, role, context in test_cases:

    result = evaluator.evaluate(
        word,
        pos,
        role,
        context
    )

    print(f"\nWord: {result['word']}")
    print(f"Category: {result['category']}")
    print(f"Source: {result['classification_source']}")
    print(f"Evidence: {result['evidence']}")
    print(f"Review Required: {result['review_required']}")

    print("-" * 60)
