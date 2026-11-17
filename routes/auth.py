from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from flask_login import logout_user, login_required, login_user

from models.conn import db
from models.model import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('auth.profile'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    # signup input validation and logic
    #TODO verify password strenght
    username = request.form.get("username") 
    email = request.form["email"]    
    password = request.form["password"]

    if not username:
        flash('Invalid username')
        return redirect(url_for('auth.signup'))
    if not email:
        flash('Invalid email')
        return redirect(url_for('auth.signup'))
    if not password:
        flash('Invalid password')
        return redirect(url_for('auth.signup'))                
    
    user = User.query.filter_by(email=email).first() 
    if user: 
        flash('User with this email address already exists')
        return redirect(url_for('auth.signup'))

    user = User(username=username, email=email)
    user.set_password(password) 
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logout'