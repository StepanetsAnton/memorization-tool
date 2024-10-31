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

                new_flashcard = Flashcard(question=question, answer=answer)
                self.session.add(new_flashcard)
                self.session.commit()

            elif choice == "2":
                break
            else:
                print(f"{choice} is not an option")

    def practice_flashcards(self):
        flashcards = self.session.query(Flashcard).all()
        if not flashcards:
            print("\nThere is no flashcard to practice!")
            return

        for flashcard in flashcards:
            print(f"\nQuestion: {flashcard.question}")
            choice = input("Please press \"y\" to see the answer or press \"n\" to skip:\n")

            if choice == "y":
                print(f"Answer: {flashcard.answer}")
            elif choice == "n":
                continue
            else:
                print(f"{choice} is not an option. Wait for the right input.")


if __name__ == "__main__":
    app = FlashcardApp()
    app.main_menu()