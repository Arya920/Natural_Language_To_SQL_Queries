### In this file we will store all the codes related to connection to my sql server.

import mysql.connector
import pandas as pd
###======================================================================database details-=======================================================
def database_details(host,user,password):
    
        connection = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            buffered = True
            )
        cursor = connection.cursor()
        databases = ("Show databases")
        cursor.execute(databases)
        db = []
        for (databases) in cursor:
            db.append(databases[0])

        cursor.close()
        connection.close()
        return db, len(db)

#### =========================================================================retrieving the tables==========================================================
def tables_in_this_DB(host,user,password,db_name):
    db_config = {
        'host':host,
        'user': user,
        'password': password,
        'database': db_name,
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query1 = "SHOW TABLES"
    cursor.execute(query1)
    tables = cursor.fetchall()

    cursor.close()
    connection.close()
    return tables, len(tables)

#### ==================================================Printing the tables=======================================================================
def printing_tables(host,user,password,db_name):
    db_config = {
        'host':host,
        'user': user,
        'password': password,
        'database': db_name,
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    table_names = [table[0] for table in cursor.fetchall()]

    tables_data = {}

    for table_name in table_names:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=col_names)

        tables_data[table_name] = df
    cursor.close()
    connection.close()
    return tables_data



def create_table_command(host,user,password,db_name):
    db_config = {
        'host': host,
        'user': user,
        'password': password,
        'database': db_name,
    }

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SHOW TABLES"
    cursor.execute(query)
    table_names = [table[0] for table in cursor.fetchall()]

    create_table_statements = {}
    for table_name in table_names:
        query = f"SHOW CREATE TABLE {table_name}"
        cursor.execute(query)
        create_table_data = cursor.fetchone()

        if create_table_data:
            # The CREATE TABLE statement is in the second element of the tuple
            create_table_statement = create_table_data[1]
            create_table_statement = create_table_statement.split("ENGINE=")[0].strip()
            create_table_statements[table_name] = create_table_statement

    cursor.close()
    connection.close()

    return create_table_statements


def retrieve_result(host,user,password,db_name,query):
    db_config = {
        'host': host,
        'user': user,
        'password': password,
        'database': db_name,
    }

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = query
    cursor.execute(query)
    res = cursor.fetchall()

    cursor.close()
    connection.close()
    return res