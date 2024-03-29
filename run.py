
from models import (
    db,
    QuestionModel,
    AnswerModel,
    Answer,
    Quiz,
    Keys,
    CandidateModel,
    QuizQuestions,
    QuizResults,
    Employer,
    User
)
import bs4 as bs
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import os
import random
import urllib.request, json
from flask_mail import Mail, Message
import html
import time
from sqlalchemy.sql.expression import func



# Launch FLASK app
app = Flask(__name__)

app.secret_key = "my_secret_key"

# configure SQL
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL2"
)  # "sqlite:///quizgame.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# for email send function
# USERNAME: 'synergysimulator@gmail.com' PW "qnwgsktqadivsdcy"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "synergysimulator@gmail.com"
app.config["MAIL_PASSWORD"] = "qnwgsktqadivsdcy"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True  # True if Port = 465
mail = Mail(app)

# http://getskeleton.com/
# https://opentdb.com/api_config.php

# export DATABASE_URL2='sqlite:///quizgame.db'
# os.system(DATABASE_URL2='sqlite:///quizgame.db')
# python3 run.py


# instantiate login manager for flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# simple key generator utility for quizzes.
def genKey():
    """
    This function Generates a random value to be used as the key for a test access code
    :return:
    """
    return random.randint(1000000, 4000000)


# retrieve questions from 3rd party API (Open Trivia Database)
def getQuestions(qty):
    global QUESTIONNUMBER
    baseUrl = "https://opentdb.com/api.php?amount=10"
    example = "https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=multiple"
    specificUrl = "https://opentdb.com/api.php?amount=10&category=18&difficulty=medium&type=multiple"
    alternate = "https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=multiple&encode=base64"
    alternate2 = "https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=multiple&encode=url3986"
    with urllib.request.urlopen(example) as url:
        data = json.loads(url.read().decode())
        print(data)
    QUESTIONNUMBER = 8888
    qnum = QUESTIONNUMBER + 1
    for eachQ in data["results"]:
        print(eachQ)
        question = QuestionModel(
            question_id=qnum,
            question_label=html.unescape(eachQ["category"]),
            question_text=html.unescape(eachQ["question"]),
            answer=html.unescape(eachQ["correct_answer"]),
            options1=str(html.unescape(eachQ["incorrect_answers"][0])),
            options2=str(html.unescape(eachQ["incorrect_answers"][1])),
            options3=str(html.unescape(eachQ["incorrect_answers"][2])),
        )
        qnum += 1
        db.session.add(question)
    db.session.commit()

    return redirect("/questions")


# Retrieves a single question by ID
def get_question(id):
    return QuestionModel.query.filter_by(question_id=id).first()


# send a candidate a quiz key via email.
# @param {string} recpEmail - the candidates email.
# @param {int} quizID - the quiz id
def emailWork(email_type, quizID, recpEmail):
    # msg = Message
    boss = "synergysimulator@gmail.com"
    if email_type == "inbound":
        msg = Message("Hello", sender="synergysimulator@gmail.com", recipients=[recpEmail])
        msg.body = f"Hello {recpEmail}, your Quiz is ready from Synergy Simulator: {quizID}"
    elif email_type == "quiz_done":
        msg = Message("Hello", sender="synergysimulator@gmail.com", recipients=[boss])
        msg.body = f"Hello {recpEmail}, has finished their Synergy Simulator Quiz ID: {quizID}"
    mail.send(msg)
    return True


# Testing purposes only
# print(f"Current Working Directory = {os.getcwd()}")
# os.chdir(".")
# print(os.getcwd())


# CREATE IF NOT EXISTS
@app.before_first_request
def create_table():
    db.create_all()


# Main route.
#  Displays the home template.
@app.route("/")
def index():
    greetings = """QUIZLET from OSU...
    This app is expressly for the testing employment candidates."""
    greetings2 = "I am a..."
    sketch = "static/images/Synergy_Simulator.png"
    sketch2 = "static/images/plane.jpg"
    authors = "© 2022 Elizabeth Ponce & Andrea Hamilton, All rights reserved"
    return render_template(
        "home.html",
        greetings=greetings,
        greetings2=greetings2,
        image2=sketch,
        image3=sketch2,
        authors=authors,
    )


