from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename  # for uploading files to server
from flask_mysql_connector import MySQL
import os
import json
# from flask_mysqldb import MySQL 
app = Flask(__name__)
mysql = MySQL(app)


UPLOAD_FOLDER = './static/uploads/'
UPLOAD_FOLDER_IMAGES = './static/images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_IMAGES'] = UPLOAD_FOLDER_IMAGES

app.config['MYSQL'] = 'localhost'
# changed MYSQL_HOST to MYSQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
# app.config['MYSQL_DB'] = 'dbs1'
app.config['MYSQL_DATABASE'] = 'dbs1'




# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == "POST":
#         details = request.form
#         firstName = details['fname']
#         lastName = details['lname']
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO Admin(AdminName, AdminPassword) VALUES (%s, %s)", (firstName, lastName))
#         mysql.connection.commit()
#         cur.close()
#         return 'success'
#     return render_template('admin.html')
#     #return render_template('index.html')


# if __name__ == '__main__':
#     app.run()


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('adminDashboard.html')

@app.route('/admin/tier', methods=['GET', 'POST'])
def admintier():
    cur = mysql.connection.cursor()
    # rows = cur.execute("SELECT tierName FROM Tier")
    rows = cur.execute("SELECT * FROM Tier")
    tiers = cur.fetchall()
    # for tier in tiers:
            #one = tier[0]
            # two = tier[1]
            # print('===============================================')
            # #print('oneee', one)
            # print('twooo', two)
            # print('===============================================')

    if request.method == "POST":
        if request.form['submit_btn'] == 'Add Tier':
            # details = request.form
            # tiername = details['tierName']
            # tierprice = details['tierPrice']
            tiername = request.form.get("tierName")
            tierprice = request.form.get("tierPrice")
            # cur = mysql.connection.cursor()
            if not tiername or not tierprice:
                return "Fields can not be empty" #CAN MAKE HTML FILE
            # rows = cur.execute("SELECT tierName FROM Tier")
            # tiers = cur.fetchall()
            dupTier = True
            for tier in tiers:
                tierVal = tier[1]
                if tiername == tierVal:
                    dupTier = False
                    return render_template("admintier.html", tiers = tiers, dupTier = dupTier)
                    # return 'duplicate' #CAN MAKE HTML FILE
            if(dupTier):
                cur.execute("INSERT INTO Tier (tierName, tierPrice) VALUES (%s, %s)",(tiername, tierprice))
                mysql.connection.commit()
            # cur.close()
            #return 'success'
        elif request.form['submit_btn'] == 'Delete Tier':
            tierid = request.form.get("tierid")
            print('===============================================')
            print(tierid)
            print('===============================================')
            if tierid == None:
                return "Fields can not be empty"
            cur.execute("DELETE FROM Tier WHERE tierID = %(tierid)s", { 'tierid': tierid })
            mysql.connection.commit()
            # return 'success'
        elif request.form['submit_btn'] == 'Update Tier':
            tierid = request.form.get("tierid")
            tierprice = request.form.get("tierPrice")
            print('===============================================')
            print(tierid)
            print(tierprice)
            print('===============================================')
            if tierid == None or tierprice == "":
                return "Fields can not be empty"
            cur.execute("UPDATE Tier SET tierPrice = %(tierprice)s WHERE tierID = %(tierid)s", { 'tierprice': tierprice, 'tierid': tierid})
            mysql.connection.commit()
            # return 'success'
    # if request.method == "POST":
    #     # details = request.form
    #     # tiername = details['tierName']
    #     # tierprice = details['tierPrice']
    #     tiername = request.form.get("tierName")
    #     tierprice = request.form.get("tierPrice")
    #     # cur = mysql.connection.cursor()
    #     if not tiername or not tierprice:
    #         return "Fields can not be empty" #CAN MAKE HTML FILE
    #     # rows = cur.execute("SELECT tierName FROM Tier")
    #     # tiers = cur.fetchall()



    #     # for tier in tiers:#///////////////////////////////
    #     #     if tiername in tier:
    #     #         return 'duplicate' #CAN MAKE HTML FILE
    #     cur.execute("INSERT INTO Tier (tierName, tierPrice) VALUES (%s, %s)",(tiername, tierprice))
    #     mysql.connection.commit()
    #     # cur.close()
    #     return 'success'

    cur.close()
    return render_template('admintier.html', tiers = tiers)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/book', methods=['GET', 'POST'])
