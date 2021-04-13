from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename # for uploading files to server
from flask_mysql_connector import MySQL
import json
import os
import MySQLdb.cursors
import re
from weekend import app

mysql = MySQL(app)

# for displaying book shelves
@app.route('/books', methods = ['GET', 'POST'])
def books():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        if request.method == 'POST':
            return redirect(url_for('pdf_display'))
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                    FROM book b, GenreTable g 
                    where b.genreID = g.genreID and b.tierID <= %s''', (userTier, ))
        allowed_books = cur.fetchall()
        cur.execute('''SELECT h.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename  
                    FROM book b, GenreTable g, hasRead h 
                    where b.bookID = h.bookID and b.genreID = g.genreID 
                    and h.userID = %s''', (userID, ))
        read_books = cur.fetchall()
        cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                    FROM book b, GenreTable g 
                    where b.genreID = g.genreID and b.tierID > %s''', (userTier, ))
        unavailable_books = cur.fetchall()
        cur.execute("SELECT genre from GenreTable")
        genres = cur.fetchall()
        cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                    FROM book b, GenreTable g 
                    where b.genreID = g.genreID''')
        search_books = cur.fetchall()
        books = []
        return render_template('book_main.html', userTier=userTier, books=books, allowed_books=allowed_books, read_books = read_books, unavailable_books=unavailable_books, search_books=search_books, genres=genres)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# searching books
@app.route('/searchBooks', methods = ["POST"])
def searchBooks():
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
        search_books = []
        search_by = request.json
        search_by = "%" + search_by + "%";
        cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                    FROM book b, GenreTable g 
                    where b.genreID = g.genreID and (author like %s or bookName like %s or genre like %s)''', (search_by, search_by, search_by,)) 
        books = cur.fetchall()
        for book in books:
            search_books.append(book)
        search_books = json.dumps(search_books)
        return search_books

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# filtering the book shelves
@app.route('/filterBooks', methods = ["POST"])
def filter():
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
        fil_books = []
        genres = request.json
        shelf = genres[0]
        for genre in genres[1:]: 
            genre = genre[2:-3]
            if (shelf == "book_list1"):
                cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                            FROM book b, GenreTable g 
                            where b.genreID = g.genreID and g.genre = %s and b.tierID <= %s''', (genre, userTier, ))
            elif (shelf == "book_list2"):
                cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename  
                            FROM book b, GenreTable g, hasRead h 
                            where b.bookID = h.bookID and b.genreID = g.genreID and g.genre = %s and h.userID = %s''', (genre, userTier, )) 
                # cur.execute("SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename FROM book b, GenreTable g where b.genreID = g.genreID and g.genre = '"  + genre + "'" )
            elif (shelf == "book_list3"):
                cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                            FROM book b, GenreTable g 
                            where b.genreID = g.genreID and g.genre = %s and b.tierID > %s''', (genre, userTier, ))
            else:
                cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                            FROM book b, GenreTable g where b.genreID = g.genreID and g.genre = %s''', (genre, ))
            books = cur.fetchall()
            for book in books:
                fil_books.append(book)
                # print(book)
            # print(genre)
        fil_books = json.dumps(fil_books)
        return fil_books

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# displaying the selected book
@app.route('/pdfDisplay/<bookID>', methods = ['GET', 'POST'])
def pdf_display(bookID):
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
        try:
            sql = "SELECT * from hasRead where userID = %s and bookID = %s"
            cur.execute(sql, (userID, bookID,))
            res = cur.fetchall()
        except: 
            return "Oops couldn't check"
        flag = 1
        if (not res):
            flag = 0
        if (not flag):
            try:
                sql = "INSERT into hasRead (userID, bookID) values (%s, %s)";
                val = (userID, bookID,)
                cur.execute(sql, val)
                mysql.connection.commit()
            except:
                return "OOPS couldn't insert"
        try:
            sql = "SELECT fileName FROM book where bookID = %s"
            cur.execute(sql, (bookID, ))
            filename = (cur.fetchone())[0]
            # print(filename)
            return render_template('pdf_display.html', filename = filename)
        except:
            return "OOPS!!!"

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# uploading a new book
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        conn = mysql.connection
        cur = conn.cursor()
        # check if the post request has the file part
        form = request.form
        # isbn = int(form.get("isbn"))
        isbn = form.get("isbn")
        title = form.get("title")
        author = form.get("author")
        tierName = form.get("tierName")
        cur.execute("SELECT tierID from tier where tierName = %s", (tierName,))
        tierID = cur.fetchone()[0]
        # print(tierID)
        # print(tierName)
        genre = form.get("genre")
        cur.execute('SELECT genreID from GenreTable where genre = %s',(genre, ))
        genreID = cur.fetchone()[0]
        name = request.files['file'].filename 
        if (not name):
            # print('No file')
            flag = 1
            return render_template("book_upload.html", flag = flag)
            # return redirect(request.url)
        if (not isbn):
            isbn = 0
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        try:
            sql = "INSERT into Book (isbn, bookName, author, genreID, tierID, fileName) VALUES (%s, %s, %s, %s, %s, %s);"
            val = (isbn, title, author, genreID, tierID, name)
            cur.execute(sql, val)
        except:
            return "OOPS couldn't add"
        mysql.connection.commit()
        return 'file uploaded successfully'
    return render_template("book_upload.html", flag = 0)