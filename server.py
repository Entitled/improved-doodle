from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "EFU*GSUYDFHUPWEflwkjencfoisd"

mysql = MySQLConnector(app, 'user_dashboard')



@app.route('/')
def index():
    users = mysql.query_db('SELECT * FROM users')
    return render_template('index.html', users=users)

@app.route('/users', methods=["POST"])
def create_user():

    #FIRST WE VALIDATE THE FORM INPUT
    errors = []
    if len(request.form['first_name']) == 0:
        errors.append("Please enter a first name.")
    if len(request.form['last_name']) == 0:
        errors.append("Please enter a last name.")
    if len(request.form['email']) == 0:
        errors.append("Please enter a valid email.")
    if len(request.form['password']) == 0:
        errors.append("Please enter a password.")

    #IF THERE WERE ANY ERRORS
    #SEND THEM BACK WITH WARNINGS
    if len(errors) > 0:
        for error in errors:
            print error
            #or flash the errors
        return redirect('/')
    #OTHERWISE PREPARE TO ADD TO THE DATABASE
    else:
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": request.form['password']
        }

        query = """INSERT INTO users
        (first_name, last_name, email, password, created_at, updated_at)
        VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"""

        mysql.query_db(query, data)
    return redirect('/')

@app.route('/users/<user_id>/delete')
def delete_user(user_id):
    data = {'some_id': user_id}
    query = 'DELETE FROM users WHERE id = :some_id'
    mysql.query_db(query, data)
    return redirect('/')




app.run(debug=True)
