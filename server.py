"""FamilyCube"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User,Profile,Member,Event,Image
from datetime import datetime

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def indexpage():
    """Indexpage."""
    app.logger.info("Hello World")
    if session.get("user_id") is not None:
        return redirect("/homepage")
    else:
        return render_template("index.html")


@app.route('/register', methods=['GET'])
def register_form():
#     """Show form for user signup."""

    return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def register_process():
#     """Process registration."""

#     # Get form variables
    first_name = request.form.get("Firstname")
    last_name = request.form.get("Lastname")
    email = request.form.get("Email")
    password = request.form.get("Password")
    

    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    

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
    email = request.form.get("email")
    password = request.form.get("password")
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

    first3_events = latest_events()
    return render_template("home_page.html",events=first3_events)

@app.route('/profile', methods=['GET'])
def profile_page():
    """Show form for user to update profile."""

    return render_template("profile.html")


@app.route('/profile', methods=['POST'])
def profile_update():
    """Profile updation process"""

    first_name= request.form.get("Firstname")
    last_name = request.form.get("Lastname")
    display_name = request.form.get("Displayname")
    email = request.form.get("Email")
    phonenumber = request.form.get("Phonenumber")
    date_of_birth_str = request.form.get("Birthday")
    date_of_birth = datetime.strptime(date_of_birth_str,'%Y-%m-%d')
    address_1 = request.form.get("Address1")
    address_2 = request.form.get("Address2")
    city = request.form.get("City")
    state = request.form.get("State")
    zipcode = request.form.get("Zipcode")
    country = request.form.get("Country")
    married = request.form.get("Marital_Status")
    marriage_date_str = request.form.get("Marriage_Anniversary")
    marriage_date = datetime.strptime(marriage_date_str,'%Y-%m-%d')
    kids = int(request.form.get("Kids"))
    userid = session["user_id"]
    

    user_profile = Profile(display_name=display_name, user_id=userid, email=email,phonenumber=phonenumber,date_of_birth=date_of_birth,
                          address_1=address_1, address_2=address_2, city=city, state=state, zipcode=zipcode, 
                          country=country, married=married, marriage_date=marriage_date, kids=kids)
    db.session.add(user_profile)
    db.session.commit()
    text = f"Birthday for {first_name} {last_name}"
    user_event = Event(profile_id=user_profile.profile_id,event_type='Birthday',event_date=date_of_birth,event_text=text)
    db.session.add(user_event)
    db.session.commit()

    if married == 'yes':
        first_name= request.form.get("Spouse_Firstname")
        last_name = request.form.get("Spouse_Lastname")
        #display_name = request.form.get("Spouse_Displayname")
        email = request.form.get("Spouse_Email")
        phonenumber = request.form.get("Spouse_Phonenumber")
        date_of_birth_str = request.form.get("Spouse_Birthday")
        date_of_birth = datetime.strptime(date_of_birth_str,'%Y-%m-%d')
        marriage_date_str = request.form.get("Spouse_Marriage_Anniversary")
        marriage_date = datetime.strptime(marriage_date_str,'%Y-%m-%d')
        relation = "Spouse"

        spouse_profile = Member(profile_id=user_profile.profile_id,first_name=first_name, last_name=last_name,email=email,
                                phonenumber=phonenumber, date_of_birth=date_of_birth, marriage_date=marriage_date,
                                relation=relation)
        db.session.add(spouse_profile)
        db.session.commit()
        #Add birthday and marriage anniversary to events
        text = f"Birthday for {first_name} {last_name}"
        spouse_db_event = Event(profile_id=user_profile.profile_id,member_id=spouse_profile.member_id,event_type='Birthday',event_date=date_of_birth,event_text=text)
        db.session.add(spouse_db_event)
        text = f"Marriage Anniversary for {first_name} {last_name} and {user_profile.fullname}"
        marriage_event = Event(profile_id=user_profile.profile_id,member_id=spouse_profile.member_id,event_type='Marriage_Anniversary',event_date=marriage_date,event_text=text)
        db.session.add(marriage_event)
        db.session.commit()
    
    if kids > 0:
        first_name= request.form.get("Kid_Firstname")
        last_name = request.form.get("Kid_Lastname")
        #display_name = request.form.get("Kid_Displayname")
        email = request.form.get("Kid_Email")
        phonenumber = request.form.get("Kid_Phonenumber")
        date_of_birth_str = request.form.get("Kid_Birthday")
        date_of_birth = datetime.strptime(date_of_birth_str,'%Y-%m-%d')
        relation = request.form.get("Kid_Relation")

        kid_profile = Member(profile_id=user_profile.profile_id,first_name=first_name, last_name=last_name,email=email,
                                phonenumber=phonenumber, date_of_birth=date_of_birth,relation=relation)

        db.session.add(kid_profile)
        db.session.commit()
        text = f"Birthday for {first_name} {last_name}"
        kid_db_event = Event(profile_id=user_profile.profile_id,member_id=kid_profile.member_id,event_type='Birthday',event_date=date_of_birth,event_text=text)
        db.session.add(kid_db_event)
        db.session.commit()

    return redirect("/homepage")
    
@app.route('/events')
def show_events():
#     """Show events."""

    userid = session.get("user_id")
    app.logger.info(userid)
    if userid is not None:
        events = db.session.query(Event).join(Profile).filter(Profile.user_id == userid).filter(Profile.profile_id == Event.profile_id).order_by(Event.event_date).all()
        app.logger.info(events)
        return render_template("events.html",events=events)

@app.route('/photos')
def upload_photos():
    """Upload photos"""

    return render_template("photos.html")

@app.route('/videos')
def upload_videos():
    """Upload Videos"""

    return render_template("videos.html")

@app.route('/calendar')
def calendar_event():
    """ View abd update calendar for events"""

    return render_template("calendar.html")

@app.route('/calendar', methods=['POST'])
def add_calendar_event():
    """  add a new event for calendar"""

    event_type = request.form.get("event_type")
    event_text = request.form.get("event_text")
    event_date_str = request.form.get("event_date")
    event_date = datetime.strptime(event_date_str,'%Y-%m-%d')
    user_id = session["user_id"]
    profile = Profile.query.filter_by(user_id=user_id).first()
    db_event = Event(profile_id=profile.profile_id,event_type=event_type,event_date=event_date,event_text=event_text)
    db.session.add(db_event)
    db.session.commit()
    return redirect("/homepage")



@app.route('/logout')
def logout():
    """Log out."""
    if session["user_id"] is not None:
        del session["user_id"]
        flash("Logged Out.")
    return redirect("/")


def latest_events():
#     """Get latest 3 events."""

    userid = session.get("user_id")
    if userid is not None:
        events = db.session.query(Event).join(Profile).filter(Profile.user_id == userid).filter(Profile.profile_id == Event.profile_id).order_by(Event.event_date).limit(3).all()
        app.logger.info(events)
        return events
    else:
        return None





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