def adminbook():
    cur = mysql.connection.cursor()
    rows = cur.execute("SELECT * FROM Book")
    books = cur.fetchall()
    rows = cur.execute("SELECT * FROM Tier")
    tiers = cur.fetchall()
    rows = cur.execute("SELECT * FROM GenreTable")
    genres = cur.fetchall()

    if request.method == "POST":
        if request.form['submit_btn'] == 'Add Genre':
            genre = request.form.get("genre")
            print('===============================================')
            #print('oneee', one)
            print(genre)
            print('=============================================')
            # sql = "INSERT INTO GenreTable (genre) VALUES (%s);"
            # val = genre
            # cur.execute(sql, val)
            # sql = ("INSERT INTO GenreTable "
            #     "(genre) "
            #     "VALUES (%s)")
            # val = (genre)
            # cur.execute(sql, val)
            cur.execute("INSERT INTO GenreTable (genre) VALUES (%s)",(genre,))
            #cur.execute("INSERT INTO Tier (tierName, tierPrice) VALUES (%s, %s)",(tiername, tierprice))
            #cur.execute("INSERT INTO GenreTable (genre) VALUES %s", (genre)) 
            mysql.connection.commit()
            #return render_template('adminbook.html', tiers = tiers, books = books, genres = genres, flag = 0)
        elif request.form['submit_btn'] == 'Delete Genre':
            genreid = request.form.get("genreIDDel")
            print('===============================================')
            #print('oneee', one)
            print(genreid)
            print('=============================================')
            cur.execute("DELETE FROM GenreTable WHERE genreID = %(genreid)s", {'genreid': genreid})
            mysql.connection.commit()
        elif request.form['submit_btn'] == 'Add Book':
            tierid = request.form.get("tierid")
            isbn = request.form.get("isbn")
            bookname = request.form.get("bookName")
            author = request.form.get("author")
            genre = request.form.get("genre")
            name = request.files['file'].filename 
            print(name)
            if (not name):
                print('No file')
                flag = 1
                return render_template("adminbook1.html", flag = flag)
                # return redirect(request.url)
            if tierid == None or not isbn or not bookname or not author or not genre:
                return "Fields can not be empty" #CAN MAKE HTML FILE
            
            dupbook = True
            for book in books:
                isbnVal = book[0]
                print('===============================================')
                print(isbnVal, int(isbn))
                print('===============================================')
                if int(isbnVal) == int(isbn):
                    dupbook = False
                    return render_template("adminbook1.html", dupbook = dupbook, tiers = tiers, books = books, genres = genres)
                    # duplicateflag = 1
                    # return render_template("adminbook1.html", flag = flag)
                     #CAN MAKE HTML FILE
            if (dupbook):
                file = request.files['file']
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                sql = "INSERT into Book (ISBN, bookName, author, genreID, tierID, fileName) VALUES (%s, %s, %s, %s, %s, %s);"
                val = (isbn, bookname, author, genre, tierid, name)
                cur.execute(sql, val)
                # file = request.files['file']
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                # cur.execute("INSERT INTO Book (ISBN, bookName, author, genre, tierID, secure_filename) VALUES (%s, %s, %s, %s, %s, %s)",(isbn, bookname, author, genre, tierid, name))
                mysql.connection.commit()
            
            # cur.close()
            # return 'file uploaded successfully'
        elif request.form['submit_btn'] == 'Delete Book':
            isbn = request.form.get("isbn")
            bookname = request.form.get("bookName")
            mismatch = True
            if not isbn and not bookname:
                return "Both fields can not be empty"
            elif not bookname:
                cur.execute("DELETE FROM Book WHERE ISBN = %(isbn)s", { 'isbn': isbn })
            elif not isbn:
                cur.execute("DELETE FROM Book WHERE bookName = %(bookname)s", { 'bookname': bookname })
            #isbn and name not same issue to be catered for
            elif isbn and bookname:
                row = cur.execute("SELECT bookName FROM Book WHERE ISBN = %(isbn)s", { 'isbn': isbn })
                valbookName = cur.fetchall()
                print('===============================================')
                print(valbookName, isbn, bookname, valbookName[0][0])
                print('===============================================')
                if valbookName[0][0] == bookname:
                    print('===============================================')
                    print("vaah")
                    print('===============================================')
                    cur.execute("DELETE FROM Book WHERE ISBN = %(isbn)s", { 'isbn': isbn })
                else:
                    mismatch = False
                    return render_template("adminbook1.html", mismatch = mismatch, tiers = tiers, books = books, genres = genres)

            mysql.connection.commit()
            # return 'success'
        elif request.form['submit_btn'] == 'Update Book Tier':
            mismatch2 = True
            tierid = request.form.get("tierid")
            isbn = request.form.get("isbn")
            bookname = request.form.get("bookName")
            if not isbn and not bookname:
                return "Both fields can not be empty"
            elif not bookname:
                cur.execute("UPDATE Book SET tierID = %(tierid)s WHERE ISBN = %(isbn)s", {'tierid': tierid, 'isbn': isbn})
            elif not isbn:
                cur.execute("UPDATE Book SET tierID = %(tierid)s WHERE bookName = %(bookname)s", {'tierid': tierid, 'bookname': bookname})
            elif isbn and bookname:
                row = cur.execute("SELECT bookName FROM Book WHERE ISBN = %(isbn)s", { 'isbn': isbn })
                valbookName = cur.fetchall()
                print('===============================================')
                print(valbookName, isbn, bookname, valbookName[0][0])
                print('===============================================')
                if valbookName[0][0] == bookname:
                    print('===============================================')
                    print("vaah")
                    print('===============================================')
                    cur.execute("UPDATE Book SET tierID = %(tierid)s WHERE ISBN = %(isbn)s", {'tierid': tierid, 'isbn': isbn})
                else:
                    mismatch2 = False
                    return render_template("adminbook1.html", mismatch2 = mismatch2, tiers = tiers, books = books, genres = genres)

            # cur.execute("UPDATE Tier SET tierPrice = %(tierprice)s WHERE tierID = %(tierid)s", { 'tierprice': tierprice, 'tierid': tierid})
            mysql.connection.commit()
            # return 'success'
    # if request.method == "POST":
    #     # details = request.form
    #     # tiername = details['tierName']
    #     # tierprice = details['tierPrice']
    #     tiername = request.form.get("tierName")
    #     tierprice = request.form.get("tierPrice")
    #     # cur = mysql.connection.cursor()
    #     if not tiername or not tierprice:
    #         return "Fields can not be empty" #CAN MAKE HTML FILE
    #     # rows = cur.execute("SELECT tierName FROM Tier")
    #     # tiers = cur.fetchall()



    #     # for tier in tiers:#///////////////////////////////
    #     #     if tiername in tier:
    #     #         return 'duplicate' #CAN MAKE HTML FILE
    #     cur.execute("INSERT INTO Tier (tierName, tierPrice) VALUES (%s, %s)",(tiername, tierprice))
    #     mysql.connection.commit()
    #     # cur.close()
    #     return 'success'

    cur.close()
    return render_template('adminbook1.html', tiers = tiers, books = books, genres = genres, flag = 0)

