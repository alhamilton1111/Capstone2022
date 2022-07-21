import csv
from models import db, AnswerModel, QuestionModel
import os


def main():
    os.remove("quizgame.db")
    db.create_all()
    question_table()
    answer_table()


def question_table():
    with open("question_table.csv") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        for idx, row in enumerate(csv_reader):
            if idx != 0:
                (
                    id,
                    question_id,
                    question_label,
                    question_text,
                    answer,
                    options,
                    options1,
                    options2,
                    options3,
                ) = row
                question = QuestionModel(
                    question_id,
                    question_label,
                    question_text,
                    answer,
                    options,
                    options1,
                    options2,
                    options3,
                )
                db.session.add(question)
                db.session.commit()


def answer_table():
    with open("answer_table.csv") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        for idx, row in enumerate(csv_reader):
            if idx != 0:
                id, question_id, candidate_id, question_label, answer, correct = row
                graded_answer = AnswerModel(
                    question_id, candidate_id, question_label, answer, int(correct)
                )
                db.session.add(graded_answer)
                db.session.commit()


if __name__ == "__main__":
    main()
