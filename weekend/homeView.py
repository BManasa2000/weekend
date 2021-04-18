from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename # for uploading files to server
from flask_mysql_connector import MySQL
import json
import os
import MySQLdb.cursors
import re
from weekend import app

mysql = MySQL(app)

@app.route('/')
def home():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        conn = mysql.connection
        cur = conn.cursor(buffered=True)
        sql1 = f'''(SELECT count(*) as num, genreID from hasread h, book b where h.userID = {userID} and b.bookID = h.bookID group by genreID)'''
        print(sql1)
        sql2 = "SELECT max(num) from " + sql1 + " y"
        print(sql2)
        cur.execute(sql2)
        res = cur.fetchone()
        if res is not None:
            res = res[0]
            print(res)
            cur.execute("SELECT genreID from " + sql1 + " y where num = %s", (res,))
            res = cur.fetchone()
        genreID = res
        try:
            if genreID is None:
                cur.execute("SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename FROM book b, GenreTable g where b.genreID = g.genreID and b.tierID <= %s", (userTier,))
                books = cur.fetchall()
            else:
                cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename FROM book b, GenreTable g where g.genreID = b.genreID and b.genreID = %s''', (genreID, ))
                books = cur.fetchall()
        # return render_template('home.html', msg = msg)
            return render_template("home.html", username=username, emailid=emailid, books=books, userTier=userTier)  
        except Exception as error:
            print(error)
            return "sorry"
    return redirect(url_for('login'))

# for upgrading membership
@app.route('/upgrade', methods = ['GET', 'POST'])
def upgrade():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        conn = mysql.connection
        cur = conn.cursor()
        if request.method == "POST":
            tierID = request.json
            # print(tierID)
            cur.execute("UPDATE user set tierID = %s where userID = %s", (tierID, userID, ))
            mysql.connection.commit()
            cur.execute("SELECT u.tierID, t.tierName from user u, tier t where userID = %s and t.tierID = u.tierID", (userID,))
            # cur.execute("SELECT tierName from tier where tierID = " + tierID)
            userTier = cur.fetchone()
            userTier = json.dumps(userTier)
            return userTier
        cur.execute("SELECT * from tier")
        tiers = cur.fetchall()
        cur.execute("SELECT u.tierID, t.tierName from user u, tier t where userID = %s  and t.tierID = u.tierID", (userID,))
        userTier = cur.fetchone()
        return render_template("upgrade.html", userID = userID, userTier = userTier, tiers = tiers)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# # shop
# @app.route('/shop')
# def shop():
#     return "Let's shop!"

@app.route('/cart')
def cart():
    return "Let's buy!"

@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'emailid' in request.form and 'password' in request.form:
        emailid = request.form['emailid']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE emailID = %s AND userPassword = %s', (emailid, password))
        user = cursor.fetchone()
        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user[0]
            session['emailid'] = user[1]
            msg = 'Logged in successfully !'
            userID = user[0]
            emailid = user[1]
            username = user[2]
            userTier = user[9]
            conn = mysql.connection
            cur = conn.cursor(buffered=True)
            sql1 = f'''(SELECT count(*) as num, genreID from hasread h, book b where h.userID = {userID} and b.bookID = h.bookID group by genreID)'''
            # va11 = (userID, )
            print(sql1)
            sql2 = "SELECT max(num) from " + sql1 + " y"
            print(sql2)
            cur.execute(sql2)
            res = cur.fetchone()
            if res is not None:
                res = res[0]
                print(res)
                cur.execute("SELECT genreID from " + sql1 + " y where num = %s", (res,))
                res = cur.fetchone()
            print(res)
            genreID = res
            try:
                if genreID is None:
                    cur.execute("SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename FROM book b, GenreTable g where b.genreID = g.genreID and b.tierID <= %s", (userTier,))
                    books = cur.fetchall()
                else:
                    genreID = genreID[0]
                    cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename FROM book b, GenreTable g where g.genreID = b.genreID and b.genreID = %s''', (genreID, ))
                    books = cur.fetchall()
            # return render_template('home.html', msg = msg)
                return render_template("home.html", emailid=emailid, books = books, userTier = userTier)  
            except Exception as error:
                print(error)
                return "sorry"
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username / password !'
            return render_template('index.html', msg = msg)
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('emailid', None)
    return redirect(url_for('login'))


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'dob' in request.form and 'flatNo' in request.form and 'street' in request.form and 'city' in request.form and 'state' in request.form and 'phoneno1' in request.form:
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']
        flatNo = request.form['flatNo']
        street = request.form['street']
        state = request.form['state']
        email = request.form['email']
        city = request.form['city']
        phoneno1 = request.form['phoneno1']
        phoneno2 = request.form['phoneno2']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE emailID = %s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'An account with this email ID already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'^[a-zA-Z0-9]{5,30}$', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z0-9-_=<>/\\\^\$\.\|\?\*\+\(\)\[\{\}\]!@#%&]{8,20}', password):
            msg = 'Password must contain between 8 and 20 characters!'
        elif not re.match(r'\S*[A-Z]+', password):
            msg = 'Password must contain at least one capital letter!'
        elif not re.match(r'\S*[a-z]+', password):
            msg = 'Password must contain at least one lower letter!'
        elif not re.match(r'\S*[0-9]+', password):
            msg = 'Password must contain at least one number!'
        elif not re.match(r'\S*[-_=<>/\\\^\$\.\|\?\\+\(\)\[\{\}\]!@#%&]+', password):
            msg = 'Password must contain at least one special character!'
        elif not re.match(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', dob):
            msg = 'Please enter a valid date !'
        elif not re.match(r'[0-9]{10}', phoneno1):
            msg = 'Please enter a valid Phone Number !'
        elif phoneno2 != "" and not re.match(r'[0-9]{10}', phoneno2):
            msg = 'Please enter a valid Phone Number !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute("INSERT INTO user (emailID, userName, userPassword, dob, flatNo, street, city, state, tierID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (email, username, password,dob, flatNo, street, city, state,1,))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM user WHERE emailID = %s', (email,))
            user = cursor.fetchone()
            uid = user[0]
            cursor.execute("INSERT INTO Contact (phoneNo, userID) VALUES (%s,%s)", (phoneno1,uid,))
            mysql.connection.commit()
            if phoneno2 != "" and phoneno1 != phoneno2:
                cursor.execute("INSERT INTO Contact (phoneNo, userID) VALUES (%s,%s)", (phoneno2,uid,))
                mysql.connection.commit()
            session['loggedin'] = True
            session['id'] = user[0]
            session['emailid'] = user[1]
            msg = 'You have successfully registered !'
            return redirect(url_for('home'))
            # return render_template('home.html', msg = msg)

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        cursor.execute('SELECT * from Contact WHERE userID = %s order by phoneNo desc', (session['id'],))
        contact = cursor.fetchall()
        cursor.execute('SELECT * from Tier WHERE tierID = %s ', (account[9],))
        tier = cursor.fetchone()
        length = len(contact)
        return render_template('profile.html', account=account, contact = contact, length = length, tier = tier)
    return redirect(url_for('login'))