@app.route('/admin/admin', methods=['GET', 'POST'])
def admindata():
    cur = mysql.connection.cursor()
    rows = cur.execute("SELECT * FROM Admin")
    admins = cur.fetchall()

    if request.method == "POST":
        if request.form['submit_btn'] == 'Add Admin':
            adminname = request.form.get("adminName")
            adminpass = request.form.get("adminPass")
            print('===============================================')
            print(adminname, adminpass)
            print('===============================================')


            dupAdmin = True

            for admin in admins:
                adminNameval = admin[1]
                adminPassval = admin[2]
                if adminname == adminNameval and adminpass == adminPassval:
                    dupAdmin = False
                    return render_template("admindata.html", dupAdmin = dupAdmin, admins = admins)

            if(dupAdmin):
                cur.execute("INSERT INTO Admin (adminName, adminPassword) VALUES (%s, %s)", (adminname, adminpass))
                mysql.connection.commit()

        elif request.form['submit_btn'] == 'Delete Admin':
            adminname = request.form.get("adminNameDelete")
            print('===============================================')
            print(adminname)
            print('===============================================')
            cur.execute("DELETE FROM Admin WHERE adminName = %(adminname)s", { 'adminname': adminname })
            mysql.connection.commit()
        
    cur.close()
    return render_template("admindata.html", admins = admins)


