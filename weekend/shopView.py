from flask import Flask, render_template, request, redirect, url_for, session, send_file
from datetime import datetime
from flask_mysql_connector import MySQL
import MySQLdb.cursors
import re
import json
import pdfkit
import os
from weekend import app

config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

mysql = MySQL(app)

@app.route("/shop")
def shop():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        try:
            conn = mysql.connection
            cur = conn.cursor()
            cur.execute("SELECT * from Item")
            products=cur.fetchall()
            print(products)
            cur.execute("SELECT * from CategoryTable")
            categories=cur.fetchall()
            mysql.connection.commit()
            return render_template('shopping.html',products=products,categories=categories)
        except ValueError:
            print("Error mysql connection 1")
            return
        # return render_template('dummy.html')
        print("SUCCESSFUL")
    return redirect(url_for('login'))

@app.route("/itemdetails/<int:id>", methods=['POST','GET'])
def itemdetails(id):
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        try:
            conn = mysql.connection
            cur = conn.cursor()
            id=str(id)
            cur.execute("SELECT itemNAME from Item WHERE itemID = %s", (id,))
            # cur.execute("SELECT itemNAME from Item WHERE itemID = '" + id + "'")
            name=cur.fetchone()[0]
            print(name)
            cur.execute("SELECT itemPRICE from Item WHERE itemID = %s", (id,))
            price=cur.fetchone()[0]
            print(price)
            cur.execute("SELECT itemIMAGE from Item WHERE itemID = %s", (id,))
            image=cur.fetchone()[0]
            print(image)
            cur.execute("SELECT brand from Item WHERE itemID = %s", (id,))
            Brand=cur.fetchone()[0]
            cur.execute("SELECT description from Item WHERE itemID = %s", (id,))
            Desc=cur.fetchone()[0]
            cur.execute("SELECT stock from Item WHERE itemID = %s", (id,))
            Stock=cur.fetchone()[0]
            Stock=int(Stock)
            if(Stock<=10):
                message='Hurry! Only few left'
            else:
                message='In Stock'
            mysql.connection.commit()
            return render_template('details.html',itemid=id,name=name,price=price,image=image,Brand=Brand,Desc=Desc,Stock=Stock,message=message,msg='')
        except ValueError:
            print("Error mysql connection 2")
            return
    return redirect(url_for('login'))
    
@app.route("/add/<int:id>", methods=['POST','GET'])
def add(id):
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        try:
            if request.method == "POST":
                if request.form['submit_btn'] == 'Add To Cart':
                    qty=request.form.get("total_quantity")
                    conn = mysql.connection
                    cur = conn.cursor()
                    cur.execute("SELECT neededQuantity from Cart where userID = %s and itemID = %s", (userID, id, ))
                    present_quantity = cur.fetchone()
                    qty=int(qty)
                    cur.execute("SELECT itemPRICE from Item WHERE itemID = %s", (id,))
                    cost=cur.fetchone()
                    if present_quantity is not None:
                        present_quantity = int(present_quantity[0])
                        print(present_quantity)
                        print(type(present_quantity))
                        price = int(int(cost[0])*qty)
                        print(qty)
                        print(price)
                        cur.execute("UPDATE Cart set neededQuantity = %s where userID = %s and itemID = %s", (qty, userID, id,))
                        cur.execute("UPDATE Cart set price = %s where userID = %s and itemID = %s", (price, userID, id,))
                    else:
                        print(present_quantity)
                        print("In none")
                        cur.execute("SELECT itemIMAGE from Item WHERE itemID = %s", (id,))
                        cart_image=cur.fetchone()
                        print(cart_image)
                        tot_itmprice=int(int(cost[0])*qty)
                        print(tot_itmprice)
                        print(id)
                        id=int(id)
                        cur.execute("INSERT INTO Cart (userID, itemID, neededQuantity, price) VALUES (%s, %s, %s, %s)",(userID, id, qty, tot_itmprice,))
                        # cur.execute("INSERT INTO Cart (itemID, neededQuantity, Image, price) VALUES (%s, %s, %s, %s)",(id,qty,cart_image[0],tot_itmprice,))
                        #cur.execute("INSERT INTO Cart (itemID, neededQuantity, Image, price) VALUES (%s, %s, %s, %s)",(2, 10, 'abc', 800))
                        #cur.execute("INSERT into Cart values(id,qty,'cart_image[0]',tot_itmprice)")
                    mysql.connection.commit()
                    return redirect(url_for('shop'))
        except ValueError:
            print("Error mysql connection 3")
            return 'failure'
    return redirect(url_for('login'))