# About route.
#  displays image template.
@app.route("/about")
def about():
    greetings = """This app is expressly for the purpose Oregon State University's Capstone 
    Project"""
    detail = "Team members, Elizabeth Ponce & Andrea Hamilton are both local " \
             "to Portland, Oregon. Elizabeth works as a System Engineer at " \
             "Airbnb. Andrea works as a Technical Project Manager at Network Redux." \
             "They both enjoy learning new technologies and enjoying all that Portland has to offer."
    sketch = "static/images/brooke-cagle-g1Kr4Ozfoac-unsplash.jpg"

    return render_template(
        "image.html", greetings=greetings, detail=detail, image=sketch
    )


# Help route.
#  displays image template.
@app.route("/help")
def help():
    greetings = """...HELP, HELP, HELP..."""

    detail = "All the help you will ever need. Page under construction."
    sketch = "static/images/lasse-jensen-mPr2sCjuKAo-unsplash.jpg"

    return render_template(
        "image.html", greetings=greetings, detail=detail, image=sketch
    )


# Contact route.
#  displays image template.
@app.route("/contact")
def contact():
    greetings = """...CONTACT..."""

    detail = "All the contact you will ever need. Page under construction"
    sketch = "static/images/lasse-jensen-mPr2sCjuKAo-unsplash.jpg"

    return render_template("image.html", greetings=greetings, detail=detail, image=sketch)


# candidates route.
# displays candidate temple.
@app.route("/candidates")
def candidates():
    greetings = """Welcome Candidates!"""

    detail = (
        "We are excited for you to take the next steps in your " "employment journey."
    )

    return render_template("candidate.html", greetings=greetings, detail=detail)


# employer route.
# displays employer route.
@app.route("/employer")
def index6():
    greetings = """Welcome Employer!"""

    detail = (
        "Please select from the following options to find the candidate "
        "of your dreams"
    )
    #
    QuestionModel.query.delete()
    getQuestions(10)

    return render_template("employer.html", greetings=greetings, detail=detail)


# Makequiz route.
#  Accepts either GET or POST request.
#  GET: gets all quizzes; displays makeQuiz template.
#  POST: processes form input, and generates a new quiz for a given candidate. redirects back to Makequiz (quiz) route
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
        time_limit = request.form['timeLimit']
        if candidate_id == "*":
            flash("There are no candidates registered.")
            abort(422)

        candidate = CandidateModel.query.filter(
            CandidateModel.id == candidate_id
        ).first()
        print(candidate)
        new_quiz = Quiz(candidate_id=candidate.id, key=genKey(), time_limit=time_limit)
        db.session.add(new_quiz)
        db.session.commit()
        flash(f"Successfully created a quiz for {candidate.name}")

        return redirect(url_for("quiz"))


# RETRIEVE LIST OF QUESTIONS
@app.route("/candidate/<int:candidate_id>/quiz/<int:quiz_id>")
def RetrieveQuestionsList(candidate_id, quiz_id):
    # Get all stored questions.
    questions = QuestionModel.query.all()
    # get the quiz from db by id.
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


# add_questions route.
#  takes a list of questions and associates them with a given quiz and given candidate.
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

    result = emailWork("inbound", candidate_quiz.key, candidate.email )

    if result:
        # db.session.refresh(candidate_quiz_query)
        candidate_quiz.email_sent = 1
        db.session.commit()

    return redirect(url_for("quiz"))


# candidate/quiz route.
# Candidate requests quiz assigned to them to take.
@app.route("/candidate/quiz", methods=("GET", "POST"))
def retrieve_quiz():
    if request.method == "GET":
        return render_template("take_quiz.html")
    elif request.method == "POST":
        candidate_email = request.form["email"]
        quiz_key = request.form["key"]
        quiz_match = Quiz.query.filter(Quiz.key == quiz_key).first()
        candidate = CandidateModel.query.filter(
            CandidateModel.email == candidate_email
        ).first()
        if not candidate:
            flash("404: Candidate not found.")
            return abort(404)
        if not quiz_match:
            flash("404: quiz not found.")
            return abort(404)

        questions = (
            db.session.query(
                QuestionModel.id,
                QuestionModel.question_text,
                QuestionModel.answer,
                QuestionModel.options1,
                QuestionModel.options2,
                QuestionModel.options3,
            )
            .select_from(QuizQuestions)
            .filter(QuestionModel.id == QuizQuestions.question_id)
            .filter(QuizQuestions.quiz_id == quiz_match.id)
            .all()
        )

        processed_questions = []

        for question in questions:
            question_dict = {}
            options = [
                question.answer,
                question.options1,
                question.options2,
                question.options3,
            ]
            random.shuffle(options)
            question_dict["id"] = question.id
            question_dict["question"] = question.question_text
            question_dict["options"] = options
            processed_questions.append(question_dict)

        # quiz template will take candidate and quiz.
        return render_template(
            "quiz.html",
            questions=processed_questions,
            candidate=candidate,
            quiz=quiz_match,
        )


