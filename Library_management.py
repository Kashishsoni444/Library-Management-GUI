import mysql.connector
from datetime import date
import os
import platform
 

'''FUNCTIONS FOR BOOKRECORDS'''
def insertdata():
      #FOR INSERTING DATA
    try:
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor() 
        bno=int(input("Enter Book Code: "))
        bname=input("Enter Book Name: ")
        auth=input("Enter Book Author's Name: ")
        price=int(input("Enter Book Price: "))
        publ=input("Enter Book Publisher: ")
        qty=int(input("Enter Quantity purchased: "))
        print('Enter Date of Purchase (Date/Month and Year separately: ')
        dd=int(input('Enter the Date: '))
        mm=int(input('Enter the Month: '))
        yy=int(input('Enter the Year: '))
        d=date(yy,mm,dd)
        qry="INSERT INTO BOOKRECORDS VALUES({},'{}','{}',{},'{}',{},'{}')".format(bno,bname,auth,price,publ,qty,d)
        cursor.execute(qry)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Record inserted.")
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()

def deletebook():       #FOR DELETING RECORDS
    try:
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor()
        bno=int(input("Enter the Code of the Book to be deleted from the library: "))
        qry=("delete from bookrecords where bno={}".format(bno))
        cursor.execute(qry)
        cnx.commit()
        cnx.close()
        print(cursor.rowcount,"Record(s) Deleted Successfully!")
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()
             
             
        

def SearchBookRec():       #FOR SEARCHING A BOOK IN THE RECORDS
    try:
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor()
        bno=int(input("Enter the Book to be Searched from the library: "))
        qry=("select *  from bookrecords where bno={}".format(bno))
        cursor.execute(qry)
        rcount=0
        for (bno,bname,auth,price,publ,qty,date_of_purchase) in cursor:
            rcount+=1
            print("============================================================")
            print("Book Code :",bno)
            print("Book Name:",bname)
            print("Author of the Book :",auth)
            print("Price of theBook :",price)
            print("Publisher of the Book :",publ)
            print("Total Quantity in hand  :",qty)
            print("Purchased on:",date_of_purchase)
            print("============================================================")
        if rcount%2==0:
            input("Press any key to continue")
            clrscreen()
        print(rcount,"Record(s) found")
        cnx.commit()
        cursor.close()
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()
         
def UpdateBook():  #FOR UPDATING BOOK RECORDS 
    try:
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor()
        bno=int(input("Enter the Book code of the book to be Updated from the library: "))
        print("Enter New Data")
        bname=input("Enter Book Name: ")
        auth=input("Enter Book Author's Name: ")
        price=int(input("Enter Book Price: "))
        publ=input("Enter Book Publisher: ")
        qty=int(input("Enter Quantity purchased: "))
        print('Enter Date of Purchase (Date/Month and Year separately: ')
        dd=int(input('Enter the Date: '))
        mm=int(input('Enter the Month: '))
        yy=int(input('Enter the Year: '))
        Date_of_Purchase=date(yy,mm,dd)
        qry="update bookrecords set bname='%s',auth='%s',price=%s,publ='%s',qty=%s,date_of_purchase='%s' where bno=%s" % (bname,auth,price,publ,qty,Date_of_Purchase,bno)
        cursor.execute(qry)
        cnx.commit()
        cursor.close()
        cnx.close()
        print(cursor.rowcount,'Record(s)  updated successfully!')
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()

####################################################################################

'''FUNCTIONS FOR SEARCHING,RETURNING AND ISSUING BOOKS'''


def SearchIssuedBook():    #FOR SEARCHING A BOOK
    try:
        os.system('cls')
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor()
        mno=int(input("Enter the Member code to Search the book: "))
        qry=("select *  from issue where mno={}".format(mno))
        cursor.execute(qry)
        rcount=0
        for (bno,mno,d_o_issue,d_o_ret) in cursor:
            rcount+=1
            print("============================================================")
            print("1.Book Code :",bno)
            print("2.Member Code:",mno)
            print("Date of Issue:",d_o_issue)
            print("Date of Return :",d_o_ret)
            print("============================================================")
        if rcount%2==0:
            input("Press any key to continue")
            clrscreen()
        print(rcount,"Record(s) found")
        cnx.commit()
        cursor.close()
        print('you have done it!')
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()


