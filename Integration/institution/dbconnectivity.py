import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, url_for, redirect, render_template,jsonify
import sqlite3
from sqlite3 import Error
import math
import random
from datetime import date, datetime


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
    database = "request.db"

    sql_create_register_table = """ CREATE TABLE IF NOT EXISTS request (
                                        request_id integer primary key AUTOINCREMENT,
                                        college_name text,
                                        reason text,
                                        status text,
                                        poc_mail text,
                                        poc_ph_no number,
                                        t_start_date DATE,
                                        t_end_date DATE,
                                        date_on_request_made DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        approximate_no_of_students number,
                                        UNIQUE(college_name)
                                        )
                                        ;"""
    sql_create_institution_table = """ CREATE TABLE IF NOT EXISTS institution (
                                            institution_name text primary key ,
                                            ins_id number,
                                            email_id text,
                                            ph_no number,
                                            password text)
                                            ;"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        try:
            create_table(conn, sql_create_register_table)
            print("Table created")
        except Error as e:
            print(e)
            return jsonify({'error':'Register Table not created'})

        try:
            create_table(conn, sql_create_institution_table)
            print("Table created")
        except Error as e:
            print(e)
            return jsonify({'error':'Institution Table not created'})

    else:
        print("Error! cannot create the database connection.")
    return conn


def insert_values_registertable(c, val1, val2, val3,val4, val5,val6,val7,val8):
    c.execute("""insert into request (college_name,reason,status,poc_mail,poc_ph_no,t_start_date,t_end_date,approximate_no_of_students) values (?,?,?,?,?,?,?,?)""", (val1, val2, val3,val4,val5,val6,val7,val8))
    conn.commit()

def insert_values_institutiontable(c, val1, val2, val3,val4, val5):
    c.execute("""insert into institution (institution_name,ins_id,email_id,ph_no,password) values (?,?,?,?,?)""", (val1, val2, val3,val4,val5))
    conn.commit()

def update_password(conn, task):
    sql = ''' UPDATE register
              SET password = ? 
              WHERE company_name = ?'''
    c = conn.cursor()
    c.execute(sql, task)
    conn.commit()

def update_status(conn, task):
    sql = ''' UPDATE request
              SET status = ? 
              WHERE college_name = ?'''
    c = conn.cursor()
    c.execute(sql, task)
    conn.commit()


def get_email_content(mail, link,password):
    return f'''
        <div style="background-color:#fff;margin:0 auto 0 auto;padding:30px 0 30px 0;color:#4f565d;font-size:13px;line-height:20px;font-family:'Helvetica Neue',Arial,sans-serif;text-align:left">
            <center>
            <table style="width:550px;text-align:center">
                <tbody><tr>
                    <td style="padding:0 0 20px 0;border-bottom:1px solid #e9edee; text-align:left; ">
                        <h2 style="font-family: trebuchet ms,sans-serif;">
                            Greetings! 
                        </h2>
                        <div style="font-size: larger;">
                            Thank you for your Interest to Open an Account with us.                
                        </div>
                        <br>
                    </td>
                </tr>
                <tr>
                    <td colspan="2" style="padding-bottom:10px; border-bottom:1px solid #e9edee; ">               
                        </span>
                            <p style="margin:20 10px 10px 10px;padding:0">
                                <span style="font-family: trebuchet ms,sans-serif; color: #4f565d; font-size: 15px; line-height: 20px;">
                                    Below is the Link to create your password
                                </span>
                            </p>
                        <span>
                            <p>
                            <form action = {link} method="POST" class="login_form">
                                <p>Mail_id:{mail}</p>
                                <p>Password:{password}</p>

                                <button type="submit" style="display:inline-block;text-decoration:none;padding:15px 20px;background-color:#048c88;border:1px solid #048c88;border-radius:3px;color:#fff;font-weight:bold; font-size: medium">Login</button>

                            </form>
                            </p>
                        </span>

                    </td>
                </tr>
                <tr>
                    <td style="padding-bottom: 20px; text-align:left;">
                         <p style="margin-block-start: 0px; font-size: larger;">
                            Thank you for your time. Have a nice day! 
                        </p>

                    </td>
                </tr>
                <tr>
                    <td colspan="2" style="padding:30px 0 0 0;border-top:1px solid #e9edee;color:#9b9fa5">
                        If you have any questions you can get in touch at <a style="color:#666d74;text-decoration:none" href="mailto:pjcip1999@gmail.com" target="_blank">pjcip1999@gmail.com</a>
                    </td>
                </tr>
            </tbody></table>
            </center>
        </div></div>'''


def mailing(link, email,password):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("pjcip1999@gmail.com", "password")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Thank you for your interest in Frontyard'
    msg['From'] = "pjcip1999@gmail.com"
    msg['To'] = email
    body = get_email_content(email, link,password)
    body = MIMEText(body, 'html')
    msg.attach(body)
    s.sendmail("pjcip1999@gmail.com", email, msg.as_string())
    s.quit()

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def register():
    return render_template('request.html')

# @app.route('/request',methods=['POST','GET'])
# def request():
#     return render_template('request.html')

@app.route('/insertion',methods =['POST','GET'])
def insert():
    if request.method == 'POST':
        c_name = request.form.get('college_name')
        reason = request.form.get('reason')
        poc_ph_no = request.form.get('phone_no')
        status = "pending"
        t_e_d = request.form.get('t_end_date')
        t_s_d = request.form.get('t_start_date')
        poc_mail = request.form.get('mail_id')
        nos = request.form.get('anos')
        try:
            insert_values_registertable(c,c_name,reason,status,poc_mail, poc_ph_no,t_s_d,t_e_d,nos)
        except Error as er:
            print(er)
            return jsonify({'error':'Error on inserting into db'})
        return render_template('index.html',flag = False)

@app.route('/status',methods =['POST'])
def status():
    if request.method == "POST":
        if request.form.get("accept"):
            c_name = request.form.get("accept")
            status = "accepted"
            print(c_name, status)
            update_status(conn, (status, c_name))
            c.execute('''select * from request where college_name ='{}' '''.format(c_name))
            data = c.fetchone()
            ins_id = data[0]
            ins_name = data[1]
            email_id = data[4]
            ph_no = data[5]

            digits = [i for i in range(0, 10)]

            random_str = ""

            for i in range(8):
                index = math.floor(random.random() * 10)
                random_str += str(digits[index])
            print(random_str)
            password = random_str
            link = 'http://127.0.0.1:5000/login'
            try:
                insert_values_institutiontable(c, ins_name,ins_id,email_id,ph_no,password)
            except Error as er:
                print(er)
                return jsonify("Error on inserting the table")

            try:
                mailing(link, email_id, password)
            except Exception as e:
                print(e)
                return jsonify({'Error': 'Some error while mailing'})

            return redirect(url_for('pending_request'))

        elif request.form.get("reject"):
            c_name = request.form.get("reject")
            status = "rejected"
            update_status(conn, (status, c_name))
            print(status,c_name)
            return redirect(url_for('pending_request'))

@app.route('/restore',methods =['POST'])
def restore():
    if request.method == "POST":
        if request.form.get("restore"):
            c_name = request.form.get("restore")
            status = "pending"
            print(c_name, status)
            update_status(conn, (status, c_name))
            return redirect(url_for('rejected_request'))


@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')
@app.route('/login_check',methods=['POST','GET'])
#change this name to logic_check
def login_check():
    if request.method == 'POST':
        c_name = request.form.get('college_name')
        password = request.form.get('pass')
        print(c_name,password)
        c.execute("select * from institution")
        row = c.fetchall()
        print(row)
        # c.execute("select password from institution where college_name = '{}'".format(c_name))
        # dbpass = c.fetchone()
        # print(dbpass)
        # print(dbpass[0])
        c.execute("select * from institution where institution_name = '{}'".format(c_name))
        data = c.fetchone()
        # company_name,user_name,email_id ,ph_no, password
        c_id = data[1]
        mail = data[2]
        phone = data[3]
        dbpass = data[4]
        print(dbpass)
        if dbpass == password:
            flag = False
            #return render_template('home.html', cname=c_name, uname=uname, mail=mail, phone=phone, old=password)
            msg = {'college_name':c_name,'college_id':c_id,'poc_mail':mail,'poc_phone':phone,'password':dbpass}
            print(msg)
            return jsonify(msg)
        else:
            flag = True
            return render_template('login.html',flag = flag)


@app.route('/pending_request')
def pending_request():

    c.execute('''select * from request where status = 'pending' ''')
    l = c.fetchall()

    final = []

    for i in range(len(l)):
        item = []
        temp = {}
        temp['College_name'] = l[i][1]
        temp['Reason'] = l[i][2]
        temp['email'] = l[i][4]
        temp['phone'] = l[i][5]
        temp['start_date'] = l[i][6]
        temp['end_date'] = l[i][7]
        temp['requested_date'] = l[i][8]
        temp['Count'] = l[i][9]
        item.append(temp.copy())
        final.append(item.copy())

    return render_template('layout.html', data=final)

@app.route('/rejected_request')
def rejected_request():

    c.execute('''select * from request where status = 'rejected' ''')
    l = c.fetchall()

    final = []

    for i in range(len(l)):
        item = []
        temp = {}
        temp['College_name'] = l[i][1]
        temp['Reason'] = l[i][2]
        temp['email'] = l[i][4]
        temp['phone'] = l[i][5]
        temp['start_date'] = l[i][6]
        temp['end_date'] = l[i][7]
        temp['requested_date'] = l[i][8]
        temp['Count'] = l[i][9]
        item.append(temp.copy())
        final.append(item.copy())

    return render_template('rej_layout.html', data=final)


#This below api is created just for testing
@app.route('/insertion_check',methods =['POST','GET'])
def insert_check():
    if request.method == 'POST':
        c_name = request.form.get('college_name')
        reason = request.form.get('reason')
        poc_ph_no = request.form.get('phone_no')
        status = "pending"
        t_e_d = request.form.get('t_end_date')
        t_s_d = request.form.get('t_start_date')
        print(type(t_e_d))
        print(t_e_d)
        print(type(t_s_d))
        print(t_s_d)
        #t_e_d = datetime.datetime.strptime(t_e_d,'%y-%m-%d')
        poc_mail = request.form.get('mail_id')

        try:
            insert_values_registertable(c,c_name,reason,status,poc_mail, poc_ph_no,t_s_d,t_e_d)
            conn.commit()
        except Error as er:
            print(er)
            return jsonify({'error':'Error on inserting into db'})
        try:
            c.execute('''select * from request ''')
            data = c.fetchone()
            print(data)
        except:
            return jsonify({'error': 'No rows found'})
        try:
            c.execute('''select * from request where college_name ='{}' '''.format(c_name))
            data = c.fetchone()
        except Error as e:
            print(e)
            return jsonify({'error':'Unableto fetch'})
        r_id = data[0]
        c_name = data[1]
        reason = data[2]
        status = data[3]
        poc_mail = data[4]
        poc_ph_no = data[5]
        t_s_d = data[6]
        t_e_d = data[7]
        d_o_r_m = data[8]
        msg ={'rid':r_id,'college':c_name,'reason':reason,'status':status,'mail':poc_mail,'phone':poc_ph_no,'start':t_s_d,'end':t_e_d,'requested date':d_o_r_m}

        return jsonify({'Status': 'Success','msg':msg})



if __name__ == '__main__':
    conn = main()
    c = conn.cursor()
    app.run()