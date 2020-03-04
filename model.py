
from flask_sqlalchemy import SQLAlchemy
import datetime



# Instantiate a SQLAlchemy object. We need this to create our db.Model classes.
db = SQLAlchemy()


##############################################################################


class User(db.Model):
    """Data model for a User."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,primary_key= True,
                           autoincrement=True,nullable=False,)
    email = db.Column(db.String(100), nullable=False,unique=True,)
    password = db.Column(db.String(25),nullable=False,)
    



    # Define your columns and/or relationships here

    def __repr__(self):
        """Return a user-readable representation of a User."""

        return f"<User user_id={self.user_id} email={self.email} password={self.password}>"

        


class Profile(db.Model):
    """Data model for profile."""

    __tablename__ = "profiles"

    # Define your columns and/or relationships here
    profile_id = db.Column(db.Integer,primary_key=True,autoincrement=True,
                                    nullable=False,)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    display_name= db.Column(db.String(50),nullable=True,)
    address_1 = db.Column(db.String(50),nullable=False,)
    address_2 = db.Column(db.String(50),nullable=True,)
    city = db.Column(db.String(25),nullable=False,)
    State = db.Column(db.String(25),nullable=False,)
    zipcode = db.Column(db.String(25),nullable=False,)
    country = db.Column(db.String,nullable=False,)

    users = db.relationship("User", backref="profiles")




    def __repr__(self):
        """Return a profile-readable representation of a profile."""

        return f"<Profile profile_id={self.profile_id} user_id={self.user_id} display_name={self.display_name}>"


class Member(db.Model):
    """Data model for members in the family."""

    __tablename__ = "members"

    # Define your columns and/or relationships here
    member_id = db.Column(db.Integer,primary_key=True,autoincrement=True,
                                    nullable=False,)
    profile_id = db.Column(db.Integer,db.ForeignKey('profiles.profile_id'))
    first_name = db.Column(db.String(50),nullable=False,)
    last_name = db.Column(db.String(50),nullable=False,)
    date_of_birth = db.Column(db.datetime,nullable=False,)
    phonenumber = db.Column(db.Integer,nullable=False,)
    email = db.Column(db.String(25),nullable=False,)


    profiles = db.relationship("Profile", backref="members")




    def __repr__(self):
        """Return a member-readable representation of a member."""

        return f"<Member member_id={self.member_id} profile_id={self.profile_id} first_name={self.first_name} last_name={self.last_name} date_of_birth={self.date_of_birth} phonenumber={self.phonenumber} email={self.email}>"


class Event(db.model):

    __tablename__ = "events"

    event_id = db.Column(db.Integer,primary_key=True,autoincrement=True,
                                    nullable=False,)
    profile_id = db.Column(db.Integer,db.ForeignKey('profiles.profile_id'))
    member_id = db.Column(db.Integer,ForeignKey('members.member_id'))
    event_type = db.Column(db.String(50),nullable=False,)
    event_date = db.Column(db.datetime,nullable=True,)
    event_location = db.Column(db.String(50),nullable=True,)
    event_text = db.Column(db.String,nullable=True,)

    profiles = db.relationship("Profile", backref="events")
    members = db.relationship("Member", backref="events")

    def __repr__(self):
        """Return a event-readable representation of a event."""

        return f"<Event event_id={self.event_id} profile_id={self.profile_id} member_id={self.member_id} event_type={self.event_type} event_date={self.event_date} event_location={self.event_location}>"


class Image(db.model):

    __tablename__ = "images"

    # Define your columns and/or relationships here
    image_id = db.Column(db.Integer,primary_key=True,autoincrement=True,
                                    nullable=False,)
    profile_id = db.Column(db.Integer,db.ForeignKey('profiles.profile_id'))
    event_id = db.Column(db.Integer,db.ForeignKey('events.event_id'))
    image = db.Column(db.image,nullable=True,)
    file_name = db.Column(db.String)
    album_name = db.Column(db.String(30),nullable=False,)
    
    
    profiles = db.relationship("Profile", backref="images")
    events = db.relationship("Event", backref="images")



    def __repr__(self):
        """Return a image-readable representation of a image."""

        return f"<Image image_id={self.image_id} profile_id={self.profile_id} event_id={self.event_id} album_name={self.album_name}>"



class Relationship(db.model):

    __tablename__ = "relationships"

    relationship_id = db.Column(db.Integer,primary_key=True,autoincrement=True,
                                    nullable=False,)
    member_one_id = db.Column(db.Integer,ForeignKey('members.member_id'))
    member_two_id = db.Column(db.Integer,ForeignKey('members.member_id'))

    members = db.relationship("Member", backref="realationships")

    def __repr__(self):
        """Return a relationship-readable representation of a relationship."""

        return f"<Relationship relationship_id={self.relationship_id} member_one_id={self.member_one_id} member_two_id={self.member_two_id}>"


class Relation(db.model):

    __tablename__ = "relations"

    relation_id = db.Column(db.Integer,primary_key=True,autoincrement=True,
                                    nullable=False,)
    relation = db.Column(db.String(25),nullable=True,)

    def __repr__(self):

        return f"<Relation relation_id={self.relation_id} relation={self.relation}>"
    
##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///users"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB")
