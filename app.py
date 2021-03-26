from flask import Flask, render_template, request
from flask_mysqldb import MySQL
# import MySQLdb.cursors
from flask_mysql_connector import MySQL

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_USER'] = 'dbms'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE'] = 'dbs1'
app.config['MYSQL_AUTH_PLUGIN'] = 'mysql_native_password'

@app.route('/')
def index():
    try:
        conn = mysql.connection
        cur = conn.cursor()
        name, species = cur.fetchone()
        return render_template('index.html', name=name, species=species)
    except ValueError:
        print("Error mysql connection 1")
        return

print("SUCCESSFUL")

if __name__=='__main__':
    app.run()

# http://127.0.0.1:5000/