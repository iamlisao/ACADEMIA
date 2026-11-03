from .document_classification_analyzer import (
    AcademiaDocumentClassificationAnalyzer
)
from .weakness_detector import AcademiaWeaknessDetector
from .learning_recommender import AcademiaLearningRecommender
from .recommendation_storage import AcademiaRecommendationStorage
from .student_learning_analytics import (
    AcademiaStudentLearningAnalytics
)
from .learning_task_tracker import AcademiaLearningTaskTracker


class AcademiaMasterLearningPipeline:

    def __init__(self):
        self.document_analyzer = AcademiaDocumentClassificationAnalyzer()
        self.weakness_detector = AcademiaWeaknessDetector()
        self.recommender = AcademiaLearningRecommender()
        self.recommendation_storage = AcademiaRecommendationStorage()
        self.analytics = AcademiaStudentLearningAnalytics()
        self.task_tracker = AcademiaLearningTaskTracker()

    def run(self, text):
        if not text.strip():
            raise ValueError("Please enter an English text.")

        document = self.document_analyzer.analyze(text)
        weaknesses = self.weakness_detector.detect()
        recommendations = self.recommender.recommend()

        saved_recommendations = self.recommendation_storage.save(
            recommendations
        )

        student_report = self.analytics.analyze()
        tasks = self.task_tracker.load_tasks()

        print("\nACADEMIA MASTER LEARNING PIPELINE")
        print("=" * 60)
        print("Document Analysis: Completed")
        print("Weakness Detection:", len(weaknesses), "weaknesses found")
        print("Recommendations:", len(recommendations), "created")
        print("Recommendation Storage: Completed")
        print("Student Analytics: Updated")
        print("Learning Tasks:", len(tasks), "unique tasks")
        print("Analysis ID:", document["analysis_id"])
        print("Total Classified Words:",
              student_report["total_classified_words"])

        self.task_tracker.display()

        return {
            "document": document,
            "weaknesses": weaknesses,
            "recommendations": saved_recommendations,
            "student_report": student_report,
            "learning_tasks": tasks
        }


if __name__ == "__main__":
    print("\nACADEMIA Master Learning Pipeline")
    print("=" * 60)

    text = input("Enter an English paragraph: ")
    pipeline = AcademiaMasterLearningPipeline()
    pipeline.run(text)