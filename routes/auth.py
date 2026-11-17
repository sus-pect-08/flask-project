from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from flask_login import logout_user, login_required, login_user, current_user

from models.conn import db
from models.model.User import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))

    return render_template('auth/login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    remember = request.form.get('remember') == 'on'

    user = db.session.execute(
        db.select(User).filter_by(email=email)
    ).scalar_one_or_none()

    if not user or not user.check_password(password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('auth.profile'))


@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('auth/signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not username:
        flash('Invalid username')
        return redirect(url_for('auth.signup'))

    if not email:
        flash('Invalid email')
        return redirect(url_for('auth.signup'))

    if not password:
        flash('Invalid password')
        return redirect(url_for('auth.signup'))

    existing_user = db.session.execute(
        db.select(User).filter_by(email=email)
    ).scalar_one_or_none()

    if existing_user:
        flash('User with this email address already exists')
        return redirect(url_for('auth.signup'))

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    flash('Account created successfully.')
    return redirect(url_for('auth.login'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))