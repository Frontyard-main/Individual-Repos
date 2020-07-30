
from flask import Flask, request, jsonify, render_template, redirect
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
        conn = sqlite3.connect(db_file, check_same_thread=False)
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
    database = "register.db"

    sql_create_register_table = """ CREATE TABLE IF NOT EXISTS register (
                                        company_name text primary key ,
                                        user_name text,
                                        email_id text,
                                        ph_no number,
                                        password text)
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


def insert_values_registertable(c, val1, val2, val3,val4, val5):
    c.execute("""insert into register (company_name,user_name,email_id ,ph_no, password) values (?,?,?,?,?)""", (val1, val2, val3,val4,val5))


def update_password(conn, task):
    sql = ''' UPDATE register
              SET password = ? 
              WHERE company_name = ?'''
    c = conn.cursor()
    c.execute(sql, task)
    conn.commit()


app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def register():

    return render_template('register.html')

@app.route('/verification',methods=['POST','GET'])
def verify():

    if request.method == 'POST':
        c_name = request.form.get('company_name')
        u_name = request.form.get('user_name')
        phone = request.form.get('phone_no')
        password = request.form.get('pass')
        mail = request.form.get('mail_id')
        insert_values_registertable(c, c_name, u_name, phone,mail,password)
        return render_template('verification.html',mail = mail)

@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')

@app.route('/home_page',methods=['POST','GET'])

def home_page():
    if request.method == 'POST':
        c_name = request.form.get('company_name')
        password = request.form.get('pass')
        print(c_name,password)
        c.execute("select * from register")
        row = c.fetchall()
        print(row)
        c.execute("select password from register where company_name = '{}'".format(c_name))
        dbpass = c.fetchone()
        print(dbpass)
        print(dbpass[0])
        if dbpass[0] == password:
            flag = False
            return render_template('home_page.html',cname = c_name,flag = flag)

        else:
            flag = True
            return render_template('login.html',flag = flag)

@app.route('/reset_con',methods=['POST','GET'])
def reset_password():
    print ('entered reset')
    if request.method == 'POST':
        c_name = request.form.get('c_name')
        passn = request.form.get('n_pass')
        passc = request.form.get('c_pass')
        print(c_name,passn,passc)
        c.execute("select * from register where company_name = '{}'".format(c_name))
        data = c.fetchone()
        #company_name,user_name,email_id ,ph_no, password
        uname = data[1]
        mail = data[2]
        phone = data[3]
        oldpass = data[4]
        print(uname,mail,phone,oldpass)
        if passn == passc:
             flag = False
             update_password(conn, (passn,c_name))
             c.execute("select * from register where company_name = '{}'".format(c_name))
             data = c.fetchone()
             # company_name,user_name,email_id ,ph_no, password
             newpass = data[4]
             print(newpass)
             return render_template('home.html',cname = c_name,uname=uname,mail=mail,phone=phone,old = oldpass,new = newpass,flag = flag)
        else:
            flag = True
            return render_template('home_page.html',flag = flag)

if __name__ == '__main__':
    conn = main()
    c = conn.cursor()
    app.run()