@app.route('/admin/item', methods=['GET', 'POST'])
def adminitem():
    cur = mysql.connection.cursor()
    rows = cur.execute("SELECT * FROM CategoryTable")
    categories = cur.fetchall()
    rows = cur.execute("SELECT * FROM Item")
    items = cur.fetchall()

    if request.method == "POST":
        if request.form['submit_btn'] == 'Add Category':
            category = request.form.get("category")
            print('===============================================')
            #print('oneee', one)
            print(category)
            print('=============================================')
            # sql = "INSERT INTO GenreTable (genre) VALUES (%s);"
            # val = genre
            # cur.execute(sql, val)
            # sql = ("INSERT INTO GenreTable "
            #     "(genre) "
            #     "VALUES (%s)")
            # val = (genre)
            # cur.execute(sql, val)
            cur.execute("INSERT INTO CategoryTable (category) VALUES (%s)",(category,))
            #cur.execute("INSERT INTO Tier (tierName, tierPrice) VALUES (%s, %s)",(tiername, tierprice))
            #cur.execute("INSERT INTO GenreTable (genre) VALUES %s", (genre)) 
            mysql.connection.commit()
            #return render_template('adminbook.html', tiers = tiers, books = books, genres = genres, flag = 0)
        elif request.form['submit_btn'] == 'Delete Category':
            categoryid = request.form.get("categoryIDDel")
            print('===============================================')
            #print('oneee', one)
            print(categoryid)
            print('=============================================')
            cur.execute("DELETE FROM CategoryTable WHERE categoryID = %(categoryid)s", {'categoryid': categoryid})
            mysql.connection.commit()
        elif request.form['submit_btn'] == 'Add Item':
            categoryid = request.form.get("categoryid")
            itemname = request.form.get("itemname")
            itemprice = request.form.get("itemprice")
            itembrand = request.form.get("itembrand")
            description = request.form.get("description")
            itemstock = request.form.get("itemstock")
            name = request.files['file'].filename 
            print(name)
            if (not name or not name.lower().endswith(('.png', '.jpg', '.jpeg'))):
                print('No file or invalid file')
                flag = 1
                return render_template("adminItem.html", flag = flag, categories = categories, items = items)
                # return redirect(request.url)
            
            dupitem = True
            # for book in books:
            #     isbnVal = book[0]
            #     print('===============================================')
            #     print(isbnVal, int(isbn))
            #     print('===============================================')
            #     if int(isbnVal) == int(isbn):
            #         dupbook = False
            #         return render_template("adminbook1.html", dupbook = dupbook, tiers = tiers, books = books, genres = genres)
            #         # duplicateflag = 1
            #         # return render_template("adminbook1.html", flag = flag)
            #          #CAN MAKE HTML FILE
            if (dupitem):
                file = request.files['file']
                file.save(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], secure_filename(file.filename)))
                sql = "INSERT into Item (itemName, itemPrice, itemImage, categoryID, brand, description, stock) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                val = (itemname, itemprice, name, categoryid, itembrand, description, itemstock)
                cur.execute(sql, val)
                # file = request.files['file']
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                # cur.execute("INSERT INTO Book (ISBN, bookName, author, genre, tierID, secure_filename) VALUES (%s, %s, %s, %s, %s, %s)",(isbn, bookname, author, genre, tierid, name))
                mysql.connection.commit()
            
            # cur.close()
            # return 'file uploaded successfully'
        elif request.form['submit_btn'] == 'Delete Item':
            itemname = request.form.get("itemDel")
            itembrand = request.form.get("itemDelBrand")
            # mismatch = True
            # if not isbn and not bookname:
            #     return "Both fields can not be empty"
            # elif not bookname:
            #     cur.execute("DELETE FROM Book WHERE ISBN = %(isbn)s", { 'isbn': isbn })
            # elif not isbn:
            #     cur.execute("DELETE FROM Book WHERE bookName = %(bookname)s", { 'bookname': bookname })
            # #isbn and name not same issue to be catered for
            # elif isbn and bookname:
            # row = cur.execute("SELECT bookName FROM Book WHERE ISBN = %(isbn)s", { 'isbn': isbn })
            # valbookName = cur.fetchall()
            print('===============================================')
            print(itemname, itembrand)
            print('===============================================')
            # if valbookName[0][0] == bookname:
            #     print('===============================================')
            #     print("vaah")
            #     print('===============================================')
            #     cur.execute("DELETE FROM Book WHERE ISBN = %(isbn)s", { 'isbn': isbn })
            # else:
            #     mismatch = False
            #     return render_template("adminItem.html", mismatch = mismatch, categories = categories, items = items, flag = 0)
            cur.execute("DELETE FROM Item WHERE itemName = %(itemname)s AND brand = %(itembrand)s", { 'itemname': itemname, 'itembrand': itembrand })
            mysql.connection.commit()
            # return 'success'
        elif request.form['submit_btn'] == 'Update Item Stock':
            # mismatch3 = True
            itemname = request.form.get("itemupdate")
            itembrand = request.form.get("itemupdatebrand")
            itemstock = request.form.get("itemupdatestock")
            print('===============================================')
            print("vaah")
            print('===============================================')
            cur.execute("UPDATE Item SET stock = %(itemstock)s WHERE itemName = %(itemname)s AND brand = %(itembrand)s", {'itemstock': itemstock, 'itemname': itemname, 'itembrand': itembrand})
            # cur.execute("UPDATE Tier SET tierPrice = %(tierprice)s WHERE tierID = %(tierid)s", { 'tierprice': tierprice, 'tierid': tierid})
            mysql.connection.commit()
            # return 'success'
    # if request.method == "POST":
    #     # details = request.form
    #     # tiername = details['tierName']
    #     # tierprice = details['tierPrice']
    #     tiername = request.form.get("tierName")
    #     tierprice = request.form.get("tierPrice")
    #     # cur = mysql.connection.cursor()
    #     if not tiername or not tierprice:
    #         return "Fields can not be empty" #CAN MAKE HTML FILE
    #     # rows = cur.execute("SELECT tierName FROM Tier")
    #     # tiers = cur.fetchall()



    #     # for tier in tiers:#///////////////////////////////
    #     #     if tiername in tier:
    #     #         return 'duplicate' #CAN MAKE HTML FILE
    #     cur.execute("INSERT INTO Tier (tierName, tierPrice) VALUES (%s, %s)",(tiername, tierprice))
    #     mysql.connection.commit()
    #     # cur.close()
    #     return 'success'

    cur.close()
    return render_template('adminItem.html', categories = categories, items = items, flag = 0)



                








if __name__ == '__main__':
    app.run()