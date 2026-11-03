
import json
from pathlib import Path
from datetime import datetime, timezone


class AcademiaRecommendationStorage:

    def __init__(self):
        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "learning_recommendations.json"
        )

    def save(self, recommendations):

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
            "recommendations": recommendations,
            "saved_at": datetime.now(timezone.utc).isoformat()
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


if __name__ == "__main__":
    from .learning_recommender import AcademiaLearningRecommender

    recommender = AcademiaLearningRecommender()
    recommendations = recommender.recommend()

    storage = AcademiaRecommendationStorage()
    saved = storage.save(recommendations)

    print("\nACADEMIA Recommendation Storage")
    print("=" * 55)
    print("Saved successfully!")
    print("Recommendations:", len(saved["recommendations"]))
    print("File:", storage.data_path)