@app.route('/edit_profile', methods =['GET', 'POST'])
def edit_profile():
    if 'loggedin' in session:
        msg = ''
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        cursor.execute('SELECT * from Contact WHERE userID = %s', (session['id'],))
        contact = cursor.fetchall()
        length = len(contact)
        if request.method == 'POST':
            if 'email' in request.form:
                email = request.form['email']
                cursor.execute("UPDATE User SET emailID = %s where userID = %s", (email,session['id'],))
                mysql.connection.commit()
            if 'username' in request.form:
                username = request.form['username']
                cursor.execute("UPDATE User SET userName = %s where userID = %s", (username,session['id'],))
                mysql.connection.commit()
            if 'dob' in request.form:
                dob = request.form['dob']
                cursor.execute("UPDATE User SET dob = %s where userID = %s", (dob,session['id'],))
                mysql.connection.commit()
            if 'flatNo' in request.form:
                flatNo = request.form['flatNo']
                cursor.execute("UPDATE User SET flatNo = %s where userID = %s", (flatNo,session['id'],))
                mysql.connection.commit()
            if 'city' in request.form:
                city = request.form['city']
                cursor.execute("UPDATE User SET city = %s where userID = %s", (city,session['id'],))
                mysql.connection.commit()
            if 'street' in request.form:
                street = request.form['street']
                cursor.execute("UPDATE User SET street = %s where userID = %s", (street,session['id'],))
                mysql.connection.commit()
            if 'state' in request.form:
                state = request.form['state']
                cursor.execute("UPDATE User SET state = %s where userID = %s", (state,session['id'],))
                mysql.connection.commit()
            if 'phoneno1' in request.form:
                phoneno1 = request.form['phoneno1']
                cursor.execute("UPDATE Contact SET phoneNo = %s where userID = %s and phoneNo = %s", (phoneno1,session['id'],contact[0][0],))
                mysql.connection.commit()
            if length==1:
                if 'phoneno2' in request.form:
                    phoneno2 = request.form['phoneno2']
                    cursor.execute("INSERT INTO Contact (phoneNo, userID) VALUES (%s,%s)", (phoneno2,session['id'],))
                    mysql.connection.commit()
            else:
                phoneno2 = request.form['phoneno2']
                cursor.execute("UPDATE Contact SET phoneNo = %s where userID = %s and phoneNo = %s", (phoneno2,session['id'],contact[0][1],))
                mysql.connection.commit()
            msg = 'Your profile has been edited !'
            return redirect(url_for('profile', msg = msg))
        else:
            return render_template('edit_profile.html', account = account, contact = contact, length = length)
    return redirect(url_for('login'))

@app.route('/admin_login/', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin WHERE adminName = %s AND adminPassword = %s', (name, password))
        user = cursor.fetchone()
        print(user)
        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user[0]
            msg = 'Logged in successfully !'
            # return render_template('home.html', msg = msg)
            return redirect(url_for('adminHome'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username / password !'
            return render_template('admin_login.html', msg = msg)
    return render_template('admin_login.html', msg=msg)
    # Show the login form with message (if any)