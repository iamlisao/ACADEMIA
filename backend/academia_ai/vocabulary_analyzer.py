
import json
import csv
import spacy

from pathlib import Path
from collections import Counter, defaultdict

from .vocabulary_classifier import AcademiaVocabularyClassifier

class AcademiaVocabularyAnalyzer:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

        self.classifier = AcademiaVocabularyClassifier()

        self.project_root = Path(__file__).resolve().parent.parent

        database_path = (
            self.project_root / "data" / "academic_vocabulary.json"
        )

        with open(database_path, "r", encoding="utf-8") as file:
            database = json.load(file)

        self.vocabulary = {
            item["word"]: item
            for item in database["vocabulary"]
        }

    def analyze(self, text):

        doc = self.nlp(text)

        lemmas = [
            token.lemma_.lower()
            for token in doc
            if token.is_alpha
        ]

        word_counts = Counter(lemmas)

        results = []
        unknown_pos = defaultdict(Counter)

        # Collect unknown vocabulary candidates
        for token in doc:

            if not token.is_alpha:
                continue

            word = token.lemma_.lower()

            if word in self.vocabulary:
                continue

            if token.is_stop or len(word) < 3:
                continue

            unknown_pos[word][token.pos_] += 1

        print("\nACADEMIA Vocabulary Analysis")
        print("=" * 45)

        print(f"Total words: {len(lemmas)}")
        print(f"Unique words: {len(word_counts)}")

        print("\nVocabulary Classification")
        print("-" * 45)

        for word, count in word_counts.items():

            item = self.vocabulary.get(word)

            if item:
                category = self.classifier.classify(
                    word,
                    item.get("category")
                )

                part_of_speech = item["part_of_speech"]

                japanese = item["japanese"]
                level = item["level"]
                definition = item["definition"]
                example = item["example"]

            else:
                if word not in unknown_pos:
                    continue

                category = self.classifier.classify(word)

                part_of_speech = (
                    unknown_pos[word].most_common(1)[0][0]
                )

                japanese = ""
                level = ""
                definition = ""
                example = ""

            print(
                f"{word} | "
                f"{category} | "
                f"{part_of_speech} | "
                f"x{count}"
            )

            results.append({
                "word": word,
                "category": category,
                "japanese": japanese,
                "definition": definition,
                "part_of_speech": part_of_speech,
                "level": level,
                "occurrences": count,
                "example": example
            })

        # Export all classification results
        output_path = (
            self.project_root / "data" / "vocabulary_classification.csv"
        )

        fieldnames = [
            "word",
            "category",
            "japanese",
            "definition",
            "part_of_speech",
            "level",
            "occurrences",
            "example"
        ]

        with open(
            output_path,
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(results)

        print("\nClassification file saved:")
        print(output_path)


if __name__ == "__main__":

    sample_text = """
    Students analyze evidence.
    The student analyzed significant changes.
    Researchers are evaluating the results.
    The results demonstrate the importance of education.
    Scientists investigate complex problems.
    Researchers develop a hypothesis.
    """

    analyzer = AcademiaVocabularyAnalyzer()
    analyzer.analyze(sample_text)
