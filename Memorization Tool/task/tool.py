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
                question = input("Question:\n ").strip()
                while not question:
                    print("Question cannot be empty.")
                    question = input("Question:\n ").strip()

                answer = input("Answer:\n ").strip()
                while not answer:
                    print("Answer cannot be empty.")
                    answer = input("Answer:\n ").strip()

                new_flashcard = Flashcard(question=question, answer=answer)
                self.session.add(new_flashcard)
                self.session.commit()
            elif choice == "2":
                return
            else:
                print(f"{choice} is not an option")

    def practice_flashcards(self):
        flashcards = self.session.query(Flashcard).all()
        if not flashcards:
            print("There are no flashcards to practice!")
            return

        for flashcard in flashcards:
            while True:
                print(f"\nQuestion: {flashcard.question}")
                choice = input("press \"y\" to see the answer:\npress \"n\" to skip:\npress \"u\" to update:\n ")

                if choice == "y":
                    print(f"Answer: {flashcard.answer}")
                    break
                elif choice == "n":
                    break
                elif choice == "u":
                    self.update_flashcard(flashcard)
                    break
                else:
                    print("Wrong option. Try again.")

    def update_flashcard(self, flashcard):
        while True:
            choice = input("press \"d\" to delete the flashcard:\npress \"e\" to edit the flashcard:\n ")

            if choice == "d":
                self.session.delete(flashcard)
                self.session.commit()
                break
            elif choice == "e":
                # Edit question
                new_question = input(f"current question: {flashcard.question}\nplease write a new question:\n ").strip()
                if new_question:
                    flashcard.question = new_question

                # Edit answer
                new_answer = input(f"current answer: {flashcard.answer}\nplease write a new answer:\n ").strip()
                if new_answer:
                    flashcard.answer = new_answer

                # Commit changes
                self.session.commit()
                break
            else:
                print("Wrong option. Try again.")

if __name__ == "__main__":
    app = FlashcardApp()
    app.main_menu()