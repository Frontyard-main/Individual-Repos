import sqlite3
#defining connection
conn = sqlite3.connect('test.db')

#defining cursor
c=conn.cursor()
print(c)
#creating a table
c.execute("""
create table if not exists register(company_name text primary key ,email_id text,ph_no number)
""")
#inserting values to the table
#c.execute("""insert into register (company_name ,email_id ,ph_no ) values ('ABC company','abc@gmail.com',45678)""")
#c.execute("""insert into register (company_name ,email_id ,ph_no ) values ('hgjhv company','hghgf@gmail.com',987689)""")
conn.commit()

c.execute("select * from register")

rows=c.fetchall()
print(rows)
#for r in rows:
 #   print(r)
#close connection
conn.close()


