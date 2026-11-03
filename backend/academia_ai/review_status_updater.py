
from .review_learning_storage import AcademiaReviewLearningStorage


def main():
    storage = AcademiaReviewLearningStorage()

    word = input("Word: ").strip()
    print("1. Not Started")
    print("2. Learning")
    print("3. Mastered")

    choice = input("Select status: ").strip()

    statuses = {
        "1": "Not Started",
        "2": "Learning",
        "3": "Mastered"
    }

    if choice not in statuses:
        print("Invalid selection.")
        return

    result = storage.update_status(word, statuses[choice])
    print("Updated:", result)


if __name__ == "__main__":
    main()
