
import json
from pathlib import Path

FILE = Path("study_data.json")


def load_data():
    if FILE.exists():
        return json.loads(FILE.read_text())
    return {"completed_topics": []}


def save_data(data):
    FILE.write_text(json.dumps(data, indent=4))


def main():
    data = load_data()

    while True:
        print("\n=== NEUROFORGE STUDY ASSISTANT ===")
        print("1. Add completed topic")
        print("2. View completed topics")
        print("3. View progress")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            topic = input("Enter topic: ").strip()
            if topic:
                data["completed_topics"].append(topic)
                save_data(data)
                print("Topic saved!")

        elif choice == "2":
            for topic in data["completed_topics"]:
                print("-", topic)

        elif choice == "3":
            print("Topics completed:",
                  len(data["completed_topics"]))

        elif choice == "4":
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
