from models import (
    db,
    QuestionModel,
    AnswerModel,
    Answer,
    Quiz,
    Keys,
    CandidateModel,
    QuizQuestions,
)
from flask import Flask, render_template, request, redirect, url_for, flash, abort
import os
import random
import urllib.request, json
from flask_mail import Mail, Message
from create_db import main

app = Flask(__name__)

app.secret_key = "my_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL2"
)  # "sqlite:///quizgame.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# for email send function
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "synergysimulator@gmail.com"
app.config["MAIL_PASSWORD"] = "uujjnzsnnngjkkhg"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True  # True if Port = 465
mail = Mail(app)

# http://getskeleton.com/
# https://opentdb.com/api_config.php

# export DATABASE_URL2='sqlite:///quizgame.db'
# os.system(DATABASE_URL2='sqlite:///quizgame.db')
# python3 run.py
# global QUESTIONNUMBER


def genKey():
    """
    This function Generates a random value to be used as the key for a test access code
    :return:
    """
    return random.randint(1000000, 4000000)


def getQuestions(qty):
    global QUESTIONNUMBER
    baseUrl = "https://opentdb.com/api.php?amount=10"
    example = "https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=multiple"
    specificUrl = "https://opentdb.com/api.php?amount=10&category=18&difficulty=medium&type=multiple"
    with urllib.request.urlopen(example) as url:
        data = json.loads(url.read().decode())
        print(data)
    QUESTIONNUMBER = 8888
    qnum = QUESTIONNUMBER + 1
    for eachQ in data["results"]:
        print(eachQ)
        question = QuestionModel(
            question_id=qnum,
            question_label=eachQ["category"],
            question_text=eachQ["question"],
            answer=eachQ["correct_answer"],
            options1=str(eachQ["incorrect_answers"][0]),
            options2=str(eachQ["incorrect_answers"][1]),
            options3=str(eachQ["incorrect_answers"][2]),
        )
        qnum += 1
        db.session.add(question)
    db.session.commit()

    return redirect("/questions")


def get_question(id):
    return QuestionModel.query.filter_by(question_id=id).first()


def emailWork(recpEmail, quizID):
    # msg = Message('Hello', sender='medleaconsulting@gmail.com', recipients=['davegillis4@gmail.com'])
    msg = Message("Hello", sender="medleaconsulting@gmail.com", recipients=[recpEmail])
    msg.body = f"Hello {recpEmail}, your Quiz is ready from Synergy Simulator: {quizID}"

    # You can also use msg.html to send html templates!
    # Example:
    # msg.html = render_template("hello.html") # Template should be in 'templates' folder

    mail.send(msg)
    return True


print(f"Current Working Directory = {os.getcwd()}")
os.chdir(".")
print(os.getcwd())


# CREATE IF NOT EXISTS
@app.before_first_request
def table():
    #  db.create_all()
    main()


@app.route("/")
def index():
    greetings = """QUIZLET from OSU...
    This app is expressly for the testing employment candidates."""
    greetings2 = "I am a..."
    test2 = "way too much fun....."
    ccValue = "349950727078541"
    test2 = genKey()
    test3 = genKey()
    sketch = "static/images/Synergy_Simulator.png"
    sketch2 = "static/images/plane.jpg"
    authors = "© 2022 Elizabeth Ponce & Andrea Hamilton, All rights reserved"
    return render_template(
        "home.html",
        greetings=greetings,
        greetings2=greetings2,
        dobie=test2,
        dibs=test3,
        image2=sketch,
        image3=sketch2,
        authors=authors,
    )


@app.route("/about")
def about():
    greetings = """QUIZLET from OSU...
    This app is expressly for the purpose of getting an A
    in our Capstone Project"""
    detail = " Please Vote with your usage.... the more hits the better...."
    sketch = "static/images/brooke-cagle-g1Kr4Ozfoac-unsplash.jpg"

    return render_template(
        "image.html", greetings=greetings, detail=detail, image=sketch
    )


@app.route("/help")
def help():
    greetings = """...HELP, HELP, HELP..."""

    detail = "All the help you will ever need"
    sketch = "static/images/lasse-jensen-mPr2sCjuKAo-unsplash.jpg"

    return render_template(
        "image.html", greetings=greetings, detail=detail, image=sketch
    )


@app.route("/contact")
def contact():
    greetings = """...CONTACT..."""

    detail = "All the touch you will ever need"

    return render_template("image.html", greetings=greetings, detail=detail)


@app.route("/candidates")
def candidates():
    greetings = """Welcome Candidates!"""

    detail = (
        "We are excited for you to take the next steps in your " "employment journey."
    )

    return render_template("candidate.html", greetings=greetings, detail=detail)


