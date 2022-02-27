from flask import Flask, render_template
from wtform_fields import *
from models import *

#configure application
app = Flask(__name__)
app.secret_key = 'replace later'

#configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://zixzrzxtdupbuj:1248d5efcacceb921a4ec3fede09c4320360597fa752c3fdc0aa87e837880df0@ec2-52-204-29-205.compute-1.amazonaws.com:5432/d72m5ca7955jkp'
db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Add User to database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB!"

    return render_template("index.html", form=reg_form)

if __name__ == "__main__":
    app.run(debug = True)
