from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Keys(db.Model):
    quiz_key = db.Column(db.Integer, primary_key=True)


class Quiz(db.Model):
    __tablename__ = "quizzes"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Integer, unique=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"))
    email_sent = db.Column(db.Boolean)
    completed = db.Column(db.Boolean)
    # Quizzes HAS MANY questions.
    # Candidate connectionhi

    def __init__(self, candidate_id, key, completed=0, email_sent=0):
        self.candidate_id = candidate_id
        self.completed = completed
        self.email_sent = email_sent
        self.key = key  # self.completed = done

    def __repr__(self):
        return f"{self.id}:{self.candidate_id}:{self.completed}"


# this is a table to relate two models Quiz with its Questions
class QuizQuestions(db.Model):
    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)


class QuestionModel(db.Model):
    __tablename__ = "question_table"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer(), unique=True)  # no need? just use id above
    question_label = db.Column(db.String())
    question_text = db.Column(db.String())
    answer = db.Column(db.String(), nullable=False)
    options = db.Column(db.String(), nullable=True)
    options1 = db.Column(db.String(), nullable=True)
    options2 = db.Column(db.String(), nullable=True)
    options3 = db.Column(db.String(), nullable=True)

    # Questions BELONG TO MANY quizzes

    def __init__(
        self,
        question_id,
        question_label,
        question_text,
        answer,
        options,
        options1,
        options2,
        options3,
    ):
        self.question_id = question_id
        self.question_label = question_label
        self.question_text = question_text
        self.answer = answer
        self.options = options
        self.options1 = options1
        self.options2 = options2
        self.options3 = options3

    def __repr__(self):
        return f"{self.question_text}:{self.question_id}:{self.answer}:{self.options1}:{self.options2}:{self.options3}"


class Answer(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    question_id = db.Column(
        db.Integer(),
        db.ForeignKey("question_table.id", ondelete="CASCADE"),
        nullable=False,
    )
    content = db.Column(db.String(), nullable=False)
    correct = db.Column(db.Boolean(), server_default="FALSE", nullable=False)

    question = db.relationship("QuestionModel")


class AnswerModel(db.Model):
    __tablename__ = "answer_table"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer())
    candidate_id = db.Column(db.Integer())
    question_label = db.Column(db.String())
    answer = db.Column(db.String())
    correct = db.Column(db.Boolean())

    def __init__(self, question_id, candidate_id, question_label, answer, correct):
        self.question_id = question_id
        self.candidate_id = candidate_id
        self.question_label = question_label
        self.answer = answer
        self.correct = correct

    def __repr__(self):
        return f"{self.answer}:{self.question_id}"


class CandidateModel(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"{self.name}:{self.email}"
