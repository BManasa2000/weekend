from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename # for uploading files to server
from flask_mysql_connector import MySQL
import json
import os

app = Flask(__name__)
mysql = MySQL(app)

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MYSQL_USER'] = 'dbms'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE'] = 'dbs1'
app.config['MYSQL_AUTH_PLUGIN'] = 'mysql_native_password'

@app.route('/')
def index():
    try:
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("SELECT name, species from pet where owner = 'BOB'")
        name, species = cur.fetchone()
        return render_template('index.html', name = name, species = species)
    except ValueError:
        print("Error mysql connection 1")
        return

@app.route('/books', methods = ['GET', 'POST'])
def books():
    if request.method == 'POST':
        return redirect(url_for('pdf_display'))
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    books = cur.fetchall()
    # print(books)
    # {"isbn": , "title": , "filename": , "genre": []}
    genres = ["English Literature", "History", "Romance", "Fiction"]

    return render_template('book_main.html', books = books, genres = genres)

@app.route('/filterBooks', methods = ["POST"])
def filter():
    # books = [{"isbn": 9781603037341, "title": "Pride and Prejudice", "filename": "Sense_and_Sensibility.pdf" , "genre": ["Romance", "Satire", "Fiction"]},
    #     {"isbn": 9781603037280, "title": "Sense and Sensibility", "filename": "Sense_and_Sensibility.pdf", "genre": ["Novel", "Romance", "Children's", "Historical fiction"]},
    #     {"isbn": 9780393603095, "title": "The Norton Anthology of English Literature" , "filename": "Sense_and_Sensibility.pdf", "genre": ["English literature", "Literature"]}]
    # print(books[0]["filename"])
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    books = cur.fetchall()
    # fil_books = []
    # genres = request.json
    # for genre in genres: 
    #     for book in books:
    #         if genre in book["genre"] and book not in fil_books:
    #             fil_books.append(book)
    #             for fb in fil_books:
    #                 print(fb["title"])
    #     print(genre)
    # fil_books = json.dumps(fil_books)
    # return fil_books
    books = json.dumps(books)
    return books

@app.route('/pdfDisplay/<filename>', methods = ['GET', 'POST'])
def pdf_display(filename):
    print(filename)
    return render_template('pdf_display.html', filename = filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        conn = mysql.connection
        cur = conn.cursor()
        # check if the post request has the file part
        form = request.form
        isbn = int(form.get("isbn"))
        title = form.get("title")
        author = form.get("author")
        tierID = 1
        genre = form.get("genre")
        name = request.files['file'].filename 
        # print(form.get("isbn"))
        # print(form.get("title"))
        # print(form.get("author"))
        # print(form.get("genre"))
        # print("==============================================")
        # print(name)
        # print("==============================================")
        if (not name):
            print('No file')
            flag = 1
            return render_template("book_upload.html", flag = flag)
            # return redirect(request.url)
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        sql = "INSERT into Book (isbn, bookName, author, genre, tierID, fileName) VALUES (%s, %s, %s, %s, %s, %s);"
        val = (isbn, title, author, genre, tierID, name)
        cur.execute(sql, val)
        mysql.connection.commit()
        return 'file uploaded successfully'
    return render_template("book_upload.html", flag = 0)

print("SUCCESSFUL")

if __name__=='__main__':
    app.run()

# http://127.0.0.1:5000/