from flask import Blueprint, render_template, redirect, url_for, request, flash,current_app,send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required
from .models import User, Subject,files
from .import db
import os

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('register.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.login_post'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/class')
@login_required
def notes():
    return render_template('notes.html')

@auth.route("/class/automata/", methods=['GET', 'POST', 'PUT'])
@login_required
def automata():
    files_list = os.listdir(current_app.config["UPLOAD_FOLDER"])
    handwritten_files_list = os.listdir(current_app.config["HANDWRITTEN_UPLOAD_FOLDER"])
    google_files_list = os.listdir(current_app.config["GOOGLE_UPLOAD_FOLDER"])
    return render_template('automata.html',handwritten_files_list=handwritten_files_list, google_files_list=google_files_list)

@auth.route('/success', methods = ['POST'])   
def success():   
    files_list = os.listdir(current_app.config["UPLOAD_FOLDER"])
    handwritten_files_list = os.listdir(current_app.config["HANDWRITTEN_UPLOAD_FOLDER"])
    google_files_list = os.listdir(current_app.config["GOOGLE_UPLOAD_FOLDER"])
    if request.method == 'POST':
            f = request.files['file']
    if f:
            filename = secure_filename(f.filename)
            if 'hw' in filename.lower():
                f.save(os.path.join(current_app.config["HANDWRITTEN_UPLOAD_FOLDER"], filename))
                handwritten_files_list.append(filename)
            elif 'gg' in filename.lower():
                f.save(os.path.join(current_app.config["GOOGLE_UPLOAD_FOLDER"], filename))
                google_files_list.append(filename)
            else:
                f.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
                files_list.append(filename)
            return render_template("ack.html", handwritten_files_list=handwritten_files_list, google_files_list=google_files_list)
    else:
        return render_template("ack.html", handwritten_files_list=handwritten_files_list, google_files_list=google_files_list)
    
@auth.route('/download/<category>/<filename>')
def download_file(category, filename):
    if category == 'handwritten':
        file_path = os.path.join(current_app.config["HANDWRITTEN_UPLOAD_FOLDER"], filename)
    elif category == 'google':
        file_path = os.path.join(current_app.config["GOOGLE_UPLOAD_FOLDER"], filename)
    return send_file(file_path, as_attachment=True)
  