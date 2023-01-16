import pymongo
from flask import *
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash,generate_password_hash

from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df4890eaa6e556b8eef8f10f75f331a0'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/'
mongo = PyMongo(app)
myClient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myClient['flaskProject']

users = mydb['Users']

@app.route('/')
@app.route('/home')
def home():  # put application's code here
    return render_template('home.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():  # put application's code here
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)
        users.insert_one(
            {"username": username,
             "email": email,
             "password": hashed_password}
        )
        flash(f'Account Created for {form.username.data}! :)', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login',methods=['POST', 'GET'])
def login():  # put application's code here
    form = LoginForm()
    if form.validate_on_submit():
        if form.email and form.password:
            email = form.email.data
            password = form.password.data
            user = users.find_one({"email": email})

            if check_password_hash(user["password"], password):
                return render_template('home.html')
            else:
                return render_template('register.html')

    return render_template('login.html', title='Login', form=form)


@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    hashed_password = generate_password_hash(password)

    if username and email and password:
        id = users.insert_one(
            {'username': username, 'password': hashed_password, 'email': email}
        )
        response = {
            "id": str(id.inserted_id),
            "username": username,
            "password": password,
            "email": email
        }
        return response
    else:
        return {'message': 'not received'}

    return {'message': 'received'}


if __name__ == '__main__':
    app.run(port=8080, debug=True)
