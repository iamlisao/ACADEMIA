
from academia_ai.classification_evaluator import (
    AcademiaClassificationEvaluator
)


evaluator = AcademiaClassificationEvaluator()

test_cases = [
    {
        "word": "analyze",
        "pos": "VERB",
        "role": "ROOT",
        "context": "students analyze the results",
        "expected": 0.95
    },
    {
        "word": "researcher",
        "pos": "NOUN",
        "role": "nsubj",
        "context": "the researcher studies society",
        "expected": 0.95
    },
    {
        "word": "support",
        "pos": "VERB",
        "role": "ROOT",
        "context": "evidence support the theory",
        "expected": 0.75
    },
    {
        "word": "student",
        "pos": "NOUN",
        "role": "nsubj",
        "context": "the student reads a book",
        "expected": 0.90
    },
    {
        "word": "beautiful",
        "pos": "ADJ",
        "role": "amod",
        "context": "a beautiful garden",
        "expected": 0.30
    }
]

print("\nACADEMIA Confidence Score Test")
print("=" * 65)

passed = 0

for case in test_cases:

    result = evaluator.evaluate(
        word=case["word"],
        part_of_speech=case["pos"],
        grammatical_role=case["role"],
        context=case["context"]
    )

    actual = result["confidence"]
    expected = case["expected"]

    status = "PASS" if actual == expected else "FAIL"

    if status == "PASS":
        passed += 1

    print(
        f'{case["word"]:15} | '
        f'Expected: {expected:.2f} | '
        f'Actual: {actual:.2f} | '
        f'{status}'
    )

print("-" * 65)
print(f"Correct: {passed}/{len(test_cases)}")
