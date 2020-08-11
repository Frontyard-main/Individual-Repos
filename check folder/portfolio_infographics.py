
import sqlite3
from sqlite3 import Error
import datetime 
#from datetime import date
from flask import  Flask, request, render_template , url_for, redirect,jsonify


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file,check_same_thread=False)
        return conn
    except Error as e:
        print(e)

    return conn
    


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

    
def main():
    database = "admin.db"

    sql_create_institution = """ CREATE TABLE IF NOT EXISTS institution(
                                        ins_id number primary key,
                                        ins_name text,
                                        ins_mail text,
                                        password text,
                                        ins_contact_no number)
                                        ;"""
    sql_create_contract = """ CREATE TABLE IF NOT EXISTS contract (
                                        contract_id number primary key,
                                        ins_id text,
                                        start_date date,
                                        end_date date,
                                        no_of_students number,
                                        point_of_contact_mail text,
                                        point_of_contact_no number,
                                        contract_status text)
                                        ;"""
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_institution)
        create_table(conn, sql_create_contract)

    else:
        print("Error! cannot create the database connection.")
    return conn

    

def insert_values_institution(c,val1,val2,val3,val4,val5):
    
    c.execute("""insert into institution(ins_id,
                                        ins_name,
                                        ins_mail,
                                        password,
                                        ins_contact_no ) values (?,?,?,?,?)""",(val1, val2, val3,val4,val5))

def insert_values_contract(c,val1,val2,val3,val4,val5,val6,val7,val8):
    c.execute("""insert into contract(contract_id ,
                                        ins_id ,
                                        start_date ,
                                        end_date,
                                        no_of_students,
                                        point_of_contact_mail,
                                        point_of_contact_no ,
                                        contract_status ) values (?,?,?,?,?,?,?,?)""",(val1, val2, val3,val4,val5,val6,val7,val8))
    


def print_institution(conn):
    c=conn.cursor()
    c.execute("select * from institution")

    rows=c.fetchall()
    for r in rows:
        print(r)

def print_contract(conn):
    c=conn.cursor()
    c.execute("select * from contract")

    rows=c.fetchall()
    for r in rows:
        print(r)
app=Flask(__name__)

@app.route('/')

def portfolio():

    c.execute('''select contract_id,ins_name,no_of_students,start_date,end_date from contract c,institution i where c.ins_id=i.ins_id and contract_status='active' ;''')
    present=list(c.fetchall()) 
    print(present)   
    c.execute('''select contract_id,ins_name,no_of_students,start_date,end_date from contract c,institution i where c.ins_id=i.ins_id and contract_status='ended';''')
    past=list(c.fetchall())
    print(past)
    # return render_template({frontend.html,"present":present,"past":past})
    return render_template("portfolio.html",past=past,present=present); 



# @app.route('/infographics',methods=['POST'])
# def infographics():
#     c.execute("select contract_id,ins_name,start_date,end_date from contract c,institution i where c.ins_id=i.ins_id and contract_status='active' ;")
#     val=[]
#     ins_name=[]
#     contract_id=[]
#     data=list(c.fetchall())
#     for i in data:
#         print(type(i[-1]))
#         ins_name.append(i[1])
#         contract_id.append(i[0])
#         diff = datetime.datetime.strptime(i[-1],'%Y-%m-%d') - datetime.datetime.strptime(i[-2],'%Y-%m-%d')
#         print(diff)
#         print(datetime.date.today())
#         Year= datetime.date.today().year
#         Month= datetime.date.today().month
#         Day = datetime.date.today().day
#         to_day=str(Year)+"-"+str(Month)+"-"+str(Day)    
#         #percent = (datetime.date.today()- datetime.datetime.strptime(i[-2],'%Y-%m-%d') / diff)*100
#         percent = ((datetime.datetime.strptime(to_day,'%Y-%m-%d')- datetime.datetime.strptime(i[-2],'%Y-%m-%d')) / diff)*100
#         print(percent)
#         print(ins_name)
#         print(contract_id)
#         val.append(ins_name)
#         val.append(contract_id)
#         val.append(percent)
#         print(val)
#     return jsonify({"percent":val})
 


if __name__ == '__main__':
    conn=main()
    c=conn.cursor()    
    r=input("do you want to insert into instituion table?(y/n)")
    while(r=='y'):
        v1=int(input("enter institution id:"))
        v2=input("enter institution name:")
        v3=input("enter mail_id:")
        v4=input("enter password:")
        v5=int(input("enter contact number:"))

        insert_values_institution(c,v1,v2,v3,v4,v5)
        r=input("do you want to insert instituion table?(y/n)")

    p=input("do you want to insert into contract table?(y/n)")
    while(p=='y'):
        v1=int(input("enter contract id:"))
        v2=int(input("enter ins_id:"))
                                        
        v3=input("enter start_date:")
        v4=input("enter end_date:")
        v5=int(input("enter no_of_students:"))
        v6=input("enter point_of_contact_mail:")
        v7=int(input("enter point_of_contact_no :"))
        v8=input("enter contract_status")
        insert_values_contract(c,v1,v2,v3,v4,v5,v6,v7,v8)

        p=input("do you want to insert contract table?(y/n)")

    with conn:
        print_institution(conn)
        print_contract(conn)

    app.run()