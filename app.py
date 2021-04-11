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
def dashboard():
    username = "Monkey"
    userTier = "123"
    return render_template("dashboard.html", username = username, userTier = userTier)

# for editing profile
@app.route('/editProfile')
def edit_profile():
    # user = [123, "monkey1@gmail.com", "Monkey2", "Monkey3", "4/4/4444", "5", "Street 6", "City 7", "State 8", 1]
    # phone = ["12345", "678910", "1112131415"]
    # user = [userID, emailID, userName, userPassword, dob, flatNo, street, city, state, tierID]
    conn = mysql.connection
    cur = conn.cursor()
    userID = str(123)
    cur.execute("SELECT * from user where userID = '" + userID + "'")
    user = cur.fetchone()
    print(user)
    cur.execute("SELECT phoneNo from contact where userID = '" + userID + "'")
    phone = cur.fetchall()
    pcount = len(phone)
    # tierID = str(user[9])
    tierID = "1"
    cur.execute("SELECT tierName from tier where tierID = '" + tierID + "'")
    tierName = (cur.fetchone())[0]
    # return "edit profile"
    return render_template("profile.html", user = user, tierName = tierName, phone = phone, pcount = pcount)

# for upgrading membership
@app.route('/upgrade/<toTier>', methods = ['GET', 'POST'])
def upgrade(toTier):
    if request.method == 'POST':
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("SELECT tierName from tier where tierID = " + toTier)
        tierName = (cur.fetchone())[0]
        return "upgrade to " + tierName
    return render_template("upgrade.html")

# for displaying book shelves
@app.route('/books', methods = ['GET', 'POST'])
def books():
    if request.method == 'POST':
        return redirect(url_for('pdf_display'))
    userID = "123"
    tierID = "1"
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                FROM book b, GenreTable g 
                where b.genreID = g.genreID and b.tierID <= ''' + tierID)
    allowed_books = cur.fetchall()
    cur.execute('''SELECT h.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename  
                FROM book b, GenreTable g, hasRead h 
                where b.bookID = h.bookID and b.genreID = g.genreID 
                and h.userID = '''+ userID)
    read_books = cur.fetchall()
    cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                FROM book b, GenreTable g 
                where b.genreID = g.genreID and b.tierID > ''' + tierID)
    unavailable_books = cur.fetchall()
    cur.execute("SELECT genre from GenreTable")
    genres = cur.fetchall()
    cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                FROM book b, GenreTable g 
                where b.genreID = g.genreID''')
    search_books = cur.fetchall()
    books = []
    # allow_len = len(allowed_books)
    print(genres)
    return render_template('book_main.html', userTier=1, books=books, allowed_books=allowed_books, read_books = read_books, unavailable_books=unavailable_books, search_books=search_books, genres=genres)

# searching books
@app.route('/searchBooks', methods = ["POST"])
def searchBooks():
    conn = mysql.connection
    cur = conn.cursor()
    search_books = []
    search_by = request.json
    search_by = "%" + search_by + "%";
    print(search_by)
    cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                FROM book b, GenreTable g 
                where b.genreID = g.genreID and (author like "''' 
                + search_by + '" or bookName like "' + search_by + '" or genre like "' + search_by + '")')
    books = cur.fetchall()
    for book in books:
        search_books.append(book)
        print(book)
    search_books = json.dumps(search_books)
    return search_books

# filtering the book shelves
@app.route('/filterBooks', methods = ["POST"])
def filter():
    # books = [{"isbn": 9781603037341, "title": "Pride and Prejudice", "filename": "Sense_and_Sensibility.pdf" , "genre": ["Romance", "Satire", "Fiction"]},
    #     {"isbn": 9781603037280, "title": "Sense and Sensibility", "filename": "Sense_and_Sensibility.pdf", "genre": ["Novel", "Romance", "Children's", "Historical fiction"]},
    #     {"isbn": 9780393603095, "title": "The Norton Anthology of English Literature" , "filename": "Sense_and_Sensibility.pdf", "genre": ["English literature", "Literature"]}]
    # print(books[0]["filename"])
    userID = "123"
    tierID = "1"
    conn = mysql.connection
    cur = conn.cursor()
    fil_books = []
    genres = request.json
    print(genres)
    shelf = genres[0]
    for genre in genres[1:]: 
        genre = genre[2:-3]
        print(type(genre))
        print(genre)
        print(shelf)
        if (shelf == "book_list1"):
            cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                        FROM book b, GenreTable g 
                        where b.genreID = g.genreID and g.genre = "''' +
                        genre + '" and b.tierID <= ' + tierID)
        elif (shelf == "book_list2"):
            cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename  
                        FROM book b, GenreTable g, hasRead h 
                        where b.bookID = h.bookID and b.genreID = g.genreID and g.genre = "'''  + 
                        genre + '" and h.userID = ' + userID)
            # cur.execute("SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename FROM book b, GenreTable g where b.genreID = g.genreID and g.genre = '"  + genre + "'" )
        elif (shelf == "book_list3"):
            cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                        FROM book b, GenreTable g 
                        where b.genreID = g.genreID and g.genre = "''' +
                        genre + '" and b.tierID > ' + tierID)
        else:
            cur.execute('''SELECT b.bookID, b.bookName, b.author, g.genre, b.tierID, b.filename 
                        FROM book b, GenreTable g where b.genreID = g.genreID and g.genre = "''' +
                        genre + '"' )
        books = cur.fetchall()
        for book in books:
            fil_books.append(book)
            print(book)
        # print(genre)
    fil_books = json.dumps(fil_books)
    return fil_books

# displaying the selected book
@app.route('/pdfDisplay/<bookID>', methods = ['GET', 'POST'])
def pdf_display(bookID):
    print(bookID)
    userID = "123"
    conn = mysql.connection
    cur = conn.cursor()
    try:
        sql = "SELECT * from hasRead where userID = " + userID + " and bookID = " + bookID
        cur.execute(sql)
        res = cur.fetchall()
    except: 
        return "Oops couldn't check"
    flag = 1
    if (not res):
        flag = 0
    print(flag)
    if (not flag):
        try:
            sql = "INSERT into hasRead (userID, bookID) values (%s, %s)";
            val = (userID, bookID)
            cur.execute(sql, val)
            mysql.connection.commit()
        except:
            return "OOPS couldn't insert"
    try:
        sql = "SELECT fileName FROM book where bookID = " + bookID;
        cur.execute(sql)
        filename = (cur.fetchone())[0]
        # print(filename)
        return render_template('pdf_display.html', filename = filename)
    except:
        return "OOPS!!!"

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
        cur.execute("SELECT tierID from tier where tierName = '" + tierName + "'")
        tierID = cur.fetchone()[0]
        print(tierID)
        print(tierName)
        genre = form.get("genre")
        cur.execute('SELECT genreID from GenreTable where genre = "' + genre + '"')
        genreID = cur.fetchone()[0]
        name = request.files['file'].filename 
        if (not name):
            print('No file')
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

# shop
@app.route('/shop')
def shop():
    return "Let's shop!"

@app.route('/cart')
def cart():
    return "Let's buy!"

print("SUCCESSFUL")

if __name__=='__main__':
    app.run()

# http://127.0.0.1:5000/