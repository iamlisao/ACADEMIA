
from .document_classification_reader import (
    AcademiaDocumentClassificationReader
)
from .document_analysis_summary import (
    AcademiaDocumentAnalysisSummary
)


class AcademiaDocumentHistorySummary:

    def __init__(self):
        self.reader = AcademiaDocumentClassificationReader()
        self.summary_analyzer = AcademiaDocumentAnalysisSummary()

    def summarize_history(self):

        records = self.reader.load()

        all_results = []

        for record in records:
            all_results.extend(record.get("results", []))

        summary = self.summary_analyzer.summarize(all_results)

        summary["total_analyses"] = len(records)

        return summary


if __name__ == "__main__":

    analyzer = AcademiaDocumentHistorySummary()

    summary = analyzer.summarize_history()

    print("\nACADEMIA Learning History Summary")
    print("=" * 55)

    for key, value in summary.items():
        print(f"{key}: {value}")