def issuebook():
    try:   #FOR ISSUING A BOOK
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor()
        bno=int(input("Enter Book Code to issue:  "))
        mno=int(input("Enter Member Code: "))
        print('Enter Date of Purchase (Date/Month and Year separately: ')
        dd=int(input('Enter the Date: '))
        mm=int(input('Enter the Month: '))
        yy=int(input('Enter the Year: '))
        d=date(yy,mm,dd)
        qry="INSERT INTO ISSUE(bno,mno,d_o_issue) VALUES(%s,%s,'%s')" %(bno,mno,d)
        cursor.execute(qry)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Record inserted.")
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()

def returnbook():  #TO UPDATE BOOK RETURN STATUS
    try:
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor()
        bno=int(input("Enter the Book code of the book to be Returned to the library: "))
        mno=int(input("Enter Member Code: "))
        rd=date.today()
        qry="update issue set d_o_ret='%s' where bno=%s and mno=%s" %(rd,bno,mno)
        cursor.execute(qry)
        cnx.commit()
        cursor.close()
        cnx.close()
        print(cursor.rowcount,'Record(s)  updated successfully!')
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()

###############################################################################################
'''FUNCTIONS FOR INSERTING,DELETING,SEARCHING AND UPDATING MEMBERS OFHE LIBRARY'''

def clrscreen():
    print('\n'*5)

def insertmember():    #FOR ADDING A NEW MEMBER
    try:
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor()
        mno=input("Enter Member Code: ")
        mname=input("Enter Member Name: ")
        print('Enter Date of Purchase (Date/Month and Year separately: ')
        dd=int(input('Enter the Date: '))
        mm=int(input('Enter the Month: '))
        yy=int(input('Enter the Year: '))
        addr=input("Enter Member's Address: ")
        mob=input("Enter Member's Mobile number: ")
        d=date(yy,mm,dd)
        qry="INSERT INTO MEMBER VALUES('{}','{}','{}','{}','{}')".format(mno,mname,d,addr,mob)
        cursor.execute(qry)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Record inserted.")
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()


def deletemember():    #FOR DELETING A MEMBER
    try:
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor()
        mno=int(input("Enter the Code of the Member to be deleted from the library: "))
        qry="delete from member where mno={}".format(mno)
        cursor.execute(qry)
        cnx.commit()
        cnx.close()
        print(cursor.rowcount,"Record(s) Deleted Successfully!")
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()


def searchmember():    #FOR SEARCHING A MEMBER
    try:
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor()
        mno=int(input("Enter the Mno of the Member to be Searched from the library: "))
        qry="select *  from member where mno={}".format(mno)
        cursor.execute(qry)
        rcount=0
        for (mno,mname,date_of_membership,addr,mob) in cursor:
            rcount+=1
            print("============================================================")
            print("Member Code :",mno)
            print("Member's  Name:",mname)
            print("Date of Membership :",date_of_membership)
            print("Address of the Member :",addr)
            print("Mobile number of the Member :",mob)
            print("============================================================")
        if rcount%2==0:
            input("Press any key to continue")
            clrscreen()
        print(rcount,"Record(s) found")
        cnx.commit()
        cursor.close()
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()

