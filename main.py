#importing what is needed from the flask micro
from flask import Flask, request, redirect, render_template, flash, url_for
import re #<----this module is for RegEx (regular expressions)

app = Flask(__name__)  #setup the application
app.secret_key = 'ReBaKAHs-SeCret-KEY'

#global variables, until we start using databases
username = ''
email = ''
password = ''
username_error = ''
password_error = ''
verify_password_error = ''
email_error = ''


#function to check the validity of a username
def checkUserName(username):
    '''
    Returns True if "username" global is invalid, then resets username to null and sets
    the respective error globals.
    '''
    for i in username:
        if i.isspace():
            username_error = 'Username cannot contain spaces.' #if has space, set error message
            username = '' #if in error, reset the username variable to empty
            return False
        elif (len(username) < 3) or (len(username) > 20):  #checks the length of username
            username_error = 'Username needs to be 3-20 characters.'
            username = ''
            return False
        elif not username:
            username_error = "Not a valid username"
            username = ''
            return False
        else:
            return True


#check the validity of password(s)
def checkPassword(password, verify):
    '''
    Returns True is there is an error in the password, or the passwords do not match, then
    sets the error globals.
    '''
    for i in password:
        if i.isspace():
            password_error = 'Password must not contain spaces.'
            return False
        elif (len(password) < 3) or (len(password) > 20):
                password_error = 'Password must be 3-20 characters and not contain spaces.'
                return False
        elif not len(password):
            password_error = 'Not a valid password'
            return False
        elif password != verify:
            verify_password_error = 'Passwords do not match.'
            return False
        else:
            return True


#checks the validity of email format
def checkEmail(email):
    '''
    Returns True is email is in an invalid format.
    '''
    if (email == '') or (not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)):
        email_error = 'This is not a valid email.'
        email = ''
        return False
    else:
        return True



#index route, the main route that loads when you start the application
@app.route('/')
@app.route('/signup', methods=['GET', 'POST'])  
def index():                              
    title = "Signup Page"  
    return render_template('signup.html', title=title)




#confirmation route
@app.route('/confirmation', methods=['GET', 'POST']) #confirmation route
def confirmation():
    title = "Welcome!"  #set the page title
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    verify = request.form['verify']
    if not checkEmail(email):  #test email
            flash('Your email is possibly invalid, you might want to check that!', 'warning')
            return redirect(url_for('index', title=title))
    elif not checkPassword(password, verify):  #test password
        flash('Passwords cannot contain spaces! Try again!', 'danger')
        return redirect(url_for('index', title=title))
    elif not checkUserName(username):  #test password
        flash('Username cannot contain spaces! Try again!', 'danger')
        return redirect(url_for('index', title=title))
    return render_template('confirmation.html', title=title, username=username)

app.run()