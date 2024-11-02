from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///flashcard.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Flashcard(Base):
    __tablename__ = 'flashcards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    box = Column(Integer, default=1)  # Track the Leitner box

Base.metadata.create_all(engine)

class FlashcardApp:
    def __init__(self):
        self.session = session

    def main_menu(self):
        while True:
            print("1. Add flashcards")
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
                question = input("Question:\n").strip()
                while not question:
                    print("Question cannot be empty.")
                    question = input("Question:\n").strip()

                answer = input("Answer:\n").strip()
                while not answer:
                    print("Answer cannot be empty.")
                    answer = input("Answer:\n").strip()

                new_flashcard = Flashcard(question=question, answer=answer, box=1)
                self.session.add(new_flashcard)
                self.session.commit()
            elif choice == "2":
                return
            else:
                print(f"{choice} is not an option")

    def practice_flashcards(self):
        flashcards = self.session.query(Flashcard).order_by(Flashcard.box).all()
        if not flashcards:
            print("There is no flashcard to practice!")
            return

        for flashcard in flashcards:
            if self.process_flashcard(flashcard):
                # After processing a card, re-fetch flashcards to check if any are left
                flashcards = self.session.query(Flashcard).order_by(Flashcard.box).all()
                if not flashcards:
                    print("There is no flashcard to practice!")
                    return

    def process_flashcard(self, flashcard):
        while True:
            print(f"\nQuestion: {flashcard.question}")
            choice = input("press \"y\" to see the answer:\npress \"n\" to skip:\npress \"u\" to update:\n")

            if choice == "y":
                print(f"Answer: {flashcard.answer}")
                self.learning_menu(flashcard)
                return True  # Processed card, so exit loop
            elif choice == "n":
                return False  # Skip card
            elif choice == "u":
                self.update_flashcard(flashcard)
                return True  # Card updated, so exit loop
            else:
                print(f"{choice} is not an option")

    def learning_menu(self, flashcard):
        while True:
            choice = input("press \"y\" if your answer is correct:\npress \"n\" if your answer is wrong:\n")

            if choice == "y":
                if flashcard.box < 3:
                    flashcard.box += 1  # Move to the next box
                    self.session.commit()
                else:
                    self.session.delete(flashcard)  # Delete from database if in box 3
                    self.session.commit()
                break
            elif choice == "n":
                flashcard.box = 1  # Reset to box 1 on incorrect answer
                self.session.commit()
                break
            else:
                print(f"{choice} is not an option")

    def update_flashcard(self, flashcard):
        while True:
            choice = input("press \"d\" to delete the flashcard:\npress \"e\" to edit the flashcard:\n")

            if choice == "d":
                self.session.delete(flashcard)
                self.session.commit()
                break
            elif choice == "e":
                new_question = input(f"current question: {flashcard.question}\nplease write a new question:\n").strip()
                if new_question:
                    flashcard.question = new_question

                new_answer = input(f"current answer: {flashcard.answer}\nplease write a new answer:\n").strip()
                if new_answer:
                    flashcard.answer = new_answer

                self.session.commit()
                break
            else:
                print(f"{choice} is not an option")

if __name__ == "__main__":
    app = FlashcardApp()
    app.main_menu()