@app.route("/sendemail", methods=["GET", "POST"])
def sendemail():
    greetings = """Email Sent!"""

    detail = "SENDING EMail to: "
    emailID = "davegillis4@gmail.com"
    quizzer = (
        genKey()
    )  # this needs to move to quiz gen page and be sent to this variable
    goodNews = emailWork(emailID, quizzer)

    return render_template(
        "emailsent.html",
        greetings=greetings,
        detail=detail,
        emailTo=emailID,
        quizID=quizzer,
        finish=goodNews,
    )


@app.route("/employer")
def index6():
    greetings = """Welcome Employer!"""

    detail = (
        "Please select from the following options to find the candidate "
        "of your dreams"
    )
    # DFG
    QuestionModel.query.delete()
    getQuestions(10)

    return render_template("employer.html", greetings=greetings, detail=detail)


@app.route("/makeQuiz", methods=["GET", "POST"])
def quiz():
    if request.method == "GET":
        greetings = """Make a Quiz"""

        detail = "Please select from the following questions to customize your " "quiz."

        all_candidates = CandidateModel.query.all()
        questions = QuestionModel.query.all()
        quizzes_query = db.session.query(Quiz, CandidateModel).join(
            CandidateModel, Quiz.candidate_id == CandidateModel.id
        )
        quizzes = quizzes_query.all()
        print(type(quizzes))
        return render_template(
            "makeQuiz.html",
            greetings=greetings,
            detail=detail,
            questions=questions,
            candidates=all_candidates,
            quizzes=quizzes,
        )
    elif request.method == "POST":
        candidate_id = request.form["candidate"]
        if candidate_id == "*":
            flash("There are no candidates registered.")
            abort(422)

        candidate = CandidateModel.query.filter(
            CandidateModel.id == candidate_id
        ).first()
        print(candidate)
        new_quiz = Quiz(candidate_id=candidate.id, key=genKey())
        db.session.add(new_quiz)
        db.session.commit()
        flash(f"Successfully created a quiz for {candidate.name}")

        return redirect(url_for("quiz"))


