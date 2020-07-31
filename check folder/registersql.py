import sqlite3
#defining connection
conn = sqlite3.connect('register.db')

#defining cursor
c=conn.cursor()
print(c)
#creating a table
c.execute("""
create table if not exists register(company_name text primary key ,email_id text,ph_no number)
""")
#inserting values to the table
c.execute("""insert into register (company_name ,email_id ,ph_no ) values ('ABC company','abc@gmail.com',45678)""")
c.execute("""insert into register (company_name ,email_id ,ph_no ) values ('hgjhv company','hghgf@gmail.com',987689)""")
c.execute("""insert into register (company_name ,email_id ,ph_no ) values ('all in one','all@gmail.com',56784)""")


c.execute("select * from register")

rows=c.fetchall()
for r in rows:
   print(r)
#update the email_id of all in one company
c.execute("update register set email_id='allinone@gmail.com' where company_name='all in one';")
#checking after updation
c.execute("select * from register")

rows=c.fetchall()
for r in rows:
   print(r)
#delete the values in ABC company
c.execute("delete from register where company_name='ABC company'")
#checking after deletion
c.execute("select * from register")

rows=c.fetchall()
for r in rows:
   print(r)

conn.commit()
#close connection
conn.close()


