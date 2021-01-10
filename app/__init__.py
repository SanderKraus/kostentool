from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)

    from .models import User, Tool, Technology

    # Flask admin
    admin = Admin(app, name='Admin-Kostentool-RWTH',
                  template_mode='bootstrap4')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Tool, db.session))
    admin.add_view(ModelView(Technology, db.session))

    # Flask login
    login.init_app(app)
    login.login_view = 'auth.login'
    login.login_message = 'Du bist nicht eingeloggt.'
    
    # sucht den User in der Datenbank mit der User ID
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Aufteilung in Module
    from app.bp_error.routes import error
    app.register_blueprint(error)

    from app.bp_auth.routes import auth
    app.register_blueprint(auth)

    from app.bp_main.routes import main
    app.register_blueprint(main)

    # Workaround for Flask-Migrate when altering Tables in Sqlite
    if app.config["DATABASE_TYPE"] == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    return app
    
