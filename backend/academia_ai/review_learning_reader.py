
from .review_learning_storage import (
    AcademiaReviewLearningStorage
)


class AcademiaReviewLearningReader:

    def __init__(self):
        self.storage = AcademiaReviewLearningStorage()

    def display(self):

        records = self.storage.load()

        print("\nACADEMIA Learning Status")
        print("=" * 55)

        if not records:
            print("No learning records found.")
            return

        for word, record in records.items():

            print(
                f"{word} | "
                f"Status: {record.get('status', 'Not Started')} | "
                f"Updated: {record.get('updated_at', 'Unknown')}"
            )

        print("\nTotal words:", len(records))


if __name__ == "__main__":

    reader = AcademiaReviewLearningReader()
    reader.display()
