
from academia_ai.classification_evaluator import (
    AcademiaClassificationEvaluator
)

evaluator = AcademiaClassificationEvaluator()

test_cases = [
    ("analyze", "VERB", "ROOT", "students analyze the results"),
    ("evidence", "NOUN", "dobj", "the evidence supports the theory"),
    ("support", "VERB", "ROOT", "evidence supports the theory"),
    ("support", "NOUN", "dobj", "my family gave me support"),
    ("student", "NOUN", "nsubj", "the student reads a book"),
    ("photosynthesis", "NOUN", "ROOT", "photosynthesis occurs in plants"),
    ("beautiful", "ADJ", "amod", "a beautiful garden"),
    ("different", "ADJ", "amod", "the results were different"),
]

print("\nACADEMIA Classification Quality Review")
print("=" * 65)

for word, pos, role, context in test_cases:

    result = evaluator.evaluate(word, pos, role, context)

    print(f"\nWord: {word}")
    print(f"Context: {context}")
    print(f"Category: {result['category']}")
    print(f"Source: {result['classification_source']}")
    print(f"Review Required: {result['review_required']}")
    print("-" * 65)
