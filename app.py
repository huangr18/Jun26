from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, Response
from db import load_users_from_db, get_user_firstname_from_db, get_username_from_db, add_video_from_db
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from aivision import runcv

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(hours=1)
app.config['SECRET_KEY'] = 'hello'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")



#home page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

#see users
@app.route("/api/get_users")
def api_get_users():
    all_users = load_users_from_db()
    return jsonify(all_users)

@app.route("/api/user")
def api_user():
    user = get_user_firstname_from_db('jimh01@gmail.com')

    return user

#login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form['email']
        firstname = get_user_firstname_from_db(email)
        username = get_username_from_db(email)
        session["firstname"] = firstname
        session["username"] = username
        return redirect(url_for('user'))
    else:
        return render_template('login.html')


@app.route("/user", methods=['GET', 'POST'])
def user():
    if "firstname" in session:
        firstname = session["firstname"]
        username = session["username"]
        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data
            filename = file.filename
            filename = username + filename
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(filename)))
            add_video = add_video_from_db(username, filename)
            return render_template('upload_success.html', filename=filename, add_video=add_video)
        
        return render_template('user.html', firstname=firstname, form=form)
    else:
        if "firstname" in session:
            return redirect(url_for("user"))
        
        return redirect(url_for("login"))


@app.route("/video/<filename>", methods=['GET', 'POST'])
def video(filename):
    if "firstname" in session:
        username = session["username"]
    return Response(runcv(filename), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/logout")
def logout():
    session.pop("firstname", None)
    flash("You have been logout!", "info")
    return redirect(url_for("home"))




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)