# process_quiz route.
# grabs questions for a given quiz; compares known answer to given answers. Marks the matching quiz to completed.
# TODO: add scoring
# TODO: email score to candidate.
# TODO: store general results in db. {QuizResults}
@app.route("/candidate/<int:candidate_id>/quiz/<int:quiz_id>/answers", methods=["POST"])
def process_quiz(candidate_id, quiz_id):
    questions = (
        db.session.query(
            QuestionModel.id, QuestionModel.question_text, QuestionModel.answer
        )
        .select_from(QuizQuestions)
        .filter(QuizQuestions.quiz_id == quiz_id)
        .filter(QuestionModel.id == QuizQuestions.question_id)
        .all()
    )

    # fetch the user so we can send them an email.
    candidate = CandidateModel.query.filter(CandidateModel.id == candidate_id).first()

    print('candidate: ', candidate.email)

    total_questions = 0
    right = 0
    wrong = 0

    time_elapsed = int(request.form['timespent'])

    print("TIMER: ", time_elapsed)

    for question in questions:
        form_answer = request.form[str(question.id)]
        correct = form_answer == question.answer
        print(form_answer)
        print(question.answer)

        if correct:
            print(f"You got {question.id} correct")
            right += 1
            total_questions += 1
            print(right)

        else:
            print(f"You got {question.id} wrong")
            wrong += 1
            total_questions += 1
            print(wrong)

    print(f"total correct, {right}")
    print(f"total incorrect, {wrong}")
    print(f"total questions, {total_questions}")
    # after processing the answers of the quiz, mark the quiz as completed.
    quiz_match = Quiz.query.filter(Quiz.id == quiz_id).first()

    quiz_match.completed = True
    print(f"quiz match id is {quiz_match.id}")
    print(f"quiz id is {quiz_id}")
    print(f"candidate id is {candidate_id}")

    score = right / total_questions
    new_results = QuizResults(quiz_id, candidate_id, right, wrong, time_elapsed, score)
   
    wrong = new_results.total_incorrect
    right = new_results.total_correct
    score = new_results.score
    new_results.quiz_id = quiz_match.id
    new_results.candidate_id = candidate_id

    db.session.add(new_results)
    db.session.commit()

    emailWork('quiz_done', quiz_match.key, candidate.email)

    flash("You will be contacted with the results of your quiz shortly.")
    return redirect("/")


# route from employers to return individual results of on candidate
@app.route("/results", methods=["GET", "POST"])
def get_results_for_candidate():
    if request.method == "GET":
        if request.method == "GET": # Screen for Employer to select candidate
            candidates = db.session.query(
                CandidateModel.id,
                CandidateModel.name,
                CandidateModel.email
            )
        return render_template("results.html", candidates=candidates)
    elif request.method == "POST":
        candidate_id = request.form["name"]
        print(f"candidate_id = {candidate_id}")
        candidate = CandidateModel.query.filter(CandidateModel.id == candidate_id).first()
        print(f"candidate = {candidate.id}")
        quiz_for_candidate = QuizResults.query.filter(QuizResults.candidate_id == candidate.id).first()
        print(f"lala {quiz_for_candidate}")
        if quiz_for_candidate:
            print(f"do_this = {quiz_for_candidate}")
            print(f"candidate result for quiz id is{quiz_for_candidate.candidate_id} ")
        if not quiz_for_candidate:
            return abort(404)
        return render_template("candidate_results.html", quiz_for_candidate=quiz_for_candidate, candidate=candidate)


