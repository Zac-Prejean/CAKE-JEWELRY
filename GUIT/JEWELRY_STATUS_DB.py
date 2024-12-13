import pyodbc as odbc
from datetime import date, datetime


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

# ################################################TESTED AND FUNCTIONAL 10/22/24 JAF###################################################   
# def get_all_status():  
#     conn = get_connection()  
#     try:  
#         cursor = conn.cursor()  
#         query = "SELECT * FROM cake.JEWELRY_STATUS"  
#         cursor.execute(query)  
#         tags = cursor.fetchall()  
#         if tags:  
#             tag_list = []  
#             for tag in tags:  
#                 line_id, order_id, custom_id, sku, description, qty, status, cubby, order_date, scannedby, datetime = tag
#                 tag_list.append({  
#                     "line_id": line_id,  
#                     "order_id": order_id,  
#                     "sku": sku,  
#                     "description": description,  
#                     "qty": qty,  
#                     "status": status,  
#                     "cubby": cubby,  
#                     "order_date": order_date,
#                     "scannedby" : scannedby,
#                     "datetime" : datetime  
#                 })  
#             return tag_list
#         else:  
#             print("No Tags found.")  
#             return []  
#     except odbc.Error as ex:  
#         print(f"Error querying Tags: {ex}")  
#         return []  
#     finally:  
#         if conn:  
#             cursor.close()  
#             conn.close()  
#             print("Connection closed.")



# ################################################TESTED AND FUNCTIONAL 10/22/24 JAF###################################################   
def add_tag(line_id, order_id, custom_id, sku, description, qty, status, cubby, order_date, scannedby, datetime):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        #print("Connected to SQL Server")
        # Data to insert
        # Insert data into the table in the 'cake' schema
        match_query = "SELECT * FROM cake.JEWELRY_STATUS WHERE line_id = ?"
        cursor.execute(match_query, (line_id,))
        line_id_check = cursor.fetchall()
        if line_id_check:
            print("Entry Already Exists in database", line_id_check)
        
        else:
            insert_data_query = '''
                INSERT INTO cake.JEWELRY_STATUS (line_id, order_id, custom_id, sku, description, qty, status, cubby, order_date, scannedby, datetime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
            cursor.execute(insert_data_query, (line_id, order_id, custom_id, sku, description, qty, status, cubby, order_date, scannedby, datetime))
            connection.commit()
        #print("Data inserted successfully")

    except odbc.Error as ex:
        print("ERROR: COULD NOT ENTER", line_id)

    finally:
        # Close the connection
        if connection:
            cursor.close()
            connection.close()
            #print("Connection closed")


# ################################################TESTED AND FUNCTIONAL 10/22/24 JAF################################################### 
def get_order_by_tag(line_id):  
    conn = get_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            # Find cubbies that match the provided orderID  
            match_query = "SELECT * FROM cake.JEWELRY_STATUS WHERE line_id = ?"  
            cursor.execute(match_query, (line_id,))  
            order = cursor.fetchall()  
  
            if order:  
                for tag in order:  
                    line_id, order_id, custom_id, sku, description, qty, status, cubby, order_date, scannedby, datetime, total_qty = tag  
                    if status != 'shipped':  
                        return order_id  
                    else:  
                        return f"Warning this order has been shipped: {order_id}"  
        except odbc.Error as ex:  
            print(f"There was a problem fetching this order number {ex}")  
        finally:  
            cursor.close()  
            conn.close()  

# ################################################TESTED AND FUNCTIONAL 10/22/24 JAF###################################################        
def find_tags_by_order(order_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            tag_list = []
            # Find cubbies that match the provided orderID
            match_query = "SELECT * FROM cake.JEWELRY_STATUS WHERE order_id = ?"
            cursor.execute(match_query, (order_id,))
            tags = cursor.fetchall()
            
            if tags:
                for tag in tags:
                    line_id, order_id, custom_id, sku, description, qty, status, cubby, order_date, scannedby, datetime = tag
                    tag_list.append(line_id)
                return tag_list
                
            else:
                return 'Order number has been shipped or does not exist'

        except odbc.Error as ex:
            print(f"There was a problem fetching this order number {ex}")
        finally:
            cursor.close()
            conn.close()


# ###############################################Waiting on update permissions##################################################
# def update_cubby(line_id, cubby):
#     # SQL query to update the status based on the line_id
#     update_status_query = '''
#         UPDATE cake.JEWELRY_STATUS
#         SET cubby = ?
#         WHERE line_id = ?
#         '''

