import string
import random

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db

# Use-Datenbank


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def create_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Bauteildatenbak


class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    force = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    length = db.Column(db.Integer)
    roughness = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def seed(session):
        random_name = ''.join(random.choice(string.ascii_lowercase)
                              for i in range(8))
        tool = Tool(
            name=random_name,
            force=1,
            width=1,
            height=1,
            length=1,
            roughness=1,
            diameter=1,
        )
        session.add(tool)
        session.commit()



class FCT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    name = db.Column(db.Text)
    breite = db.Column(db.Integer)
    breite_ein = db.Column(db.Integer)
    hoehe = db.Column(db.Integer)
    hoehe_ein = db.Column(db.Integer)
    laenge = db.Column(db.Integer)
    laenge_ein = db.Column(db.Integer)
    rauheit = db.Column(db.Integer)
    rauheit_ein = db.Column(db.Integer)
    durchmesser = db.Column(db.Integer)
    durchmesser_ein = db.Column(db.Integer)
    alttechnologie = db.Column(db.Integer)


    def seed(session):
        random_name = ''.join(random.choice(string.ascii_lowercase)
                              for i in range(8))
        fct = FCT(
            name=random_name,
            position=1,
            breite=1,
            hoehe=1,
            laenge=1,
            rauheit=1,
            durchmesser=1,
            alttechnologie=1,
        )
        session.add(fct)
        session.commit()

class Technology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(), unique=True, nullable=True)
    alt_technology = db.Column(db.Integer)
    connection = db.Column(db.String())
    roughness_a = db.Column(db.Integer)
    roughness_b = db.Column(db.Integer)
    roughness_c = db.Column(db.Integer)
    roughness_d = db.Column(db.Integer)
    shape_tolerance_a = db.Column(db.Integer)
    shape_tolerance_b = db.Column(db.Integer)
    shape_tolerance_c = db.Column(db.Integer)
    shape_tolerance_d = db.Column(db.Integer)
    max_machining_path_x_a = db.Column(db.Integer)
    max_machining_path_x_b = db.Column(db.Integer)
    max_machining_path_x_c = db.Column(db.Integer)
    max_machining_path_x_d = db.Column(db.Integer)
    max_machining_path_y_a = db.Column(db.Integer)
    max_machining_path_y_b = db.Column(db.Integer)
    max_machining_path_y_c = db.Column(db.Integer)
    max_machining_path_y_d = db.Column(db.Integer)
    max_machining_path_z_a = db.Column(db.Integer)
    max_machining_path_z_b = db.Column(db.Integer)
    max_machining_path_z_c = db.Column(db.Integer)
    max_machining_path_z_d = db.Column(db.Integer)

    #Kostentool
    hauptzeit_tn = db.Column(db.Integer)
    ruestzeit_tr = db.Column(db.Integer)
    werkzeugwechselzeit_twz = db.Column(db.Integer)
    werkstückwechselzeit_twst = db.Column(db.Integer)
    losgroesse_nl = db.Column(db.Integer)
    standmenge_nwz = db.Column(db.Integer) #Standmenge Werkzeug
    fertigungsmittelnr_xfm = db.Column(db.Integer) #Anzahl der Fertigungsmittel


    capability = db.Column(db.Integer)
    alttechnologie = db.Column(db.Integer)
    verknüpfung = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def seed(session):
        random_name = ''.join(random.choice(string.ascii_lowercase)
                              for i in range(8))
        techno = Technology(
            position=1,
            name=random_name,
            alt_technology=2,
            connection="connection",
            roughness_a=1,
            roughness_b=1,
            roughness_c=1,
            roughness_d=1,
            shape_tolerance_a=1,
            shape_tolerance_b=1,
            shape_tolerance_c=1,
            shape_tolerance_d=1,
            max_machining_path_x_a=1,
            max_machining_path_x_b=1,
            max_machining_path_x_c=1,
            max_machining_path_x_d=1,
            max_machining_path_y_a=1,
            max_machining_path_y_b=1,
            max_machining_path_y_c=1,
            max_machining_path_y_d=1,
            max_machining_path_z_a=1,
            max_machining_path_z_b=1,
            max_machining_path_z_c=1,
            max_machining_path_z_d=1,

            hauptzeit_tn = 1
            ruestzeit_tr = 1
            werkzeugwechselzeit_twz = 1
            werkstückwechselzeit_twst =1
            losgroesse_nl = 1
            standmenge_nwz = 1 #Standmenge Werkzeug
            fertigungsmittelnr_xfm = 1

            alttechnologie=1,
            verknüpfung=1,
        )
        session.add(techno)
        session.commit()