@app.route("/allresults", methods=["GET"])
def get_results_for_all_candidates():
    if request.method == "GET":
        results = db.session.query(
            QuizResults.id,
            QuizResults.quiz_id,
            QuizResults.candidate_id,
            QuizResults.candidate_id,
            QuizResults.score,
        )
        
        candidates = db.session.query(
            CandidateModel.id,
            CandidateModel.name,
            CandidateModel.email
        )
        
        if candidates:
            if results:
                return render_template("all_candidate_results.html", candidates=candidates, results=results)
             

# DELETE CANDIDATE 
@app.route("/deleteCandidate", methods=["GET", "POST"])
def delete_candidate():
 
    if request.method == "GET":
        candidates = db.session.query(
            CandidateModel.id,
            CandidateModel.name,
            CandidateModel.email
        )
        return render_template("/listCandidates.html", candidates=candidates)
    if request.method == "POST":
        candidateToDelete = request.form["candidateToDelete"]
        print(f"candidate to delete is {candidateToDelete}")
        candidateToDelete2 = int(candidateToDelete)
        print(f"candidatetodelete2 is {candidateToDelete2}")
        delete_me = CandidateModel.query.filter(CandidateModel.id==candidateToDelete).first()
        if delete_me:
            db.session.delete(delete_me)
            db.session.commit()
            flash("You have deleted the selected Candidate.")
            return redirect("/employer")
        abort(404)
        
   
# UPDATE CANDIDATE 
@app.route("/updateCandidate", methods=["GET","POST"])
def update_candidate():
 
    if request.method == "GET": # Screen for Employer to select candidate
        candidates = db.session.query(
            CandidateModel.id,
            CandidateModel.name,
            CandidateModel.email
        )
        return render_template("/updateCandidate.html", candidates=candidates) #update candadiatl html and list of candidates
    elif request.method == "POST": # Employer has selected candidate
        candidate_id = request.form["candidateToUpdate"]
        candidate = db.session.query(
            CandidateModel.id,
            CandidateModel.name,
            CandidateModel.email
        ).filter(CandidateModel.id==candidate_id).first()
        return render_template("/editCandidate.html", candidateToUpdate=candidate) #update candadiatl html and list of candidates


@app.route("/editCandidate", methods=["GET","POST"])
def edit_candidate():
    if request.method == "GET":
        candidate_id = request.form["candidateToUpdate"]
        candidate = db.session.query(
            CandidateModel.id,
            CandidateModel.name,
            CandidateModel.email
        ).filter(CandidateModel.id==candidate_id).first()
        return render_template("/editCandidate.html", candidateToUpdate=candidate)
    if request.method == "POST":
       
        candidate_id = request.form["candidate_id"]
      
        update_me = CandidateModel.query.filter(CandidateModel.id==candidate_id).first()
        if update_me:
           
            candidateToUpdate = CandidateModel.query.filter(CandidateModel.id==update_me.id).first()
            candidateToUpdate.name = request.form["candidate_name"]
            candidateToUpdate.email = request.form["candidate_email"]
            db.session.commit()
            flash("You have updated the selected Candidate's Information.")
            return redirect("/employer")

        abort(404)


# register_user route.
# user registration.
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

@login_manager.user_loader
def get(id):
    return Employer.query.get(id)


@app.route('/login',methods=['GET','POST'])
def employer_login_():
    if request.method == "GET":
        return render_template('emp_login.html')
    if request.method == "POST": 
        email = request.form['email']
        password = request.form['password']
        employer = Employer.query.filter_by(email=email).first()
        if employer:
            login_user(employer)
            return redirect('/employer')
        else:
            flash("No user with those credentials, please register.", "error")
            return redirect('/signup')

@app.route("/signup",methods=["GET","POST"])
def emp_signup():
    if request.method == "GET":
        return render_template("emp_signup.html")
    if request.method == "POST": 
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        employer = Employer(username=username,email=email,password=password)
        db.session.add(employer)
        db.session.commit()
        employer = Employer.query.filter_by(email=email).first()
        login_user(employer)
        return redirect("/login")

@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')



# page_not_found error handler page.
#  display generic 404 page when 404 code is sent.
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":

    app.directory = "./"
    app.run(host="127.0.0.1", port=5000, debug=True)

    # https://www.askpython.com/python-modules/flask/flask-flash-method
    # export DATABASE_URL2='sqlite:///quizgame.db'
    # python3 run.py
