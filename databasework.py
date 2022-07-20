from sqlalchemy.orm import Session

from models import db, QuestionModel, AnswerModel
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quizgame.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# <form action='' method="POST">
#     <p>question ID <input type="integer" name="question_id" /></p>
#     <p>question label <input type="text" name="question_label" /></p>
#     <p>question text <input type="text" name="question_text" /></p>
#     <p>answer <input type="text" name="answer" /></p>
#     <p>options <input type="text" name="options" /></p>
#     <p><input type="submit" value="Submit" /></p>
# </form>
Q1 = QuestionModel(123, "fred", "best variable name ever", "smith",
                   "a-b-c")

# db.session.add(Q1)
# db.session.commit()
print("done",Q1.question_label)

db.session.query('question_table').all()