# @app.route("/home", methods=['POST','GET'])
# def home():
#     return index()
    
@app.route("/shoppingcart", methods=['POST','GET'])
def shoppingcart():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        try:
            conn = mysql.connection
            cur = conn.cursor()
            cur.execute("SELECT itemID, neededQuantity, price from Cart where userID = %s", (userID, ))
            products=cur.fetchall()
            print(products)
            cur.execute("SELECT * from Item")
            itemdets=cur.fetchall()
            print(itemdets)
            mysql.connection.commit()
            return render_template('cart.html',products = products,itemdets = itemdets)
        except ValueError:
            print("Error mysql connection 4")
            return
    return redirect(url_for('login'))

    
@app.route("/payment", methods=['POST','GET'])
def payment():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        try:
            conn = mysql.connection
            cur = conn.cursor()
            cur.execute("SELECT sum(price) from Cart where userID = %s", (userID, ))
            total=cur.fetchone()
            print(total)
            # amount=cur.execute("SELECT sum(neededQuantity) from cart")
            return render_template('pay.html',total=total)
        except ValueError:
            print("Error mysql connection 5")
            return
    return redirect(url_for('login'))

@app.route('/delete1/<int:id>', methods=['POST','GET'])
def delete1(id):
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        try:
            conn = mysql.connection
            cur = conn.cursor()
            print(id)
            id=str(id)
            cur.execute("DELETE from Cart WHERE itemID = %s and userID = %s", (id, userID, ))
            mysql.connection.commit()
            cur.execute("SELECT itemID, neededQuantity, price from Cart where userID = %s", (userID, ))
            products=cur.fetchall()
            print(products)
            cur.execute("SeLECT * from Item")
            itemdets=cur.fetchall()
            print(itemdets)
            return render_template('cart.html',products=products, itemdets=itemdets) 
        except ValueError:
            print("Problem deleting item")
        mysql.connection.commit()
        return redirect(url_for('shop'))
    return redirect(url_for('login'))

boughtitms2 = []

@app.route("/final", methods=['POST','GET'])
def final():
    if 'loggedin' in session:
        global boughtitms2
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        if request.method == "POST":
            if request.form['submit_btn'] == 'Pay':
                cost=request.form.get("total_price")
                print(type(cost))
                conn = mysql.connection
                cur = conn.cursor()
                cur.execute("SELECT sum(price) from Cart where userID = %s", (userID,))
                total=cur.fetchone()
                print(type(total[0]))
                if int(cost)==int(total[0]):
                    cur.execute("SELECT itemID from Cart where userID = %s", (userID, ))
                    boughtitms=cur.fetchall()
                    cur.execute("SELECT i.itemName, c.neededQuantity, c.price from Cart c, item i where userID = %s and c.itemID = i.itemID", (userID, ))
                    boughtitms2=cur.fetchall()
                    print(boughtitms2)
                    date=datetime.date(datetime.now())
                    time=datetime.time(datetime.now())
                    for boughtitm in boughtitms:
                        # boughtitm=boughtitm[2:-3]
                        boughtitm=boughtitm[0]
                        print(boughtitm)
                        print(type(boughtitm))
                        boughtitm=str(boughtitm)
                        cur.execute("SELECT neededQuantity from Cart where itemID = %s and userID = %s", (boughtitm, userID,))
                        qty=cur.fetchone()[0]
                        print(qty)
                        #qty=int(qty[0])
                        cur.execute("SELECT price from Cart where itemID = %s and userID = %s", (boughtitm, userID,))
                        price=cur.fetchone()[0]
                        print(price)
                        #price=int(price[0])
                        cur.execute("INSERT INTO Bought (userID, itemID, boughtQuantity, amount, boughtDate,boughtTime) VALUES (%s, %s, %s, %s, %s, %s)",(userID, boughtitm,qty,price,date,time,))
                        cur.execute("DELETE FROM Cart where userID = %s and itemID = %s", (userID,boughtitm ,))
                        cur.execute("SELECT stock from Item where itemID = %s", (boughtitm, ))
                        stock = cur.fetchone()[0]
                        stock = int(stock) - int(qty)
                        cur.execute("UPDATE item set stock = %s where itemID = %s", (stock ,boughtitm ,))
                        # cur.execute("INSERT INTO Bought (itemID, boughtQuantity, amount, boughtDate,boughtTime) VALUES (%s, %s, %s, %s, %s)",(boughtitm,qty,price,date,time,))
                        #cur.execute("INSERT into Bought values(boughtitm,qty[0],price[0],date,time)")
                        mysql.connection.commit()
                        # return redirect(url_for('shop'))  
                    return render_template("bill.html", bought = boughtitms2)   
                # return 'Please Enter the correct amount to be paid'
    return redirect(url_for('login'))

