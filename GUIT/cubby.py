# cubby.py

import pyodbc as odbc  
from datetime import datetime  
from flask import request, jsonify  
  
# Define connection parameters  
server = 'completefulserver.database.windows.net,1433'  
database = 'MainDatabase'  
username = 'JoeF'  
password = 'SEg4FFFoQUP*5Fi**rD#kh3'  
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'  
  
def get_connection():  
    try:  
        conn = odbc.connect(connection_string)  
        print("Database connection established")  
        return conn  
    except odbc.Error as ex:  
        print(f"Connection error: {ex}")  
        return None  
  
def get_all_cubbies():  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        query = "SELECT * FROM cake.JEWELRY_CUBBY"  
        cursor.execute(query)  
        cubbies = cursor.fetchall()  
        if cubbies:  
            cubby_list = []  
            for cubby in cubbies:  
                cubby_list.append({  
                    "itemID": cubby[0],  
                    "orderID": cubby[1],  
                    "qty": cubby[2],  
                    "sku": cubby[3],  
                    "scannedBy": cubby[4],  
                    "cubbyID": cubby[5],  
                    "orderDate": cubby[6],  
                    "dateTime": cubby[7].strftime('%Y-%m-%d %H:%M'),  
                    "total_qty": cubby[8]  
                })  
            return cubby_list  
        else:  
            print("No cubbies found.")  
            return []  
    except odbc.Error as ex:  
        print(f"Error querying cubbies: {ex}")  
        return []  
    finally:  
        if conn:  
            cursor.close()  
            conn.close()  
            print("Connection closed.")  
  
def create_cubby():  
    conn = get_connection()  
    cubbyID = None  # Initialize cubbyID  
  
    if conn:  
        try:  
            cursor = conn.cursor()  
            # Find the next available cubbyID between 1 and 500  
            cursor.execute("""  
                SELECT MIN(cubbyID + 1)  
                FROM (  
                    SELECT 0 AS cubbyID  
                    UNION  
                    SELECT cubbyID  
                    FROM cake.JEWELRY_CUBBY  
                ) AS subquery  
                WHERE (cubbyID + 1) <= 500  
                AND (cubbyID + 1) NOT IN (SELECT cubbyID FROM cake.JEWELRY_CUBBY)  
            """)  
            result = cursor.fetchone()  
            cubbyID = result[0] if result[0] is not None else 1  # If all 1-500 are occupied, start at 1  
            print(f"Next available cubbyID: {cubbyID}")  
  
        except odbc.Error as ex:  
            print(f"Error determining cubbyID: {ex}")  
  
        finally:  
            cursor.close()  
            conn.close()  
  
    return cubbyID  # Return cubbyID  
  
def get_cubby(itemID, orderID, qty, sku, scannedBy, batch, dateTime, total_qty):  
    conn = get_connection()  
    cubbyID = None  # Initialize cubbyID  
  
    if conn:  
        try:  
            cursor = conn.cursor()  
            # Find cubbies that match the provided orderID  
            match_query = "SELECT * FROM cake.JEWELRY_CUBBY WHERE orderID = ?"  
            cursor.execute(match_query, (orderID,))  
            cubbies = cursor.fetchall()  
            if cubbies:  
                for cubby in cubbies:  
                    print(f"ItemID: {cubby[0]}, OrderID: {cubby[1]}, Qty: {cubby[2]}, SKU: {cubby[3]}, ScannedBy: {cubby[4]}, CubbyID: {cubby[5]}, OrderDate: {cubby[6]}, DateTime: {cubby[7]}, TotalQty: {cubby[8]}")  
                    cubbyID = cubby[5]  
                # Add the new item information to the existing cubby  
                insert_query = '''  
                INSERT INTO cake.JEWELRY_CUBBY (itemID, orderID, qty, sku, scannedBy, cubbyID, orderDate, dateTime, total_qty)  
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  
                '''  
                cursor.execute(insert_query, (itemID, orderID, qty, sku, scannedBy, cubbyID, batch, dateTime, total_qty))  
                conn.commit()  
            if cubbyID is None:  
                print(f"No cubbies found for orderID: {orderID}")  
                cubbyID = create_cubby()  
                # Insert the new cubby into the table  
                insert_query = '''  
                INSERT INTO cake.JEWELRY_CUBBY (itemID, orderID, qty, sku, scannedBy, cubbyID, orderDate, dateTime, total_qty)  
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  
                '''  
                cursor.execute(insert_query, (itemID, orderID, qty, sku, scannedBy, cubbyID, batch, dateTime, total_qty))  
                conn.commit()  
        except odbc.Error as ex:  
            print(f"Error finding cubby: {ex}")  
        finally:  
            cursor.close()  
            conn.close()  
  
    return cubbyID 

def delete_cubby(cubbyID):  
    conn = get_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()
            update_query = "UPDATE cake.JEWELRY_STATUS SET cubby = 0 WHERE cubby = ?"  
            cursor.execute(update_query, (cubbyID,))  
            conn.commit()  
            print(f"CubbyID {cubbyID} set to 0 in JEWELRY_STATUS.")   
            # Delete the cubby with the specified cubbyID  
            delete_query = "DELETE FROM cake.JEWELRY_CUBBY WHERE cubbyID = ?"  
            cursor.execute(delete_query, (cubbyID,))  
            conn.commit()  
            if cursor.rowcount > 0:  
                print(f"Cubby with cubbyID {cubbyID} deleted successfully.")  
                return True  
            else:  
                print(f"No cubby found with cubbyID: {cubbyID}")  
                return False  
        except odbc.Error as ex:  
            print(f"Error deleting cubby: {ex}")  
            return False  
        finally:  
            cursor.close()  
            conn.close()

