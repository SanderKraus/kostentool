import os


# Hier werden Configuration Variables für Flask definiert
# Define the application directory
# Hilffunktion um aktuelles Projekt(Pfad zum Projekt) zu finden. Zeigt genau den Ornder an in dem sich das Projekt befindet (macht den Code schöner)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLAlchemy configuration
DATABASE_TYPE = 'sqlite'
# festgelegte Definition von SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')   
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Admin fluid layout
FLASK_ADMIN_FLUID_LAYOUT = True

# Secret key
SECRET_KEY = "secret"
