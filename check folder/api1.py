from flask import Flask, request, render_template , url_for, redirect
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