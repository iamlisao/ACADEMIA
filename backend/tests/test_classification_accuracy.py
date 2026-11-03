
from academia_ai.context_vocabulary_classifier import (
    AcademiaContextVocabularyClassifier
)


classifier = AcademiaContextVocabularyClassifier()


test_cases = [

    # Academic Vocabulary
    ("analyze", "VERB", "ROOT", "students analyze the results", "Academic Vocabulary"),
    ("evidence", "NOUN", "dobj", "researchers present evidence", "Academic Vocabulary"),
    ("hypothesis", "NOUN", "dobj", "test the hypothesis", "Academic Vocabulary"),
    ("evaluate", "VERB", "ROOT", "evaluate the research method", "Academic Vocabulary"),
    ("researcher", "NOUN", "nsubj", "the researcher conducted a study", "Academic Vocabulary"),
    ("scientist", "NOUN", "nsubj", "the scientist conducted research", "Academic Vocabulary"),
    ("method", "NOUN", "dobj", "use a scientific method", "Academic Vocabulary"),
    ("significant", "ADJ", "amod", "a significant result", "Academic Vocabulary"),

    # General Vocabulary
    ("student", "NOUN", "nsubj", "the student reads a book", "General Vocabulary"),
    ("teacher", "NOUN", "nsubj", "the teacher explains the lesson", "General Vocabulary"),
    ("school", "NOUN", "dobj", "students attend school", "General Vocabulary"),
    ("problem", "NOUN", "dobj", "solve the problem", "General Vocabulary"),
    ("change", "NOUN", "dobj", "a change in the situation", "General Vocabulary"),
    ("question", "NOUN", "dobj", "answer the question", "General Vocabulary"),

    # Technical Vocabulary
    ("molecule", "NOUN", "dobj", "chemical molecule structure", "Technical Vocabulary"),
    ("photosynthesis", "NOUN", "nsubj", "photosynthesis occurs in plants", "Technical Vocabulary"),
    ("algorithm", "NOUN", "dobj", "the computer uses an algorithm", "Technical Vocabulary"),

    # Context and uncertain cases
    ("support", "VERB", "ROOT", "evidence support the theory", "Academic Vocabulary"),
    ("support", "NOUN", "dobj", "my family gives me support", "Needs Review"),
    ("beautiful", "ADJ", "amod", "a beautiful day", "Needs Review"),
    ("different", "ADJ", "amod", "different colors of flowers", "Needs Review"),
    ("new", "ADJ", "amod", "a new notebook", "Needs Review"),
]


correct = 0

print("\nACADEMIA Classification Accuracy Test")
print("=" * 65)

for word, pos, role, context, expected in test_cases:

    actual = classifier.classify(
        word,
        pos,
        role,
        context
    )

    passed = actual == expected

    if passed:
        correct += 1

    status = "PASS" if passed else "FAIL"

    print(
        f"{word:16} | "
        f"Expected: {expected:22} | "
        f"Actual: {actual:22} | "
        f"{status}"
    )


total = len(test_cases)
accuracy = (correct / total) * 100

print("\nTest Summary")
print("-" * 65)
print(f"Correct: {correct}/{total}")
print(f"Accuracy: {accuracy:.1f}%")
