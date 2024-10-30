class FlashcardApp:
    def __init__(self):
        self.flashcards = []

    def main_menu(self):
        while True:
            print("\n1. Add flashcards")
            print("2. Practice flashcards")
            print("3. Exit")
            choice = input()

            if choice == "1":
                self.add_flashcards_menu()
            elif choice == "2":
                self.practice_flashcards()
            elif choice == "3":
                print("Bye!")
                break
            else:
                print(f"{choice} is not an option")

    def add_flashcards_menu(self):
        while True:
            print("1. Add a new flashcard")
            print("2. Exit")
            choice = input()

            if choice == "1":
                question = ""
                while question == "":
                    question = input("Question:\n").strip()


                answer = ""
                while answer == "":
                    answer = input("Answer:\n").strip()

                self.flashcards.append((question, answer))

            elif choice == "2":
                break
            else:
                print(f"{choice} is not an option")

    def practice_flashcards(self):
        if not self.flashcards:
            print("\nThere is no flashcard to practice!")
            return

        for question, answer in self.flashcards:
            print(f"\nQuestion: {question}")
            choice = input("Please press \"y\" to see the answer or press \"n\" to skip:\n")

            if choice == "y":
                print(f"Answer: {answer}")
            elif choice == "n":
                continue
            else:
                print(f"{choice} is not an option. Wait for the right input.")


if __name__ == "__main__":
    app = FlashcardApp()
    app.main_menu()