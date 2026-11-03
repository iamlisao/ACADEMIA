import json
from pathlib import Path

from .weakness_detector import AcademiaWeaknessDetector


class AcademiaLearningRecommender:

    def __init__(self):
        self.detector = AcademiaWeaknessDetector()

        base_path = Path(__file__).resolve().parent.parent / "data"

        self.data_path = base_path / "document_classification_results.json"
        self.status_path = base_path / "review_learning_status.json"
        self.task_status_path = base_path / "learning_task_status.json"

    def load_json(self, path):
        if not path.exists():
            return {}

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_review_words(self):
        records = self.load_json(self.data_path)
        statuses = self.load_json(self.status_path)

        review_words = {}

        for record in records:
            for result in record.get("results", []):
                if not result.get("review_required"):
                    continue

                word = result["word"].lower()
                status = statuses.get(word, {}).get("status", "Not Started")

                if status != "Mastered":
                    review_words[word] = result

        return list(review_words.keys())

    def recommend(self):
        weaknesses = self.detector.detect()
        recommendations = []

        review_words = self.load_review_words()
        task_statuses = self.load_json(self.task_status_path)

        for item in weaknesses:

            area = item["area"]

            if area == "Vocabulary Review" and review_words:
                recommendations.append({
                    "activity": "Academic Vocabulary Practice",
                    "task": "Review these words: " + ", ".join(review_words),
                    "duration": "10 minutes"
                })

            elif area == "Learning Progress":
                recommendations.append({
                    "activity": "Vocabulary Review Session",
                    "task": "Practice words marked as Learning.",
                    "duration": "10 minutes"
                })

        completed_tasks = sum(
            1 for item in task_statuses.values()
            if item.get("status") == "Completed"
        )

        if completed_tasks > 0:
            recommendations.append({
                "activity": "Next Learning Challenge",
                "task": "Complete a new academic reading and vocabulary analysis.",
                "duration": "15 minutes"
            })

        return recommendations

    def display(self):
        recommendations = self.recommend()

        print("\nACADEMIA Personalized Learning Plan")
        print("=" * 55)

        if not recommendations:
            print("No recommendations. Keep up the good work!")
            return

        for index, item in enumerate(recommendations, start=1):
            print(f"\n{index}. {item['activity']}")
            print(f"Task: {item['task']}")
            print(f"Duration: {item['duration']}")


if __name__ == "__main__":
    recommender = AcademiaLearningRecommender()
    recommender.display()