def updatemember():   #FOR UPDATING INFORMATION ABOUT MEMBERS
    try:
        cnx=mysql.connector.connect(user="root",host="localhost",passwd="1234",database="Library")
        cursor=cnx.cursor()
        mno=int(input("Enter the Member code of the Member to be Updated from the library: "))
        print("Enter New Data")
        mname=input("Enter Member Name: ")
        print('Enter Date of Purchase (Date/Month and Year separately: ')
        dd=int(input('Enter the Date: '))
        mm=int(input('Enter the Month: '))
        yy=int(input('Enter the Year: '))
        addr=input("Enter Member's Address: ")
        mob=int(input("Enter Member's Mobile number: "))
        Date_of_membership=date(yy,mm,dd)
        qry="update member set mname='%s',date_of_membership='%s',addr='%s',mob=%s where mno=%s" % (mname,Date_of_membership,addr,mob,mno)
        cursor.execute(qry)
        cnx.commit()
        cursor.close()
        cnx.close()
        print(cursor.rowcount,'Record(s)  updated successfully!')
    except Exception:
        print("Sorry,something went wrong")
    cnx.close()

########################################################################################
'''DESIGNING MENU'''

def clrscreen():
    print('\n'*5)
    
def menubook():
    while True:
        clrscreen()
        print('\t\t\tBOOK MANAGEMENT\n')
        print('===========================================================================')
        print('1.ADD BOOK RECORD')
        print('2.SEARCH BOOK RECORD')
        print('3.DELETE BOOK RECORD')
        print('4.UPDATE BOOK RECORD')
        print('5.RETURN THE IN MENU')
        print('===========================================================================')
        ch=int(input('Enter your choice between 1-5------>'))
        if ch==1:
            insertdata()
        elif ch==2:
            SearchBookRec()
        elif ch==3:
            deletebook()
        elif ch==4:
            UpdateBook()
        elif ch==5:
            return
        else:
            print('Wrong choice.....Enter  your choice again:')
            x=input('press any key to continue')

#---------------------------------------------------------------------------------------------------------------------------------------------------------
def membermenu():
    while True:
        clrscreen()
        print('\t\t\tMEMBER RECORD MANAGEMENT\n')
        print('===========================================================================')
        print('1.ADD MEMBER RECORD')
        print('2.SEARCH MEMBER RECORD')
        print('3.DELETE MEMBER RECORD')
        print('4.UPDATE MEMBER RECORD')
        print('5.RETURN THE IN MENU')
        print('===========================================================================')
        ch=int(input('Enter your choice between 1-5------>'))
        if ch==1:
            insertmember()
        elif ch==2:
            searchmember()
        elif ch==3:
            deletemember()
        elif ch==4:
            updatemember()
        elif ch==5:
            return
        else:
            print('Wrong choice.....Enter  your choice again:')
            x=input('press any key to continue')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
def issuemenu():
    while True:
        clrscreen()
        print('\t\t\tISSUED BOOK MANAGEMENT\n')
        print('===========================================================================')
        print('1.ISSUE BOOK')
        print('2.SEARCH ISSUE BOOK RECORD')
        print('3.RETURN ISSUED BOOK')
        print('4.RETURN THE IN MENU')
        print('===========================================================================')
        ch=int(input('Enter your choice between 1-4------>'))
        if ch==1:
            issuebook()
        elif ch==2:
            SearchIssuedBook()
        elif ch==3:
            returnbook()
        elif ch==4:
            return
        else:
            print('Wrong choice.....Enter  your choice again:')
            x=input('press any key to continue')

################################################################################################
"""DESIGNING FORMAT OF THE MAIN WINDOW"""

while True:
    print('\t\t\tLIBRARY MANAGEMENT\n')
    print('===========================================================================')
    print('1.BOOK MANAGEMENT')
    print('2.MEMBERS MANAGEMENT')
    print('3.ISSUE/RETURN BOOK')
    print('4.EXIT')
    print('===========================================================================')
    ch=int(input('Enter your choice between 1-4------>'))
    if ch==1:
        menubook()
    elif ch==2:
        membermenu()
    elif ch==3:
        issuemenu()
    elif ch==4:
        break
    else:
        print('Wrong choice.....Enter  your choice again:')
        x=input('press any key to continue')
