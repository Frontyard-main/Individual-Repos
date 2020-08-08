import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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


def get_email_content(c_name,link):
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
                                <input type="hidden" name="company_name" value={c_name}/>
                                <button type="submit" style="display:inline-block;text-decoration:none;padding:15px 20px;background-color:#048c88;border:1px solid #048c88;border-radius:3px;color:#fff;font-weight:bold; font-size: medium">Verify</button>
                                
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



def mailing(cname,link,email):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("pjcip1999@gmail.com", "Chrish1999")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Thank you for your interest in Frontyard'
    msg['From'] = "pjcip1999@gmail.com"
    msg['To'] = email
    body = get_email_content(cname,link)
    body = MIMEText(body, 'html')
    msg.attach(body)
    s.sendmail("pjcip1999@gmail.com", email, msg.as_string())
    s.quit()


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
        password = None
        mail = request.form.get('mail_id')
        link = 'http://127.0.0.1:5000/path_to_pass'
        flag = False
        try:
            insert_values_registertable(c, c_name, u_name, phone,mail,password)

        except :
            flag = True
            return render_template('register.html',mail = mail,flag = flag)
    try:
        mailing(c_name,link, mail)
    except Exception as e:
        print(e)
        return jsonify({'Error':'Some error while mainling'})
    return render_template('checkEmail.html', mail=mail)

@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('index.html')

@app.route('/landingpage',methods=['POST','GET'])
def landingpage():
    c_name = request.form.get('c_name')
    c.execute("select * from register where company_name = '{}'".format(c_name))
    data = c.fetchone()
    # company_name,user_name,email_id ,ph_no, password
    uname = data[1]
    mail = data[2]
    phone = data[3]
    password = data[4]

    return render_template('home.html', cname=c_name, uname=uname, mail=mail, phone=phone, old=password)

@app.route('/login_check',methods=['POST','GET'])
#change this name to logic_check
def login_check():
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
        c.execute("select * from register where company_name = '{}'".format(c_name))
        data = c.fetchone()
        # company_name,user_name,email_id ,ph_no, password
        uname = data[1]
        mail = data[2]
        phone = data[3]
        password = data[4]
        if dbpass[0] == password:
            flag = False
            return render_template('home.html', cname=c_name, uname=uname, mail=mail, phone=phone, old=password)

        else:
            flag = True
            return render_template('login.html',flag = flag)

@app.route('/path_to_pass',methods=['POST','GET'])
#change this name to logic_check
def path_to_pass():
    if request.method == 'POST':
        c_name = request.form.get('company_name')
        print(c_name)
        if "/" in c_name or "\\" in c_name:
            c_name = c_name[:-1]
        print(c_name)
        return render_template('setPassword.html',cname = c_name)



@app.route('/create_password',methods=['POST','GET'])
def create_password():
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
        mail = data[3]
        phone = data[2]
        oldpass = data[4]
        print(uname,mail,phone,oldpass)
        if passn == passc:
             flag = False
             print("password matches")
             update_password(conn, (passn,c_name))
             c.execute("select * from register where company_name = '{}'".format(c_name))
             data = c.fetchone()
             # company_name,user_name,email_id ,ph_no, password
             newpass = data[4]
             print(newpass)
             return render_template('home.html',cname = c_name,uname=uname,mail=mail,phone=phone,old = newpass,flag = flag)
        else:
            flag = True
            print("password doesn't matches")
            return render_template('setPassword.html',cname = c_name,flag = flag)

if __name__ == '__main__':
    conn = main()
    c = conn.cursor()
    app.run()

