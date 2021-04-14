from datetime import datetime
from flask import Flask,render_template,request
from flask_mysql_connector import MySQL
app= Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sanvidhruva@01'
app.config['MYSQL_DATABASE'] = 'dbs1'

@app.route("/")
def index():
    try:
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("SELECT * from Item")
        products=cur.fetchall()
        cur.execute("SELECT * from CategoryTable")
        categories=cur.fetchall()
        mysql.connection.commit()
        return render_template('shopping.html',products=products,categories=categories)
    except ValueError:
        print("Error mysql connection 1")
        return
    # return render_template('dummy.html')
    print("SUCCESSFUL")

@app.route("/itemdetails/<int:id>", methods=['POST','GET'])
def itemdetails(id):
    try:
        conn = mysql.connection
        cur = conn.cursor()
        id=str(id)
        cur.execute("SELECT itemNAME from Item WHERE itemID = '" + id + "'")
        name=cur.fetchone()[0]
        print(name)
        cur.execute("SELECT itemPRICE from Item WHERE itemID = '" + id + "'")
        price=cur.fetchone()[0]
        print(price)
        cur.execute("SELECT itemIMAGE from Item WHERE itemID = '" + id + "'")
        image=cur.fetchone()[0]
        print(image)
        cur.execute("SELECT brand from Item WHERE itemID = '" + id + "'")
        Brand=cur.fetchone()[0]
        cur.execute("SELECT description from Item WHERE itemID = '" + id + "'")
        Desc=cur.fetchone()[0]
        cur.execute("SELECT stock from Item WHERE itemID = '" + id + "'")
        Stock=cur.fetchone()[0]
        Stock=int(Stock)
        if(Stock<=10):
            message='Hurry! Only few left'
        else:
            message='In Stock'
        mysql.connection.commit()
        return render_template('details.html',itemid=id,name=name,price=price,image=image,Brand=Brand,Desc=Desc,Stock=Stock,message=message)
    except ValueError:
        print("Error mysql connection 2")
        return
    
@app.route("/add/<int:id>", methods=['POST','GET'])
def add(id):
    try:
        if request.method == "POST":
            if request.form['submit_btn'] == 'Add To Cart':
                qty=request.form.get("total_quantity")
                conn = mysql.connection
                cur = conn.cursor()
                id=str(id)
                print(id, qty)
                qty=int(qty)
                cur.execute("SELECT itemPRICE from Item WHERE itemID = '" + id + "'")
                cost=cur.fetchone()
                cur.execute("SELECT itemIMAGE from Item WHERE itemID = '" + id + "'")
                cart_image=cur.fetchone()
                print(cart_image)
                tot_itmprice=int(int(cost[0])*qty)
                print(tot_itmprice)
                print(id)
                id=int(id)
                #cur.execute("INSERT INTO Cart (itemID, neededQuantity, Image, price) VALUES (%s, %s, %s, %s)",(2, 10, 'abc', 800))
                cur.execute("INSERT INTO Cart (itemID, neededQuantity, Image, price) VALUES (%s, %s, %s, %s)",(id,qty,cart_image[0],tot_itmprice))
                #cur.execute("INSERT into Cart values(id,qty,'cart_image[0]',tot_itmprice)")
                mysql.connection.commit()
                return 'success'
    except ValueError:
        print("Error mysql connection 3")
        return 'failure'

@app.route("/home", methods=['POST','GET'])
def home():
    return index()
    
@app.route("/shoppingcart", methods=['POST','GET'])
def shoppingcart():
    try:
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("SELECT * from Cart")
        products=cur.fetchall()
        print(products)
        cur.execute("SeLECT itemID,itemName from Item")
        itemdets=cur.fetchall()
        print(itemdets)
        mysql.connection.commit()
        return render_template('cart.html',products=products,itemdets=itemdets)
    except ValueError:
        print("Error mysql connection 4")
        return
    
@app.route("/payment", methods=['POST','GET'])
def payment():
    try:
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("SELECT sum(price) from Cart")
        total=cur.fetchone()
        print(total)
        # amount=cur.execute("SELECT sum(neededQuantity) from cart")
        return render_template('pay.html',total=total)
    except ValueError:
        print("Error mysql connection 5")
        return

@app.route('/delete1/<int:id>', methods=['POST','GET'])
def delete1(id):
    try:
        conn = mysql.connection
        cur = conn.cursor()
        print(id)
        id=str(id)
        cur.execute("DELETE from Cart WHERE itemID = '" + id + "'")
        mysql.connection.commit()
        cur.execute("SELECT * from Cart")
        products=cur.fetchall()
        return render_template('cart.html',products=products)
        
    except ValueError:
        print("Problem deleting item")
    mysql.connection.commit()
    return 'success'

@app.route("/final", methods=['POST','GET'])
def final():
    if request.method == "POST":
        if request.form['submit_btn'] == 'Pay':
            cost=request.form.get("total_price")
            print(type(cost))
            conn = mysql.connection
            cur = conn.cursor()
            cur.execute("SELECT sum(price) from Cart")
            total=cur.fetchone()
            print(type(total[0]))
            if int(cost)==int(total[0]):
                cur.execute("SELECT itemID from Cart")
                boughtitms=cur.fetchall()
                print(boughtitms)
                
               
                date=datetime.date(datetime.now())
                time=datetime.time(datetime.now())
                for boughtitm in boughtitms:
                    # boughtitm=boughtitm[2:-3]
                    boughtitm=boughtitm[0]
                    print(boughtitm)
                    print(type(boughtitm))
                    
                    boughtitm=str(boughtitm)
                    

                    cur.execute("SELECT neededQuantity from Cart where itemID= '" + boughtitm + "'")
                    qty=cur.fetchone()[0]
                    print(qty)
                    #qty=int(qty[0])
                    cur.execute("SELECT price from Cart where itemID='" + boughtitm + "'")
                    price=cur.fetchone()[0]
                    print(price)
                    #price=int(price[0])
                    cur.execute("INSERT INTO Bought (itemID, boughtQuantity, amount, boughtDate,boughtTime) VALUES (%s, %s, %s, %s, %s)",(boughtitm,qty,price,date,time,))
                    #cur.execute("INSERT into Bought values(boughtitm,qty[0],price[0],date,time)")
                    mysql.connection.commit()
                    return 'success'     
            return 'Please Enter the correct amount to be paid'

@app.route("/boughtcart", methods=['POST','GET'])
def boughtcart():
    try:
        conn = mysql.connection
        cur = conn.cursor()  
        cur.execute("SELECT * from Bought")
        bgtitms=cur.fetchall()
        cur.execute("SELECT itemID,itemName,itemImage from Item")
        itmdetails=cur.fetchall()
        return render_template('bought.html',bgtitms=bgtitms,itmdetails=itmdetails)
    except ValueError:
        print("Error mysql connection 6")
        return
    
if __name__ == "__main__":
    app.run()
