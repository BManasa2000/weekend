from flask import Flask
from flask_mysql_connector import MySQL

app = Flask(__name__)
# make sure to import these after defining app
import weekend.homeView
import weekend.bookView

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MYSQL_USER'] = 'dbms'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE'] = 'dbs1'
app.config['MYSQL_AUTH_PLUGIN'] = 'mysql_native_password'
app.config['SECRET_KEY'] = 'abcd' 

# session['loggedin'] = True
# session['id'] = user[0]
# session['emailid'] = "monkey1@gmail.com"
# msg = 'Logged in successfully !'

# print("SUCCESSFUL")

if __name__=='__main__':
    app.run()

# http://127.0.0.1:5000/