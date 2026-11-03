import json
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

import spacy

from .classification_evaluator import AcademiaClassificationEvaluator
class AcademiaAcademicTextAnalyzer:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.evaluator = AcademiaClassificationEvaluator()

        self.vocabulary_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "academic_vocabulary.json"
        )

        with open(self.vocabulary_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.vocabulary = {
            item["word"].lower(): item
            for item in data["vocabulary"]
        }

    def analyze(self, text):
        doc = self.nlp(text)

        sentences = []
        vocabulary_results = []

        category_mapping = {
            "academic_skills": "Academic Vocabulary",
            "academic_descriptions": "Academic Vocabulary",
            "technical": "Technical Vocabulary",
            "general": "General Vocabulary"
        }

        for sentence in doc.sents:
            sentence_words = []

            for token in sentence:
                if not token.is_alpha:
                    continue

                if token.pos_ not in {"NOUN", "VERB", "ADJ", "ADV"}:
                    continue

                word = token.lemma_.lower()

                context = sentence[
                    max(0, token.i - 3):token.i + 4
                ]

                context_text = " ".join(
                    item.text for item in context if item != token
                )

                result = self.evaluator.evaluate(
                    word=word,
                    part_of_speech=token.pos_,
                    grammatical_role=token.dep_,
                    context=context_text
                )

                registered = self.vocabulary.get(word)

                if registered:
                    result["category"] = category_mapping.get(
                        registered["category"],
                        result["category"]
                    )

                    result["classification_source"] = (
                        "registered_vocabulary"
                    )

                    result["evidence"] = [
                        "Matched ACADEMIA registered vocabulary"
                    ]

                    result["confidence"] = 0.99
                    result["review_required"] = False

                    result["registered_word"] = True
                    result["japanese"] = registered["japanese"]
                    result["definition"] = registered["definition"]
                    result["level"] = registered["level"]

                else:
                    result["registered_word"] = False

                vocabulary_results.append(result)
                sentence_words.append(token.text)

            sentences.append({
                "sentence": sentence.text.strip(),
                "words_analyzed": sentence_words
            })

        return {
            "original_text": text,
            "total_sentences": len(sentences),
            "total_words": len([t for t in doc if t.is_alpha]),
            "sentences": sentences,
            "vocabulary_analysis": vocabulary_results
        }
    def save_analysis(self, result):
        save_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "academic_text_analysis_history.json"
        )

        if save_path.exists():
            with open(save_path, "r", encoding="utf-8") as file:
                history = json.load(file)
        else:
            history = []

        record = {
            "analysis_id": str(uuid4()),
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            **result
        }

        history.append(record)

        with open(save_path, "w", encoding="utf-8") as file:
            json.dump(
                history,
                file,
                ensure_ascii=False,
                indent=4
            )

        print("\nAnalysis saved successfully!")
        print("Analysis ID:", record["analysis_id"])
        print("File:", save_path)

        return record
    
    def display(self, result):
        print("\nACADEMIA ACADEMIC TEXT ANALYZER")
        print("=" * 55)

        print("\nText Statistics")
        print("Total sentences:", result["total_sentences"])
        print("Total words:", result["total_words"])

        print("\nSentence Analysis")

        for index, sentence in enumerate(
            result["sentences"], start=1
        ):
            print(f"\n{index}. {sentence['sentence']}")
            print(
                "Analyzed words:",
                ", ".join(sentence["words_analyzed"])
            )

        print("\nVocabulary Analysis")
        print("-" * 55)

        for item in result["vocabulary_analysis"]:
            print(
                item["word"],
                "|",
                item["category"],
                "| Confidence:",
                item["confidence"]
            )

            if item["registered_word"]:
                print("Japanese:", item["japanese"])
                print("Definition:", item["definition"])
                print("Level:", item["level"])

        print("\nAnalysis Complete.")


if __name__ == "__main__":
    analyzer = AcademiaAcademicTextAnalyzer()

    sample_text = """
    Researchers analyze evidence to evaluate the effects of education.
    Critical thinking helps university students interpret complex information.
    """

    result = analyzer.analyze(sample_text)
    analyzer.display(result)
    analyzer.save_analysis(result)
