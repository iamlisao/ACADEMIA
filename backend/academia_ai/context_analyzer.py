
import spacy


class AcademiaContextAnalyzer:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def analyze(self, text):

        doc = self.nlp(text)

        results = []

        for token in doc:

            if not token.is_alpha:
                continue

            if token.pos_ not in {"VERB", "NOUN", "ADJ"}:
                continue

            word = token.lemma_.lower()

            context = [
                item.text
                for item in doc
                if abs(item.i - token.i) <= 3
                and item.i != token.i
            ]

            results.append({
                "word": word,
                "original_word": token.text,
                "part_of_speech": token.pos_,
                "grammatical_role": token.dep_,
                "head_word": token.head.text,
                "context": " ".join(context)
            })

        return results


if __name__ == "__main__":

    sample_text = """
    Researchers develop new methods to investigate complex problems.
    Students analyze evidence to evaluate different arguments.
    """

    analyzer = AcademiaContextAnalyzer()

    for result in analyzer.analyze(sample_text):
        print(result)
