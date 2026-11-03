
from .vocabulary_classifier import AcademiaVocabularyClassifier

class AcademiaContextVocabularyClassifier:

    def __init__(self):
        self.classifier = AcademiaVocabularyClassifier()

    def classify(
        self,
        word,
        part_of_speech,
        grammatical_role,
        context
    ):

        word = word.lower().strip()

        # 1. Existing vocabulary classification
        basic_category = self.classifier.classify(word)

        if basic_category != "Needs Review":
            return basic_category

        # 2. Additional vocabulary
        academic_words = {
            "researcher",
            "scientist",
            "method",
            "importance",
            "education",
            "influence",
            "society",
            "result",
            "results",
        }

        technical_words = {
            "photosynthesis",
            "algorithm",
            "molecule",
            "ecosystem",
            "chromosome",
            "derivative",
            "mitochondria",
            "polymer",
        }

        if word in technical_words:
            return "Technical Vocabulary"

        if word in academic_words:
            return "Academic Vocabulary"

        # 3. Context-based classification
        context_words = set(context.lower().split())

        academic_clues = {
            "research",
            "study",
            "evidence",
            "theory",
            "analysis",
            "results",
            "argument",
            "experiment",
            "data",
        }

        if (
            word == "support"
            and part_of_speech == "VERB"
            and context_words & academic_clues
        ):
            return "Academic Vocabulary"

        return "Needs Review"