def search_cubby(search_term):  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        query = """  
            SELECT * FROM cake.JEWELRY_CUBBY  
            WHERE CAST(itemID AS nvarchar) = ? OR CAST(orderID AS nvarchar) = ? OR CAST(cubbyID AS nvarchar) = ?  
        """  
        cursor.execute(query, (search_term, search_term, search_term))  
        cubbies = cursor.fetchall()  
        if cubbies:  
            print(f"Cubbies found: {cubbies}")  # Log the cubbies found  
            cubby_list = []  
            for cubby in cubbies:  
                cubby_list.append({  
                    "itemID": cubby[0],  
                    "orderID": cubby[1],  
                    "qty": cubby[2],  
                    "sku": cubby[3],  
                    "scannedBy": cubby[4],  
                    "cubbyID": cubby[5],  
                    "orderDate": cubby[6],  
                    "dateTime": cubby[7].strftime('%Y-%m-%d %H:%M'),  
                    "total_qty": cubby[8]  
                })  
            return cubby_list  
        else:  
            print(f"No cubbies found for search term: {search_term}")  
            return []  
    except odbc.Error as ex:  
        print(f"Error searching cubbies: {ex}")  
        return []  
    finally:  
        if conn:  
            cursor.close()  
            conn.close()  
        print("Connection closed.")  
   
  
def init_cubby_routes(app):  
    @app.route('/insert_to_cubby', methods=['POST'])  
    def insert_to_cubby():  
        data = request.get_json()  
        print(f"Received data: {data}")  # Log received data  
        scanned_number = data.get('scanned_number')  
        signedInEmployeeName = data.get('signedInEmployeeName')  
        if not scanned_number:  
            return jsonify({'error': 'No line_id or custom_id provided'}), 400  
        conn = get_connection()  
        if not conn:  
            print("Database connection failed")  
            return jsonify({'error': 'Database connection failed'}), 500  
        try:  
            cursor = conn.cursor()  
            # Fetch data from JEWELRY_STATUS using the scanned number as itemID  
            query = """SELECT line_id, order_id, sku, qty, order_date, total_qty  
                    FROM cake.JEWELRY_STATUS 
                    WHERE line_id = ? OR custom_id = ?"""  
            cursor.execute(query, (scanned_number, scanned_number))  
            result = cursor.fetchone()  
            if result:  
                line_id, order_id, sku, qty, order_date, total_qty = result  
                # Use the scanned number as itemID  
                itemID = scanned_number  
                # Determine cubbyID using get_cubby logic  
                datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M')  
                cubbyID = get_cubby(itemID, order_id, qty, sku, signedInEmployeeName, order_date, datetime_now, total_qty)  
                if cubbyID is None:  
                    return jsonify({'error': 'Failed to create cubby'}), 500  
                # Update JEWELRY_STATUS with the new cubbyID  
                update_query = """UPDATE cake.JEWELRY_STATUS 
                                SET cubby = ?  
                                WHERE line_id = ?"""  
                cursor.execute(update_query, (cubbyID, line_id))  
                conn.commit()  
                print("Data transferred successfully")  # Log success  
                return jsonify({'message': 'Data transferred successfully', 'cubbyID': cubbyID})  
            else:  
                print("No matching record found in JEWELRY_STATUS")  
                return jsonify({'error': 'No matching record found in JEWELRY_STATUS'}), 404  
        except odbc.Error as ex:  
            print(f"Database query error: {ex}")  
            return jsonify({'error': 'Database query failed'}), 500  
        finally:  
            cursor.close()  
            conn.close()  
  
    @app.route('/get_custom_id/<item_id>', methods=['GET'])  
    def get_custom_id(item_id):  
        conn = get_connection()  
        if not conn:  
            return jsonify({'error': 'Database connection failed'}), 500  
        try:  
            cursor = conn.cursor()  
            query = """SELECT custom_id FROM cake.JEWELRY_STATUS WHERE line_id = ?"""  
            cursor.execute(query, (item_id,))  
            result = cursor.fetchone()  
            if result:  
                custom_id = result[0]  
                return jsonify({'custom_id': custom_id})  
            else:  
                return jsonify({'custom_id': None}), 404  
        except odbc.Error as ex:  
            print(f"Database query error: {ex}")  
            return jsonify({'error': 'Database query failed'}), 500  
        finally:  
            cursor.close()  
            conn.close()  
  
    @app.route('/get_cubbies', methods=['GET'])  
    def get_cubbies():  
        cubbies = get_all_cubbies()  
        return jsonify(cubbies)  
  
    @app.route('/delete_cubby/<int:cubbyID>', methods=['DELETE'])  
    def delete_cubby_route(cubbyID):  
        success = delete_cubby(cubbyID)  
        if success:  
            return jsonify({'message': 'Cubby deleted successfully'}), 200  
        else:  
            return jsonify({'error': 'Failed to delete cubby'}), 500  
        
    @app.route('/search_item', methods=['GET'])  
    def search_item():  
        search_term = request.args.get('search_term')  
        print(f"Search term received: {search_term}") 
        if not search_term:  
            return jsonify({'error': 'No search term provided'}), 400  

        cubbies = search_cubby(search_term)  
        if cubbies:  
            print(f"Search results: {cubbies}") 
            return jsonify(cubbies)  
        else:  
            print(f"No matching records found for search term: {search_term}")  
            return jsonify({'error': 'No matching records found'}), 404  