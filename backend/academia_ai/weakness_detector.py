
from .student_learning_analytics import (
    AcademiaStudentLearningAnalytics
)


class AcademiaWeaknessDetector:

    def __init__(self):
        self.analytics = AcademiaStudentLearningAnalytics()

    def detect(self):
        report = self.analytics.analyze()

        categories = report["category_counts"]
        total = report["total_classified_words"]

        weaknesses = []

        # 1. Review words
        if report["unique_review_words"] > 0:
            weaknesses.append({
                "area": "Vocabulary Review",
                "reason": (
                    f'{report["unique_review_words"]} unique '
                    "words need review."
                ),
                "priority": "High"
            })

        # 2. Academic vocabulary coverage
        academic_count = categories["Academic Vocabulary"]

        if total > 0:
            academic_ratio = academic_count / total

            if academic_ratio < 0.5:
                weaknesses.append({
                    "area": "Academic Vocabulary",
                    "reason": (
                        "Academic vocabulary currently represents "
                        "less than 50% of classified words."
                    ),
                    "priority": "Medium"
                })

        # 3. Unmastered review words
        statuses = report["learning_status"]

        unmastered = (
            statuses["Not Started"] + statuses["Learning"]
        )

        if unmastered > 0:
            weaknesses.append({
                "area": "Learning Progress",
                "reason": (
                    f"{unmastered} review words are not yet mastered."
                ),
                "priority": "High"
            })

        return weaknesses

    def display(self):
        weaknesses = self.detect()

        print("\nACADEMIA Weakness Detection")
        print("=" * 55)

        if not weaknesses:
            print("No major weaknesses detected.")
            return

        for item in weaknesses:
            print(f'\nArea: {item["area"]}')
            print(f'Reason: {item["reason"]}')
            print(f'Priority: {item["priority"]}')

        print("\nTotal weaknesses detected:", len(weaknesses))


if __name__ == "__main__":
    detector = AcademiaWeaknessDetector()
    detector.display()