# CREATE VIEW -- TO REMOVE for FINAL submission -- (for testing only)
@app.route("/questions/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("createquestion.html")
    if request.method == "POST":
        checks = "Check all that apply:"
        question_id = request.form["question_id"]
        question_label = request.form["question_label"]
        question_text = request.form["question_text"]
        answer = request.form["answer"]
        options = request.form["options"]
        options1 = request.form["options1"]
        options2 = request.form["options2"]
        options3 = request.form["options3"]
        if question_label == checks:
            question = QuestionModel(
                question_id=question_id,
                question_label=question_label,
                question_text=question_text,
                answer=answer,
                options=options,
                options1=options1,
                options2=options2,
                options3=options3,
            )
        else:
            question = QuestionModel(
                question_id=question_id,
                question_label=question_label,
                question_text=question_text,
                answer=answer,
                options=options,
                options1=options1,
                options2=options2,
                options3=options3,
            )
        db.session.add(question)
        db.session.commit()
        return redirect("/questions")


# RETRIEVE LIST OF QUESTIONS
@app.route("/candidate/<int:candidate_id>/quiz/<int:quiz_id>")
def RetrieveQuestionsList(candidate_id, quiz_id):
    # Get all stored questions.
    questions = QuestionModel.query.all()
    # get the quiz from db by id.
    #  print(questions[0].question_text)
    # #    questions = [dict(q) for q in questions]
    # # print("trying to read DB")
    # return render_template("questionslist.html", questions=questions)
    candidate_quiz = Quiz.query.filter(Quiz.id == quiz_id).first()
    # get the candidate from db by id.
    candidate = CandidateModel.query.filter(CandidateModel.id == candidate_id).first()

    # TODO: get all questions already associated with this quiz.
    return render_template(
        "questionslist.html",
        quiz=candidate_quiz,
        questions=questions,
        candidate=candidate,
    )


@app.route("/candidate/<int:candidate_id>/quiz/<int:quiz_id>/add", methods=["POST"])
def add_questions(candidate_id, quiz_id):
    q_selection = request.form.getlist("questions")
    questions = QuestionModel.query.filter(
        QuestionModel.question_id.in_(q_selection)
    ).all()
    if not questions:
        flash("No questions found")
        abort(404)

    candidate = CandidateModel.query.filter(CandidateModel.id == candidate_id).first()
    candidate_quiz_query = Quiz.query.filter(Quiz.id == quiz_id)
    candidate_quiz = candidate_quiz_query.first()
    if not candidate_quiz:
        flash("404: Quiz not found.")
        abort(404)

    for question in questions:
        quiz_question = QuizQuestions(
            quiz_id=candidate_quiz.id, question_id=question.id
        )
        db.session.add(quiz_question)
    db.session.commit()

    result = emailWork(candidate.email, candidate_quiz.key)

    if result:
        # db.session.refresh(candidate_quiz_query)
        candidate_quiz.email_sent = 1
        db.session.commit()

    return redirect(url_for("quiz"))


# RETRIEVE SINGLE QUESTION
@app.route("/questions/<int:id>")
def RetrieveSingleQuestion(id):
    question = get_question(id)
    if question:
        return render_template("questions.html", question=question)
    return f"Question with id = {id} Doesn't exist"


# UPDATE QUESTION
@app.route("/questions/<int:id>/update", methods=["GET", "POST"])
def update(id):
    question = QuestionModel.query.filter_by(question_id=id).first()
    if request.method == "POST":
        if question:
            db.session.delete(question)
            db.session.commit()
            question_label = request.form["question_label"]
            question_text = request.form["question_text"]
            answer = request.form["answer"]
            options = request.form["options"]
            options1 = request.form["options1"]
            options2 = request.form["options2"]
            options3 = request.form["options3"]
            question = QuestionModel(
                question_id=id,
                question_label=question_label,
                question_text=question_text,
                answer=answer,
                options=options,
                options1=options1,
                options2=options2,
                options3=options3,
            )

            db.session.add(question)
            db.session.commit()
            return redirect(f"/questions/{id}")
        return f"Question with id = {id} Does not exist!"
    return render_template("update.html, question = question")


# DELETE QUESTION
@app.route("/questions/<int:id>/delete", methods=["GET", "POST"])
def delete_question(id):
    question = QuestionModel.query.filter_by(question_id=id).first()
    if request.method == "POST":
        if question:
            db.session.delete(question)
            db.session.commit()
            return redirect("/questions")
        abort(404)
    return render_template("delete.html")


# DELETE CANDIDATE -- TO DO
@app.route("/candidates/<int:id>/delete", methods=["GET", "POST"])
def delete_candidate(id):
    question = AnswerModel.query.filter_by(candidate_id=id).first()
    if request.method == "POST":
        if question:
            db.session.delete(question)
            db.session.commit()
            return redirect("/candidates")
        abort(404)
    return render_template("delete.html")


@app.route("/answerquestion/<int:candidate_id>/<int:id>", methods=["GET", "POST"])
def answer_question(candidate_id, id):
    # USER ASKED QUESTION
    question = get_question(id)
    while question is not None:
        # If question is a free form
        # render this template
        # if quetions is some other form
        # render other template
        # if question is this kind
        # render other
        # if other kind
        # render this
        checks = "Check all that apply:"
        free_form = "Input answer in text box:"
        boolean = "Boolean"
        mult_choice = "Multiple Choice"
        if request.method == "GET":
            if question.question_label == checks:
                options = question.options.split(",")
                return render_template(
                    "user_answer_check.html", question=question, options=options
                )
            elif question.question_label == free_form:
                return render_template("user_answer_free_form.html", question=question)
            elif question.question_label == boolean:
                options = question.options.split(",")
                return render_template(
                    "user_answer_t_or_f.html", question=question, options=options
                )

            elif question.question_label == mult_choice:
                options = question.options.split(",")
                return render_template(
                    "user_answer_mult_choice.html", question=question, options=options
                )
        # USER ANSWERS QUESTION
        id += 1  # increments to next question
        if question.question_label == checks:
            user_checks = request.form.getlist(
                "answer"
            )  # string, e.g., ["cookies","pies"]
            user_checks = ",".join(user_checks)  # now reads "cookies,pies"
            if question.answer == user_checks:
                correct = True
            else:
                correct = False
        # TO DO : refactor with the next 3 options
        elif question.question_label == free_form:
            if question.answer == request.form["answer"]:
                correct = True
            else:
                correct = False
        elif question.question_label == boolean:
            if question.answer == request.form["answer"]:
                correct = True
            else:
                correct = False
        elif question.question_label == mult_choice:
            if question.answer == request.form["answer"]:
                correct = True
            else:
                correct = False
        question_id = question.question_id
        question_label = question.question_label
        candidate_id = candidate_id
        answer = question.answer
        graded_answer = AnswerModel(
            question_id, candidate_id, question_label, answer, correct
        )
        print(correct)
        db.session.add(graded_answer)
        db.session.commit()
        return redirect(f"/answerquestion/{candidate_id}/{id}")
    return f"No question exists for question {id}"


@app.route("/register", methods=["GET", "POST"])
def register_user():
    print(request.method)
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        candidate = CandidateModel.query.filter(CandidateModel.email == email).first()

        if candidate:
            flash("User already registered", "error")
            return render_template("register.html"), 400

        new_candidate = CandidateModel(name, email)
        db.session.add(new_candidate)
        db.session.commit()
        flash("User successfully registered", "success")
        return redirect(url_for("candidates"))


@app.route("/quiz/<int:key>")
def take_quiz(key):
    return "you are taking a quiz."


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":

    app.directory = "./"
    app.run(host="127.0.0.1", port=5000, debug=True)

    # https://www.askpython.com/python-modules/flask/flask-flash-method  # Working to properly use FLASH

    # export DATABASE_URL2='sqlite:///quizgame.db'
    # python3 run.py
