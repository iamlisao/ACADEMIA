
import json
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4


class AcademiaDocumentClassificationStorage:

    def __init__(self):
        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "document_classification_results.json"
        )

    def save(self, original_text, results):

        self.data_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if self.data_path.exists():
            with open(self.data_path, "r", encoding="utf-8") as file:
                records = json.load(file)
        else:
            records = []

        record = {
            "analysis_id": str(uuid4()),
            "original_text": original_text,
            "results": results,
            "total_words": len(results),
            "review_count": sum(
                1 for item in results
                if item.get("review_required", False)
            ),
            "analyzed_at": datetime.now(timezone.utc).isoformat()
        }

        records.append(record)

        with open(self.data_path, "w", encoding="utf-8") as file:
            json.dump(
                records,
                file,
                ensure_ascii=False,
                indent=4
            )

        return record