@app.route("/bill", methods=['POST', 'GET'])
def bill():
    if request.method == 'POST':
        global boughtitms2
        html = render_template("bill2.html", bought = boughtitms2)
        print(boughtitms2)
        pdf = pdfkit.from_string(html, 'out.pdf', configuration = config, options = {"enable-local-file-access": ""})
        #response = make_response(pdf)
        #response.headers["Content-Type"] = "application/pdf"
        #response.headers["Content-Disposition"] = "inline; filename=output.pdf"
        path = "out.pdf"
        return send_file(path,as_attachment=True)

    # return render_template("bill.html", bought = boughtitms2)

@app.route("/boughtcart", methods=['POST','GET'])
def boughtcart():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from user WHERE userID = %s', (session['id'],))
        account = cursor.fetchone()
        userID = account[0]
        emailid = account[1]
        username = account[2]
        userTier = account[9]
        try:
            conn = mysql.connection
            cur = conn.cursor()  
            cur.execute("SELECT * from Bought where userID = %s", (userID, ))
            bgtitms=cur.fetchall()
            print(bgtitms)
            cur.execute("SELECT itemID,itemName,itemImage from Item")
            itmdetails=cur.fetchall()
            print(itmdetails)
            return render_template('bought.html', bgtitms = bgtitms, itmdetails = itmdetails)
        except ValueError:
            print("Error mysql connection 6")
            return
    return redirect(url_for('login'))
    
# filtering the book shelves
@app.route('/filterItems', methods = ["GET", "POST"])
def filter_items():
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
        fil_items = []
        categories = request.json
        for category in categories:
            print(category)
            cur.execute('''SELECT * FROM item i, categoryTable c where i.categoryID = c.categoryID and c.category = %s''', (category, ))
            items = cur.fetchall()
            print(items)
            for item in items:
                fil_items.append(item)
                print(item)
            # print(genre)
        fil_items = json.dumps(fil_items)
        return fil_items

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/searchItems', methods=["GET", "POST"])
def search_items():
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
        search_items = []
        search_by = request.json
        search_by = "%" + search_by + "%";
        print(search_by)
        cur.execute("SELECT * from Item i, CategoryTable c where c.categoryID = i.categoryID and (i.itemName like %s or c.category like %s or i.brand like %s)", (search_by, search_by, search_by, ))
        products=cur.fetchall()
        print(products)
        for product in products:
            search_items.append(product)
        search_items = json.dumps(search_items)
        return search_items

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/emptyCart', methods = ["GET"])
def empty_cart():
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
        cur.execute("DELETE from Cart where userID = %s", (userID,))
        mysql.connection.commit()
        return redirect(url_for('shoppingcart'))

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