#     try:
#         # Connect to the SQL Server
#         conn = get_connection()
#         cursor = conn.cursor()

#         # Update the status
#         cursor.execute(update_status_query, (cubby, line_id))
#         conn.commit()

#         # Check how many rows were affected
#         if cursor.rowcount > 0:
#             print(f"Cubby updated successfully for line_id {line_id}.")
#         else:
#             print(f"No record found with line_id {line_id}.")

#     except odbc.Error as ex:
#         print("Error:", ex)

#     finally:
#         if conn:
#             cursor.close()
#             conn.close()
#             #print("Connection closed.")
# ###############################################Waiting on update permissions################################################## 

# def update_custom_id(line_id, custom_id):
#     # SQL query to update the status based on the line_id
#     update_status_query = '''
#         UPDATE cake.JEWELRY_STATUS
#         SET custom_id = ?
#         WHERE line_id = ?
#         '''

#     try:
#         # Connect to the SQL Server
#         conn = get_connection()
#         cursor = conn.cursor()

#         # Update the status
#         cursor.execute(update_status_query, (custom_id, line_id))
#         conn.commit()

#         # Check how many rows were affected
#         if cursor.rowcount > 0:
#             print(f"custom_id updated successfully for line_id {line_id}.")
#         else:
#             print(f"No record found with line_id {line_id}.")

#     except odbc.Error as ex:
#         print("Error:", ex)

#     finally:
#         if conn:
#             cursor.close()
#             conn.close()
#             #print("Connection closed.")

###############################################Waiting on update permissions##################################################   
# def update_status(line_id, new_status):
#     # SQL query to update the status based on the tag_ID
#     update_status_query = '''
#         UPDATE cake.JEWELRY_STATUS
#         SET status = ?
#         WHERE line_id = ?
#         '''

#     try:
#         # Connect to the SQL Server
#         conn = get_connection()
#         cursor = conn.cursor()

#         # Update the status
#         cursor.execute(update_status_query, (new_status, line_id))
#         conn.commit()

#         # Check how many rows were affected
#         if cursor.rowcount > 0:
#             print(f"Status updated successfully for line_id {line_id}.")
#         else:
#             print(f"No record found with line_id {line_id}.")

#     except odbc.Error as ex:
#         print("Error:", ex)

#     finally:
#         if conn:
#             cursor.close()
#             conn.close()
#             print("Connection closed.")

# ################################################TESTED AND FUNCTIONAL 10/22/24 JAF################################################### 
# def delete_cubby(cubby):  
#     conn = get_connection()  
#     if conn:  
#         try:  
#             cursor = conn.cursor()  
#             # Delete the cubby with the specified cubbyID  
#             delete_query = "DELETE FROM cake.JEWELRY_STATUS WHERE cubby = ?"  
#             cursor.execute(delete_query, (cubby,))  
#             conn.commit()  
#             if cursor.rowcount > 0:  
#                 print(f"Cubby with cubbyID {cubby} deleted successfully.")  
#             else:  
#                 print(f"No cubby found with cubby: {cubby}")  
#         except odbc.Error as ex:  
#             print(f"Error deleting cubby: {ex}")  
#         finally:  
#             cursor.close()  
#             conn.close()  


# ######################################################Testing Modules #####################################################################
# # add_tag('13149528326217', 'ML1638408', '','PPCLPHC-BRC-GLD', 'Mint Paperclip Bracelet', 4, 'status', 0, '10/22/2024', 'jaf', datetime.now())
# data = get_all_status()
# print(data)
# # update_status('13149528326217', 'picked')
# # list = find_tags_by_order('ML1638349')
# print(list)
# # order = get_order_by_tag('13149447356489')
# # print(order)
# # delete_cubby(0)