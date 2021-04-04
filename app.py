from flask import Flask, render_template, request
from flask_mysql_connector import MySQL
# from flask_mysqldb import MySQL
app = Flask(__name__)
mysql = MySQL(app)


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

            for tier in tiers:
                tierVal = tier[1]
                if tiername == tierVal:
                    return 'duplicate' #CAN MAKE HTML FILE
            cur.execute("INSERT INTO Tier (tierName, tierPrice) VALUES (%s, %s)",(tiername, tierprice))
            mysql.connection.commit()
            # cur.close()
            return 'success'
        elif request.form['submit_btn'] == 'Delete Tier':
            tierid = request.form.get("tierid")
            print('===============================================')
            print(tierid)
            print('===============================================')
            if tierid == None:
                return "Fields can not be empty"
            cur.execute("DELETE FROM Tier WHERE tierID = %(tierid)s", { 'tierid': tierid })
            mysql.connection.commit()
            return 'success'
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
            return 'success'
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

@app.route('/admin/book', methods=['GET', 'POST'])
def adminbook():
    cur = mysql.connection.cursor()
    rows = cur.execute("SELECT * FROM Book")
    books = cur.fetchall()
    rows = cur.execute("SELECT * FROM Tier")
    tiers = cur.fetchall()

    if request.method == "POST":
        if request.form['submit_btn'] == 'Add Book':
            tierid = request.form.get("tierid")
            isbn = request.form.get("isbn")
            bookname = request.form.get("bookName")
            author = request.form.get("author")
            genre = request.form.get("genre")
            if tierid == None or not isbn or not bookname or not author or not genre:
                return "Fields can not be empty" #CAN MAKE HTML FILE
            
            for book in books:
                isbnVal = books[0]
                if isbn == isbnVal:
                    return 'duplicate' #CAN MAKE HTML FILE
            cur.execute("INSERT INTO Book (ISBN, bookName, author, genre, tierID) VALUES (%s, %s, %s, %s, %s)",(isbn, bookname, author, genre, tierid))
            mysql.connection.commit()
            # cur.close()
            return 'success'
        elif request.form['submit_btn'] == 'Delete Book':
            isbn = request.form.get("isbn")
            bookname = request.form.get("bookName")
            if not isbn and not bookname:
                return "Both fields can not be empty"
            elif not bookname:
                cur.execute("DELETE FROM Book WHERE ISBN = %(isbn)s", { 'isbn': isbn })
            elif not isbn:
                cur.execute("DELETE FROM Book WHERE bookName = %(bookname)s", { 'bookname': bookname })
            # cur.execute("DELETE FROM Tier WHERE tierID = %(tierid)s", { 'tierid': tierid })
            mysql.connection.commit()
            return 'success'
        elif request.form['submit_btn'] == 'Update Book Tier':
            tierid = request.form.get("tierid")
            isbn = request.form.get("isbn")
            bookname = request.form.get("bookName")
            if not isbn and not bookname:
                return "Both fields can not be empty"
            elif not bookname:
                cur.execute("UPDATE Book SET tierID = %(tierid)s WHERE ISBN = %(isbn)s", {'tierid': tierid, 'isbn': isbn})
            elif not isbn:
                cur.execute("UPDATE Book SET tierID = %(tierid)s WHERE bookName = %(bookname)s", {'tierid': tierid, 'bookname': bookname})
            # cur.execute("UPDATE Tier SET tierPrice = %(tierprice)s WHERE tierID = %(tierid)s", { 'tierprice': tierprice, 'tierid': tierid})
            mysql.connection.commit()
            return 'success'
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
    return render_template('adminbook.html', tiers = tiers, books = books)


if __name__ == '__main__':
    app.run()