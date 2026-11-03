
from .context_vocabulary_classifier import (
    AcademiaContextVocabularyClassifier
)


class AcademiaClassificationEvaluator:

    def __init__(self):
        self.classifier = AcademiaContextVocabularyClassifier()

    def evaluate(
        self,
        word,
        part_of_speech,
        grammatical_role,
        context
    ):

        category = self.classifier.classify(
            word,
            part_of_speech,
            grammatical_role,
            context
        )

        normalized_word = word.lower().strip()
        context_words = set(context.lower().split())

        evidence = []
        classification_source = "no_matching_rule"

        basic_classifier = self.classifier.classifier

        academic_words = basic_classifier.ACADEMIC_WORDS
        technical_words = basic_classifier.TECHNICAL_WORDS
        general_words = basic_classifier.GENERAL_WORDS

        additional_academic_words = {
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

        additional_technical_words = {
            "photosynthesis",
            "algorithm",
            "molecule",
            "ecosystem",
            "chromosome",
            "derivative",
            "mitochondria",
            "polymer",
        }

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

        # 1. Check the actual classification result
        if category == "Academic Vocabulary":

            if normalized_word in academic_words:
                classification_source = "academic_word_list"
                evidence.append(
                    "Matched academic vocabulary list"
                )

            elif normalized_word in additional_academic_words:
                classification_source = "additional_academic_word_list"
                evidence.append(
                    "Matched additional academic vocabulary list"
                )

            else:
                matched_clues = sorted(
                    context_words & academic_clues
                )

                classification_source = "academic_context"

                if matched_clues:
                    evidence.append(
                        f"Academic context clues: {matched_clues}"
                    )
                else:
                    evidence.append(
                        "Academic classification from context rule"
                    )

        elif category == "Technical Vocabulary":

            classification_source = "technical_word_list"

            if (
                normalized_word in technical_words
                or normalized_word in additional_technical_words
            ):
                evidence.append(
                    "Matched technical vocabulary list"
                )
            else:
                evidence.append(
                    "Matched technical classification rule"
                )

        elif category == "General Vocabulary":

            classification_source = "general_word_list"

            if normalized_word in general_words:
                evidence.append(
                    "Matched general vocabulary list"
                )
            else:
                evidence.append(
                    "Matched general vocabulary classification rule"
                )

        else:

            classification_source = "no_matching_rule"

            evidence.append(
                "No matching classification rule found"
            )

        # 2. Calculate provisional confidence score
        confidence_scores = {
            "academic_word_list": 0.95,
            "additional_academic_word_list": 0.90,
            "technical_word_list": 0.95,
            "general_word_list": 0.90,
            "academic_context": 0.75,
            "no_matching_rule": 0.30,
        }

        confidence = confidence_scores.get(
            classification_source,
            0.30
        )

        review_required = category == "Needs Review"

        return {
            "word": word,
            "part_of_speech": part_of_speech,
            "grammatical_role": grammatical_role,
            "context": context,
            "category": category,
            "classification_source": classification_source,
            "evidence": evidence,
            "review_required": review_required,
            "confidence": confidence
        }


if __name__ == "__main__":

    evaluator = AcademiaClassificationEvaluator()

    result = evaluator.evaluate(
        word="support",
        part_of_speech="VERB",
        grammatical_role="ROOT",
        context="evidence support the theory"
    )

    print("\nACADEMIA Classification Evaluation")
    print("=" * 55)

    for key, value in result.items():
        print(f"{key}: {value}")
