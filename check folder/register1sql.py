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
        conn = sqlite3.connect(db_file)
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
    database = "register1.db"

    sql_create_register_table = """ CREATE TABLE IF NOT EXISTS register (
                                        company_name text primary key ,
                                        email_id text,
                                        ph_no number)
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

    

def insert_values_registertable(c,val1,val2,val3):
    
    c.execute("""insert into register (company_name ,email_id ,ph_no ) values (?,?,?)""",(val1, val2, val3))

def update_registertable(conn,task):

    sql = ''' UPDATE register
              SET company_name = ? ,
                  email_id = ? ,
                  ph_no = ?
              WHERE company_name = ?'''
    c = conn.cursor()
    c.execute(sql,task)
    conn.commit()

def delete_from_registertable(conn, id):
   
    sql = 'DELETE FROM register WHERE company_name=?'
    c = conn.cursor()
    c.execute(sql, (id,))
    conn.commit()

def print_registertable(conn):
    c=conn.cursor()
    c.execute("select * from register")

    rows=c.fetchall()
    for r in rows:
        print(r)

if __name__ == '__main__':
    conn=main()
c=conn.cursor()    
r=input("do you want to insert?(y/n)")
while(r=='y'):
    v1=input("enter company name:")
    v2=input("enter your company email id:")
    v3=int(input("enter you phone number:"))

    insert_values_registertable(c,v1,v2,v3)
    r=input("do you want to insert?(y/n)")

with conn:
    update_registertable(conn, ('abc', 'abc@gmail.com',6908, 'abc'))
    delete_from_registertable(conn, 'val1')
    print_registertable(conn)

conn.commit()




