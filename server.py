"""FamilyCube"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User,Profile,Member,Event,Image

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def indexpage():
    """Indexpage."""

    return render_template("index.html")


@app.route('/register', methods=['GET'])
def register_form():
#     """Show form for user signup."""

    return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def register_process():
#     """Process registration."""

#     # Get form variables
    firstname= request.form["Firstname"]
    lastname = request.form["Lastname"]
    email = request.form["Email"]
    password = request.form["Password"]
    

    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {email} added.")
    return redirect("/login")


@app.route('/login', methods=['GET'])
def login_form():
#     """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
#     """Process login."""

#     # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    print(email,password)

    user = User.query.filter_by(email=email).first()
    print(user)
    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/homepage")

@app.route('/homepage')
def homepage():

    return render_template("home_page.html")







# @app.route('/logout')
# def logout():
#     """Log out."""

#     del session["user_id"]
#     flash("Logged Out.")
#     return redirect("/")





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
