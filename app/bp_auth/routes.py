from flask import (Blueprint, render_template,
                   redirect, url_for, request, flash)
from flask_login import current_user, login_user, logout_user

from app.models import User
from app import db
from app.bp_auth.forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__, url_prefix='/')


@auth.before_request
def redirect_if_authenticated():
    if request.endpoint != 'auth.logout' and current_user.is_authenticated:
        return redirect(url_for('main.index'))
    pass


@auth.route('/', methods=["GET", "POST"])
def index():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(password=form.password.data):
                login_user(user)
                return redirect(url_for('main.index'))
            flash('Username oder Passwort ist falsch.')
    return render_template('auth/landingpage.html', form=form)


@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            existing_user = User.query.filter_by(
                username=form.username.data).first()
            if existing_user is None:
                user = User(
                    username=form.username.data,
                )
                user.create_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('main.index'))
            flash('Der Username ist schon vergeben.')
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


