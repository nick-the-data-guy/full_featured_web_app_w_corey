from flask import Flask, render_template, url_for, flash, redirect

# this is where you import the forms you created in the forms.py file
from forms import RegistrationForm, LoginForm

app=Flask(__name__)

# secret keys protects against modifying cookies and cross-site forgery attacks
# you want this to be a bunch of random characters.
#  to get a random key:
# $ python
# >>> import secrets
# >>> secrets.token_hex(16)



app.config['SECRET_KEY'] = 'ef931caa57f5dcc01a77ba311507ade0'
posts = [
	
        {
			'author': 'Nick White',
			'title': 'Blog Post 1',
			'content': 'First Post content',
			'date_posted': 'April 20, 2018'

        },

        {
			'author': 'Your Mom',
			'title': 'Your Mom Went To college',
			'content': 'haha haaha',
			'date_posted': 'April 16, 2019'

        }



]


################
## home route ##
################
@app.route('/')
@app.route('/home')
def home():
	return render_template("home.html", posts=posts)



#################
## about route ##
#################
@app.route("/about")
def about():
	return render_template("about.html", title='About')




########################
## registration route ##
########################
@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)




#################
## login route ##
#################
@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password.', 'danger')
	return render_template('login.html', title='Login', form=form)




if __name__ == "__main__":
	app.run(debug=True)