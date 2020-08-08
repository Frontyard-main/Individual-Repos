from flask import Flask, flash, jsonify,redirect, render_template, \
     request, url_for
import sqlite3
from sqlite3 import Error

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
    database = "request5.db"

    sql_create_register_table = """ CREATE TABLE IF NOT EXISTS request5(request_id integer  primary key AUTOINCREMENT,
                                        college_name text,
                                        reason_for_prefering_us text,
                                        tentative_start_date date,
                                        tentative_end_date date,
                                        approximate_no_of_students number,
                                        point_of_contact_mail text,
                                        point_of_contact_no text,
                                        status text,
                                        date_on_request_made DATETIME DEFAULT CURRENT_TIMESTAMP)
                                        ;"""
 

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_register_table)

    else:
        print("Error! cannot create the database connection.")
    return conn


def insert_values_registertable(c, val1, val2, val3,val4, val5,val6,val7,val8):
    c.execute("""insert into request5 (college_name,reason_for_prefering_us,tentative_start_date,tentative_end_date,approximate_no_of_students,point_of_contact_mail,point_of_contact_no,status) values (?,?,?,?,?,?,?,?)""", (val1, val2, val3,val4,val5,val6,val7,val8))

    print("inserted")
    print("Hey!Thanks for Registering,we are happy to work with you.Please keep checking your mail for login details,we will be sending you.Keep in update")

    
    
app = Flask(__name__)
app.secret_key = 'random string'
@app.route('/',methods=['POST','GET'])
def register():
    flag=None
    return render_template('collegereg.html',flag= False,flag1=False)


@app.route('/verification',methods=['POST'])
def insertion():
  
    error = None
    if request.method == 'POST':
        
        college_name=request.form.get('College_Name')
        reason_for_prefering_us=request.form.get('Reason_for_Prefering_us')
        tentative_start_date=request.form.get('Tentative_Start_Date')
        tentative_end_date=request.form.get('Tentative_End_Date')
        approximate_no_of_students=request.form.get('Approximate_No_of_Students')
        point_of_contact_mail=request.form.get('Point_of_Contact_Mail')
        point_of_contact_no=request.form.get('Point_of_Contact')
        status="PENDING"
        #flag = None
        print(college_name,reason_for_prefering_us,tentative_start_date,tentative_end_date,approximate_no_of_students,point_of_contact_mail,point_of_contact_no)
        
        c.execute("select point_of_contact_mail from request5 where college_name = '{}'".format(college_name))
        data = c.fetchone()
        
        if data == None :
            flag = True
            flag1 = False
            insert_values_registertable(c,college_name,reason_for_prefering_us,tentative_start_date,tentative_end_date,approximate_no_of_students,point_of_contact_mail,point_of_contact_no,status)
            print("Requested")
            return render_template('collegereg.html',flag = flag,flag1=flag1)
        else:
            flag = False
            flag1=True
            print("Not Requested yet")
            print("Hey!Thanks for choosing us.We could see your Insttution  that was provided is already registered. Could please contact'{}'to get the login details for your institution.".format(data))
            return render_template('collegereg.html',flag = flag ,flag1=flag1,mail=data)
       

if __name__ == '__main__':
    conn=main()
    c=conn.cursor() 
    app.run()  
    
       
conn.commit()
   