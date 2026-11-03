
from academia_ai.document_classification_storage import (
    AcademiaDocumentClassificationStorage
)


storage = AcademiaDocumentClassificationStorage()

sample_text = (
    "Students analyze evidence to evaluate their arguments."
)

sample_results = [
    {
        "word": "analyze",
        "category": "Academic Vocabulary",
        "confidence": 0.95,
        "review_required": False,
        "evidence": ["Matched academic vocabulary list"]
    },
    {
        "word": "evidence",
        "category": "Academic Vocabulary",
        "confidence": 0.95,
        "review_required": False,
        "evidence": ["Matched academic vocabulary list"]
    },
    {
        "word": "different",
        "category": "Needs Review",
        "confidence": 0.30,
        "review_required": True,
        "evidence": ["No matching classification clues found"]
    }
]

saved_record = storage.save(
    original_text=sample_text,
    results=sample_results
)

print("\nACADEMIA Document Storage Test")
print("=" * 50)
print("Saved successfully!")
print("Analysis ID:", saved_record["analysis_id"])
print("Total words:", saved_record["total_words"])
print("Review required:", saved_record["review_count"])
print("Saved file:", storage.data_path)
