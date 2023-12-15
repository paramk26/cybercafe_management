#function definiton
def run(code):
    cursor.execute(code)
    value=cursor.fetchall()
    mycon.commit()
    return value
def table(nest):
    for lst in nest:
        print("-"*30*len(lst))
        for value in lst:
            print(value,end=" "*(27-len(str(value))))
            print("|",end=" "*3)
        print('')
         
#constants
y="y"
unique="no"
users={}
login="un"
menu=(("S.NO","SERVICE","RATE"),)




#-------------------------------------MAIN----------------------------------

import mysql.connector as sql
mycon=sql.connect(host="localhost",user="root",password="mysql",database='cybercafe')   
cursor=mycon.cursor()
print("""
-------------------------------------------------------------------------------
----------------------WELCOME TO THE CYBER CAFE--------------------------------
-------------------------------------------------------------------------------
""","\n")

print("""
---------------USER STATUS-------------------
1.ADMIN
2.CUSTOMER""",'\n')
c1=int(input("Enter your choice number"))


#STAFF LOGIN
#ADMIN PASSWORD- mysql
if c1==1 :
    pswrd=input("Enter password-")
    if pswrd=="mysql":                         
        print("""------------LOGIN SUCCESSFUL-----------------""","\n")                        
        while y=="y":
            print("""
----------ADMIN'S MENU-----------------------
1.SHOW TRANSACTION HISTORY
2.SHOW BOOKINGS
3.UPDATE RATES
4.EXIT
---------------------------------------------""",'\n')
            c2=int(input("Enter choice number"))
            print("\n\n")
            if c2==1:
                
                transaction= run("""SELECT  c.name,
                                            r.service,
                                            r.rate * t.qty as total
                                    FROM transaction t
                                    JOIN customers c 
                                    ON t.cus_id = c.cus_id
                                    JOIN rate r 
                                    ON t.service_id = r.service_id """)
                print("\n","TRANSACTION HISTORY:-")
                print("="*90)
                table((("USERNAME","SERVICE","TOTAL"),))
                table(transaction)
                print('='*90,'\n')
                      
            if c2==2:
                
                bookings=run("""SELECT	c.name,
                                        r.service,
                                        b.date,
                                        b.time,
                                        b.qty
                                FROM bookings b
                                JOIN rate r 
                                ON b.service_id = r.service_id
                                JOIN customers c
                                ON b.cus_id = c.cus_id""")
                print("="*5*30)
                table((("NAME","SYSTEM","DATE","TIME","HOURS"),))
                table(bookings)
                print("="*5*30)
                
            if c2==3:
                rate=run("SELECT * FROM rate")
                print('='*3*30)
                table(menu)
                table(rate)
                print('='*3*30,'\n')
                c2=int(input("Enter item number to modify-"))
                newr=int(input("Enter new rate-"))
                run(""" UPDATE rate
                        SET rate={new}
                        WHERE service_id={no}""".format(new=newr,no=c2))               
            if c2==4:
                y="n"
    else:
        print("""
-----------WRONG PASSWORD------------------""")


#---------------------------------------USER LOGIN-----------------------------------------------------
        
if c1==2:
    for row in run("SELECT name,password FROM customers"):
        users[row[0]]= row[1]
   
    print("""
-----------LOGIN---------------------------
1.NEW USER
2.EXSISTING USER""")
    c2=int(input("Enter your choice"))
    if c2==1:     
        while unique=="no":
            name=input("Enter your username")
            if name not in users.keys():
                password= input("enter password")
                run("INSERT INTO customers(name,password) VALUES('{}','{}');".format(name,password))
                unique="yes"
            else:
                print("Username already exists.Try another username")
    if c2==2:
        while login=="un":
            name=input("Enter your name")
            password=input("Enter password")
            if (name,password) in users.items():
                login="su"
            else:
                print("Credentials mismatch. Please try again")

    cid=run("SELECT cus_id FROM customers WHERE name='{}';".format(name))[0][0]
    #extracting cus_id #because fetchall returns a row in tuple form inside a tuple
    print("""--------------LOGIN SUCCESSFUL---------------""")
          


    
#-------------------------------------------main menu---------------------------------------------

    
    while y=="y":
        print("""
---------------SERVICES-----------------------
1 Printout
2 Gaming
3 Net surfing 
4 Advance booking
5 Transaction History
6 Exit
----------------------------------------------
""")
        c3=int(input("Enter choice number-"))

        if c3==1:
            printout=run("SELECT * FROM rate WHERE service_id IN (1,2);")
            print("="*90)
            table(menu)
            table(printout)
            print("="*90,'\n')
            c4= int(input("Enter choice number-"))
            qty=int(input("Enter number of papers-"))
            run("INSERT INTO transaction(cus_id,service_id,qty,date) VALUES({},{},{},CURDATE());".format(cid,c4,qty))
            tid=run("SELECT trans_id FROM transaction ORDER BY trans_id DESC LIMIT 1")[0][0]  #extracting trans_id
            
        if c3==2:
            game=run("SELECT * FROM rate WHERE service_id BETWEEN 5 AND 11")
            print("="*90)
            table(menu)
            table(game)
            print("="*90,'\n')
            c4=int(input("Enter choice number"))
            qty=int(input("Enter number of hours-"))
            run("INSERT INTO transaction(cus_id,service_id,qty,date) VALUES({},{},{},CURDATE());".format(cid,c4,qty))
            tid=run("SELECT trans_id FROM transaction ORDER BY trans_id DESC LIMIT 1")[0][0]
        if c3==3:
            qty=int(input("Enter number of hours-"))
            run("INSERT INTO transaction(cus_id,service_id,qty,date) VALUES({},{},{},CURDATE());".format(cid,4,qty))
            tid=run("SELECT trans_id FROM transaction ORDER BY trans_id DESC LIMIT 1")[0][0]
            
        if c3==4:
            adv=run("SELECT * FROM rate WHERE service_id BETWEEN 4 AND 11")
            print("="*90)
            table(menu)
            table(adv)
            print("="*90,'\n')
            c4=int(input("Enter choice number-"))
            qty=int(input("Enter number of hour-"))
            date=input("Enter date in yyyy-mm-dd format-")
            time=input("Enter time in hh:mm:ss format-")
            run("INSERT INTO bookings VALUES({},{},'{}','{}',{});".format(cid,c4,date,time,qty))
        

        if c3==5:
            cus_trans= run("""SELECT r.Service,
                                r.rate * t.qty AS Total,
                                t.date
                                FROM transaction t
                                JOIN rate r
                                ON t.service_id = r.service_id
                                WHERE cus_id={}""".format(cid))
            print("Your transactions are:",'\n')
            print("="*90)
            table(cus_trans)
            print("="*90)
        if c3 in (1,2,3):
            bill=run("""SELECT r.Service,
                                r.rate * t.qty AS Total,
                                t.date
                                FROM transaction t
                                JOIN rate r
                                ON t.service_id = r.service_id
                                WHERE trans_id={}""".format(tid))
            print("="*42,"BILL","="*42)
            
            table((('SERVICE','TOTAL','DATE'),))
            table(bill)
            print("="*90)
            
        if c3==6:
            print("""
-------------------------------------------------------------------------------
--------------------------------THANKYOU---------------------------------------
-------------------------------VISIT AGAIN-------------------------------------
-------------------------------------------------------------------------------""")
            mycon.close()
            y="n"
            

























            




            

