from flask import *
from flask_wtf import CSRFProtect

from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df4890eaa6e556b8eef8f10f75f331a0'


@app.route('/')
@app.route('/home')
def home():  # put application's code here
    return render_template('home.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():  # put application's code here
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():  # put application's code here
    form = LoginForm()
    return render_template('register.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
