from config import *


# Define connection parameters
server = 'completefulserver.database.windows.net,1433'
database = 'MainDatabase'
username = 'JoeF'
password = 'SEg4FFFoQUP*5Fi**rD#kh3'
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


def get_connection():
    try:
        conn = odbc.connect(connection_string)
        return conn
    except odbc.Error as ex:
        print(f"Connection error: {ex}")
        return None

################################################TESTED AND FUNCTIONAL 10/22/24 JAF###################################################   
def get_all_redos():  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        query = "SELECT * FROM cake.JEWELRY_REDO"  
        cursor.execute(query)  
        tags = cursor.fetchall()  
        if tags:  
            tag_list = []  
            for tag in tags:  
                line_id, order_id, custom_id, sku, description, qty, status, cubby, order_date, scannedby, datetime = tag
                tag_list.append({  
                    "line_id": line_id,  
                    "order_id": order_id,  
                    "sku": sku,  
                    "description": description,  
                    "qty": qty,  
                    "status": status,  
                    "cubby": cubby,  
                    "order_date": order_date,
                    "scannedby" : scannedby,
                    "datetime" : datetime  
                })  
            return tag_list
        else:  
            print("No Tags found.")  
            return []  
    except odbc.Error as ex:  
        print(f"Error querying Tags: {ex}")  
        return []  
    finally:  
        if conn:  
            cursor.close()  
            conn.close()  
            print("Connection closed.")



################################################TESTED AND FUNCTIONAL 10/22/24 JAF###################################################   
def add_redo(order_id, reason, scannedby, time):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        #print("Connected to SQL Server")
        # Data to insert
        # Insert data into the table in the 'cake' schema
        match_query = "SELECT * FROM cake.JEWELRY_REDO WHERE order_id = ?"
        cursor.execute(match_query, (order_id,))
        order_id_check = cursor.fetchall()
        print(order_id_check)
        if order_id_check:
            print("Entry Already Exists in database", order_id_check)
            return "Order has already been submitted for redo"
        
        else:
            insert_data_query = '''
                INSERT INTO cake.JEWELRY_REDO (order_id, reason, scannedby, time)
                VALUES (?, ?, ?, ?)
                '''
            print(insert_data_query)
            cursor.execute(insert_data_query, (order_id, reason, scannedby, time))
            connection.commit()
            print("Data inserted successfully")
            return "Success"

    except odbc.Error as ex:
        print("ERROR: COULD NOT ENTER", order_id)
        return 'Issue with data format'

    finally:
        # Close the connection
        if connection:
            cursor.close()
            connection.close()
            #print("Connection closed")



#add_redo('ML1645510', 'Testing db', 'jaf', datetime.now())