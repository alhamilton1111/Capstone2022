# importing Flask and other modules
from flask import Flask, request, render_template

# Flask constructor
app2 = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function
@app2.route('/', methods =["GET", "POST"])
def dfg2():
	if request.method == "POST":
		# getting input with name = fname in HTML form
		first_name = request.form.get("fname")
		# getting input with name = lname in HTML form
		last_name = request.form.get("lname")
		return "Your name is "+first_name + last_name
	return render_template("form2.html")

if __name__=='__main__':
	app2.run()
