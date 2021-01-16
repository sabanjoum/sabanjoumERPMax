from datetime import date
from flask import Flask , render_template,url_for,request,session
from mysql.connector import MySQLConnection 
import mysql.connector as mysql
'SET GLOBAL connect_timeout=86400';
'SET GLOBAL wait_timeout=86400';
'SET GLOBAL interactive_timeout=86400'; 


app = Flask(__name__)
class erpMaxClass:
    


    mydb = mysql.connect(
    host = "127.0.0.1",
    autocommit=True,
    user = "root",
    password = "123456",
    database="erpMax"
    ) 
    """ database connected """ 
    global cursor
    cursor = mydb.cursor(buffered=True)
    """ cursor created """ 
    if mydb.is_connected:
        print ('CONNECTED')





    @app.route('/')
    @app.route('/view', methods=['GET','POST'])
    def view():
        
        v=erpMaxClass()
        v.viewProduct()
        return render_template('viewProduct.html', time=time, data=data, rows=rows)

            
    @app.route('/viewProduct', methods=['GET','POST'])
    def viewProduct(self):
        cursor.execute("SELECT * FROM product")
        global rows 
        rows=cursor.fetchall() 
        cursor.execute("SELECT * FROM location")
        global data
        data=cursor.fetchall() 
        cursor.execute("SELECT * FROM productmovement")
        global time
        time=cursor.fetchall() 

    



    @app.route('/add_pro', methods=['GET','POST'])
    def add_pro(self):
        if request.method == 'POST' and 'productName' in request.form and 'locationName' in request.form and 'qty' in request.form :
            print("  ") 
            productName = request.form['productName']  
            global locationName
            locationName = request.form['locationName']  
            qty = request.form['qty']  
            cursor.execute("INSERT INTO product (`productName`) VALUES ('%s')" % (productName))
            print(productName)    
            cursor.execute("SELECT productID from product where productName = ('%s') " % productName)
            productID =   cursor.fetchone()        
            cursor.execute("update product set locationName = ('%s') where productID = ('%s')  " % (locationName, productID[0]))
            cursor.execute("update product set qty = ('%s') where productID = ('%s')  " % (qty, productID[0]))
            print(qty)
            pid=productID[0]
            print(pid) 
           
           
            cursor.execute("INSERT into productmovement  (`productID`) values ('%s')" %(productID[0]))  
            
            cursor.execute("update productMovement set qty = ('%s') where productID = ('%s')  " % (qty, productID[0]))
            


            cursor.execute("SELECT locationName from location")
            location =   cursor.fetchall()       
            cursor.execute("update productmovement set from_location = ('%s') where productID = ('%s')  " % (locationName, productID[0])) 
            print(locationName)        
            print("  ") 
            

            
    @app.route('/addproduct', methods=['GET', 'POST'])
    def addproduct():
        ap=erpMaxClass()
        ap.add_pro()    
        ap.viewProduct()    
        return render_template('addProduct.html', time=time, data=data, rows=rows)
        """ mydb.commit() """ 
        
                        
    @app.route('/viewProductMovements', methods=['GET','POST'])
    def viewProductMovements():
         
        cursor.execute("SELECT * FROM productmovement")
        global time 
        time=cursor.fetchall() 

        return render_template('viewProductMovements.html',    time=time)
        
     

    @app.route('/edit_pro', methods=['POST','GET'])
    def edit_pro(self):
        if request.method == 'POST' and 'productName' in request.form  and 'oldProductName' in request.form  and 'to_location' in request.form   :
            print('1')        
            productName = request.form['productName'] 
            oldProductName = request.form['oldProductName'] 
            to_location = request.form['to_location']
            print('2') 
            print('3') 
            print(oldProductName)        
            cursor.execute(" update product SET productName = REPLACE( productName , '%s' , '%s' ) " % (oldProductName, productName))
            """ mydb.commit() """ 
            
            print(productName) 
            cursor.execute(" SELECT locationName from product where productName=('%s')"  %  (productName))
            pl= cursor.fetchone()
            print(pl[0])
            cursor.execute(" SELECT productID from product where productName=('%s')"  %  (productName))
            productID= cursor.fetchone()[0]
            print(productID) 
           
            """ 
            cursor.execute(" update product SET locationName = REPLACE( locationName , '%s' , '%s' ) " % (pl[0], locationName )) """
            cursor.execute("update productmovement set to_location = ('%s') where productID = ('%s')  " % (to_location, productID)) 
            print(to_location)

             
            
            


    @app.route('/editproduct', methods=['POST','GET'])
    def editproduct():
        ep=erpMaxClass()
        ep.edit_pro()
        return render_template('editProduct.html')
    
    """
    cursor.execute("  SELECT MAX(productID) as length FROM product  ")
    """     
    @app.route('/delete_pro', methods=['POST','GET'])
    def delete_pro(self):
        if request.method == 'POST' and 'productName' in request.form  :
            print('Deleting on way')
            productName = request.form['productName']  
            print(productName)                    
            cursor.execute("SELECT productID FROM product WHERE  productName  = ('%s') " % (productName))
            productID= cursor.fetchone()
            print(productID)
            cursor.execute("DELETE FROM product WHERE  productID = ('%s') " % ( productID))
            cursor.execute("DELETE FROM productmovement WHERE  productID = ('%s') " % ( productID))
            print(productID)         
            
    @app.route('/deleteproduct', methods=['POST','GET'])
    def deleteProduct():
        dp=erpMaxClass() 
 
        dp.delete_pro()
        return render_template('deleteProduct.html')

    @app.route('/add_loc', methods=['GET','POST'])
    def add_loc(self):
        if request.method == 'POST' and 'locationName' in request.form : 
            print('Alo')
            locationName = request.form['locationName']
            
            cursor.execute("INSERT INTO location (`locationName`) VALUES ('%s') " % (locationName))
            print(locationName)
            
            """ mydb.commit() """ 
         

    @app.route('/addlocation', methods=['GET', 'POST'])
    def addlocation():
        al=erpMaxClass()
        al.add_loc()
        return render_template('addLocation.html' )



    @app.route('/viewLocation', methods=['GET', 'POST'])
    def viewLocation():
        v=erpMaxClass()
        v.viewProduct()
        return render_template('viewLocation.html' , data=data)

        


    @app.route('/edit_loc', methods=['POST','GET'])
    def edit_loc(self):
        if request.method == 'POST' and 'locationName' in request.form  and 'locationNameNew' in request.form  :
            locationNameNew = request.form['locationNameNew']
            locationName  = request.form['locationName']
            print(locationName)
                 
            cursor.execute(" update location SET locationName = REPLACE( locationName , '%s' , '%s' ) " % (locationName, locationNameNew))
  
            
            print(locationNameNew)   

    @app.route('/editLocation', methods=['POST','GET'])
    def editLocation():
        dl=erpMaxClass() 
        dl.edit_loc()
        return render_template('editLocation.html')



        
    @app.route('/delete_loc', methods=['POST','GET'])
    def delete_loc(self):
        if request.method == 'POST' and 'locationName' in request.form  :
            print('Deleting on way')
            locationName = request.form['locationName']  
            print(locationName)        
            cursor.execute("DELETE FROM location WHERE locationName = ('%s') " % (locationName))
            cursor.execute("SELECT locationName FROM location  ")
            locations=cursor.fetchall()
 
            print(locations)

    @app.route('/deleteLocation', methods=['POST','GET'])
    def deleteLocation():
        dl=erpMaxClass() 
        dl.delete_loc()
        return render_template('deleteLocation.html')



if __name__ == "__main__":
    app.run(debug=True)