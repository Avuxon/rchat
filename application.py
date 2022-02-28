from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, \
    logout_user

from wtform_fields import *
from models import *


#configure application
app = Flask(__name__)
app.secret_key = 'replace later'

#configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://zixzrzxtdupbuj:1248d5efcacceb921a4ec3fede09c4320360597fa752c3fdc0aa87e837880df0@ec2-52-204-29-205.compute-1.amazonaws.com:5432/d72m5ca7955jkp'
db = SQLAlchemy(app)

# Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    # Updates DB if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)
        # automatically adds a 16 byte salt and 29,000 iterations by default


        # Add User to database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST']) 
def login():
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = \
            User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)

@app.route('/chat', methods=['GET', 'POST'])
# @login_required
def chat():
    if not current_user.is_authenticated:
        return "Please login before accessing chat"

    return "Chat with me"

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return "Logged out using Flask-login"

if __name__ == "__main__":
    app.run(debug = True)
