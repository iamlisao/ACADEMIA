
class AcademiaVocabularyClassifier:

    ACADEMIC_WORDS = {
        "analyze", "analysis", "evaluate", "evaluation",
        "demonstrate", "evidence", "hypothesis",
        "investigate", "investigation", "significant",
        "interpret", "interpretation", "justify",
        "establish", "identify", "concept", "theory",
        "argument", "conclude", "conclusion",
        "researcher", "research", "method", "approach",
        "result", "results", "influence", "impact",
        "society", "education", "importance", "factor",
        "process", "structure", "principle", "function",
        "develop", "development", "complex", "complexity"
    }

    GENERAL_WORDS = {
        "student", "teacher", "school", "book",
        "people", "thing", "place", "time",
        "change", "problem", "answer", "question",
        "study", "work", "make", "use"
    }

    TECHNICAL_WORDS = {
        "photosynthesis", "algorithm", "molecule",
        "ecosystem", "chromosome", "derivative",
        "mitochondria", "polymer"
    }

    def classify(self, word, registered_category=None):

        word = word.lower().strip()

        # Registered vocabulary takes priority
        if registered_category in {
            "academic_skills",
            "academic_descriptions"
        }:
            return "Academic Vocabulary"

        if registered_category == "technical":
            return "Technical Vocabulary"

        if registered_category == "general":
            return "General Vocabulary"

        if word in self.ACADEMIC_WORDS:
            return "Academic Vocabulary"

        if word in self.TECHNICAL_WORDS:
            return "Technical Vocabulary"

        if word in self.GENERAL_WORDS:
            return "General Vocabulary"

        return "Needs Review"


if __name__ == "__main__":

    classifier = AcademiaVocabularyClassifier()

    test_words = [
        "analyze",
        "hypothesis",
        "researcher",
        "method",
        "student",
        "photosynthesis",
        "beautiful",
        "society",
        "influence"
    ]

    print("\nACADEMIA Vocabulary Classification")
    print("=" * 45)

    for word in test_words:
        print(f"{word}: {classifier.classify(word)}")
