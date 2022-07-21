from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')#Render Homepage
def index():
    if 'user_id' in session:
        return redirect('/recipes')
    return render_template('index.html')

# Bcrypt methods below
@app.route('/register', methods=['POST'])# 
def register():
    # validate the form here ...
    if request.method == 'POST':
        if not User.validate_registration(request.form): # validate me senpai, validate me
            print('invalid')
            return redirect('/')
        if not User.unique_address(request.form): #if there is match, rejects submission
            print('email already registered')
            return redirect('/')
    # create the hash
        print('hashing')
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
    # put the pw_hash into the data dictionary
        data = {
            "first_name": request.form['first_name'].title(),
            "last_name": request.form['last_name'].title(),
            "email": request.form['email'].lower(),
            "password" : pw_hash
        }
        print('consolidated')
    # Call the save @classmethod on User
        user_id = User.save_entry(data)
        print('user saved')
    # store user id into session
        session['user_id'] = user_id
        print('id returned')
        return redirect("/recipes")

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user = User.get_by_email(data)
    # user is not registered in the db
    if not user:
        flash("Email provided is not registered", 'error_log')
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        # if we get False after checking the password
        flash("Password provided is invalid", 'error_log')
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user.id
    return redirect("/recipes")

@app.route('/recipes')# Show all Recipes! If not logged in, clear session and go to login page
def result():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    user = User.get_by_id(data) 
    if not user:
        return redirect('/logout')
    return render_template('success.html', recipes=Recipe.fetch_recipes(), user=user) #, messages=messages, total=total )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
