# status.py


from config import *
import pyodbc 
from JEWELRY_STATUS_DB import get_order_by_tag

# Define connection parameters  
server = 'completefulserver.database.windows.net,1433'  
database = 'MainDatabase'  
username = 'JoeF'  
password = 'SEg4FFFoQUP*5Fi**rD#kh3'  
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'  
  
API_KEY = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJTQV9BUEkiLCJqa3UiOiJodHRwczovL2FwcC5za3VsYWJzLmNvbS9zL2FwaS9vYXV0aC9qd2tzIn0.eyJpc3MiOiJodHRwczovL2FwcC5za3VsYWJzLmNvbS9zL2FwaS9vYXV0aCIsInN1YiI6IjY2YzRhMmY1OWU5YWE3ZDNmNTc1NmE2MSIsImFjY291bnRfaWQiOiI2NjI5NzlmYmRiN2NkMTRkMjA5OTI1NjciLCJzZWVkIjoiSFF3QXJvdTUwZDB5LS1aT2JaZWU4dyIsImF1ZCI6Imh0dHBzOi8vYXBwLnNrdWxhYnMuY29tL3MvYXBpL29hdXRoIiwic2NvcGVzIjpbInByb2ZpbGUiLCJlbWFpbCIsInBob25lIiwicGxhdGZvcm1PcGVuIiwicGxhdGZvcm1HZW5lcmljIiwicGxhdGZvcm1BcGkiLCJ1c2VyU3RhbmRhcmQiLCJ1c2VyTWFuYWdlciIsInVzZXJBZG1pbiIsImV2ZXJ5b25lIl0sImF1dGhfdGltZSI6MTcyOTAyMjk1NiwiaWF0IjoxNzI5MDIyOTU2LCJqdGkiOiI2NzBlY2JlYzNkYmE2YmMzYWQzYjVlNGUifQ.DyCpSPtdl8FJgUkrvgii4hmUqQHvP8DJh3v8pRLu9QVH7YH3TTmlribAl1ld5SH_IuwC-DwaYsTSmNUkoINrSdFLwZ_leQKGxguwVIq5NJ8sCe37WEdOt5s37ZjzGsN8gzIAqgRbp9qQFl6Iud5zgdw24rijQViUZSBbyoU4v54jK1k4uG2_DC0SbSOBwdChPF3-xQoSR6T36Imxf3TSOKtlTzM69tZcjbcChvTseSV6Nswig57I_1GjBFHu3c2HHThNacT2OvnsfkmlTbh5ej02gga-nJQ7vIM0fk-c3WRfVVielsPMTG8dkkfNo7zc07MIuPk-Oxg3eco9FvdfMw"  
STORE_ID = "66578a3a08851e1cf8e5cfcb"  

def add_status(row, customtagID):  
    line_id = int(row['Line - ID'])
    order_id = str(row['Order - Number'])  
    qty = row['Item - Qty']  
    sku = row['Item - SKU']  
    description = row['Item - Options']  
    order_date = row['Order - Date']  
    scannedby = '-'  
    datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M')  
    cubby = ''  
    total_qty = row['Total Order Qty']  
  
    # Determine the value for custom_id based on SKU  
    if sku.startswith("NCK") or sku.startswith("RNG"):  
        custom_id_value = '-'  
    else:  
        custom_id_value = customtagID  
  
    print(f"Custom ID: {custom_id_value}")  
  
    # Establish a connection to the SQL Server  
    conn = get_connection()  
    cursor = conn.cursor()  
  
    try:  
        # Check if the line_id already exists in the database  
        check_query = "SELECT COUNT(*) FROM cake.JEWELRY_STATUS WHERE line_id = ?"  
        cursor.execute(check_query, (line_id,))  
        count = cursor.fetchone()[0]  
  
        if count > 0:  
            print(f"Skipping lineID {line_id} as it already exists.")  
            return  
  
        insert_query = '''  
        INSERT INTO cake.JEWELRY_STATUS (line_id, order_id, sku, description, qty, status, cubby, order_date, scannedby, [datetime], custom_id, total_qty)  
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  
        '''  
        query_params = (line_id, order_id, sku, description, qty, 'Batched', cubby, order_date, scannedby, datetime_now, custom_id_value, total_qty)  
  
        cursor.execute(insert_query, query_params)  
        conn.commit()  
        print("Data inserted successfully.")  
    except Exception as e:  
        print(f"Error inserting data: {e}")  
    finally:  
        cursor.close()  
        conn.close()  


def add_status_combined(items, combined_qty, customtagID, line_id_combined="-"):  
    if items:  
        row = items[0][1]  
        line_id = int(row['Line - ID'])   
        order_id = str(row['Order - Number'])  
        sku = row['Item - SKU']  
        description = row['Item - Options']  
        order_date = row['Order - Date']  
        scannedby = '-'  
        datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M')  
        cubby = ''  
        total_qty = row['Total Order Qty']  
  
        custom_id_value = customtagID  
  
        print(f"Custom ID: {custom_id_value}")  
  
        # Establish a connection to the SQL Server  
        conn = get_connection()  
        cursor = conn.cursor()  
  
        try:  
            # Check if the line_id already exists in the database  
            check_query = "SELECT COUNT(*) FROM cake.JEWELRY_STATUS WHERE line_id = ?"  
            cursor.execute(check_query, (line_id,))  
            count = cursor.fetchone()[0]  
  
            if count > 0:  
                print(f"Skipping lineID {line_id} as it already exists.")  
                return  
  
            insert_query = '''  
            INSERT INTO cake.JEWELRY_STATUS (line_id, order_id, sku, description, qty, status, cubby, order_date, scannedby, [datetime], custom_id, total_qty)  
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  
            '''  
            query_params = (line_id, order_id, sku, description, combined_qty, 'Batched', cubby, order_date, scannedby, datetime_now, custom_id_value, total_qty)  
  
            cursor.execute(insert_query, query_params)  
            conn.commit()  
            print("Data inserted successfully.")  
        except Exception as e:  
            print(f"Error inserting data: {e}")  
        finally:  
            cursor.close()  
            conn.close()  
     
   
def get_connection():  
    try:  
        conn = odbc.connect(connection_string)  
        return conn  
    except odbc.Error as ex:  
        print(f"Connection error: {ex}")  
        return None  
  
def sku_labs_update_status(orderNumber, status):  
    url = "https://api.skulabs.com/order/modify_status"  
    status_date = str(date.today())  
    payload = {  
        "store_id": STORE_ID,  
        "order_number": str(orderNumber),  
        "status": status,  
        "status_date": status_date  
    }  
    headers = {"Authorization": API_KEY, "Content-Type": "application/json"}  
    response = requests.request("PUT", url, json=payload, headers=headers)  
    print(response.text)  
  
def sku_labs_add_error_tag(orderNumber, Reason_string):  
    url = "https://api.skulabs.com/order/add_tag_by_name"  
    payload = {"orders": [{"order_number": orderNumber, "store_id": STORE_ID}], "tag_name": "CAKE_PROCESSING_ERROR", "reason": Reason_string}  
    headers = {"Authorization": API_KEY, "Content-Type": "application/json"}  
    response = requests.request("POST", url, json=payload, headers=headers)  
    print(response.text)  
  
def sku_labs_add_tag(orderNumber, tag_name, Reason_string):  
    '''  
    Defined tags:  
        Exported  
        C_Designed  
        C_Scanned in  
        C_Electro  
        C_Engraved  
        C_Assembly  
        C_Scan out  
        C_Reprocess  
    '''  
    url = "https://api.skulabs.com/order/add_tag_by_name"  
    payload = {"orders": [{"order_number": orderNumber, "store_id": STORE_ID}], "tag_name": tag_name, "reason": Reason_string}  
    headers = {"Authorization": API_KEY, "Content-Type": "application/json"}  
    response = requests.request("POST", url, json=payload, headers=headers)  
    message = response.text  
    return message  
  
def sku_labs_modify_status(orderNumber, STATUS_STRING):  
    url = "https://api.skulabs.com/order/modify_status"  
    payload = {"store_id": STORE_ID, "order_number": orderNumber, "status": STATUS_STRING, "status_date": "10-23-2024"}  
    headers = {"Authorization": API_KEY, "Content-Type": "application/json"}  
    response = requests.request("PUT", url, json=payload, headers=headers)  
    print(response.text)

def init_status_routes(app):  
    @app.route('/scan/<station>', methods=['POST'])  
    def scan(station):  
        data = request.get_json()  
        line_id = data.get('line_id')  
        custom_id = data.get('custom_id')  
        signedInEmployeeName = data.get('signedInEmployeeName').strip() 
        cubbyID = data.get('cubbyID')  
    
        # Provide a default integer value for cubbyID if it's None  
        if cubbyID is None:  
            cubbyID = 0  
    
        conn = get_connection()  
        if not conn:  
            return jsonify({'error': 'Database connection failed'}), 500  
    
        try:  
            cursor = conn.cursor()  
            if line_id:  
                query = """SELECT line_id, order_id, sku, description, qty, status, cubby, order_date, scannedby, [datetime], custom_id, total_qty  
                        FROM cake.JEWELRY_STATUS WHERE line_id = ?"""  
                cursor.execute(query, (line_id.replace('.0', ''),))  
            elif custom_id:  
                query = """SELECT line_id, order_id, sku, description, qty, status, cubby, order_date, scannedby, [datetime], custom_id, total_qty  
                        FROM cake.JEWELRY_STATUS WHERE custom_id = ?"""  
                cursor.execute(query, (custom_id,))  
            else:  
                return jsonify({'error': 'No line_id or custom_id provided'}), 400  
    
            result = cursor.fetchone()  
            if result:  
                current_status = result[5]  
                reason_string = 'SCAN STATION'  
                total_qty = result[11]  
    
                if station == 'scanIn':  
                    expected_status = 'Batched'  
                    new_status = 'Scanned-In'  
                    tag = 'C_Scanned in'  
                elif station == 'printStation':  
                    expected_status = 'Scanned-In'  
                    new_status = 'Printed'  
                    tag = 'C_Assembly'  
                elif station == 'scanOut':  
                    if total_qty > 1:  
                        expected_status = 'Printed'  
                        new_status = 'Cubby'  
                        tag = 'C_Scan out'  
                    else:  
                        expected_status = 'Printed'  
                        new_status = 'Scanned-Out'  
                        tag = 'C_Scan out'  
                else:  
                    return jsonify({'error': 'Invalid station type'}), 400  
    
                if current_status != expected_status:  
                    # Show warning modal  
                    return jsonify({  
                        'error': f'Item is not in the {expected_status} stage',  
                        'status': current_status,  
                        'message': f"This item has processed the {current_status} stage. Check with supervisor."  
                    }), 400  
    
                # Update only the specific line_id  
                update_query = """UPDATE cake.JEWELRY_STATUS SET status = ?, [datetime] = ?, scannedby = ?, cubby = ? WHERE line_id = ?"""  
                datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M')  
                datetime_date = datetime.now().strftime('%Y-%m-%d')  
                cursor.execute(update_query, (new_status, datetime_now, signedInEmployeeName, cubbyID, result[0]))  
                conn.commit()  
    
                # Add tag only to the specific order_id  
                order_id = result[1]  
                sku_labs_add_tag(order_id, tag, str(reason_string))  
    
                # Update or insert sandedCheck, daysTotal, and startedCheck for the SCANIN stage  
                sku = result[2]  
                if station == 'scanIn':  
                    if sku.startswith('NCK') or sku.startswith('RNG'):  
                        cursor.execute("SELECT sandedCheck, daysTotal, startedCheck FROM cake.JEWELRY_TALLY WHERE employeeName = ? AND orderDate = ?", (signedInEmployeeName, datetime_date))  
                        updated_value = cursor.fetchone()  
                        if updated_value:  
                            update_tally_query = """UPDATE cake.JEWELRY_TALLY  
                                                SET sandedCheck = COALESCE(sandedCheck, 0) + 1,  
                                                    daysTotal = COALESCE(daysTotal, 0) + 1,  
                                                    startedCheck = COALESCE(startedCheck, 0) + 1  
                                                WHERE employeeName = ? AND orderDate = ?"""  
                            cursor.execute(update_tally_query, (signedInEmployeeName, datetime_date))  
                        else:  
                            insert_tally_query = """INSERT INTO cake.JEWELRY_TALLY (employeeName, orderDate, sandedCheck, daysTotal, startedCheck)  
                                                VALUES (?, ?, 1, 1, 1)"""  
                            cursor.execute(insert_tally_query, (signedInEmployeeName, datetime_date))  
                            print(f"New record created for employee: {signedInEmployeeName} on date: {datetime_date}")  
                    elif sku.startswith('SRN') or sku.startswith('BNCK') or sku.startswith('BCT') or sku.startswith('RWTF') or sku.startswith('DLTH'):  
                        cursor.execute("SELECT startedCheck FROM cake.JEWELRY_TALLY WHERE employeeName = ? AND orderDate = ?", (signedInEmployeeName, datetime_date))  
                        updated_value = cursor.fetchone()  
                        if updated_value:  
                            update_tally_query = """UPDATE cake.JEWELRY_TALLY  
                                                SET startedCheck = COALESCE(startedCheck, 0) + 1  
                                                WHERE employeeName = ? AND orderDate = ?"""  
                            cursor.execute(update_tally_query, (signedInEmployeeName, datetime_date))  
                            print(f"startedCheck updated for employee: {signedInEmployeeName} on date: {datetime_date}")  
                        else:  
                            insert_tally_query = """INSERT INTO cake.JEWELRY_TALLY (employeeName, orderDate, startedCheck)  
                                                VALUES (?, ?, 1)"""  
                            cursor.execute(insert_tally_query, (signedInEmployeeName, datetime_date))  
                            print(f"New record created for employee: {signedInEmployeeName} on date: {datetime_date}")  
                    else:  
                        print(f"SKU {sku} not recognized for this tally update. No tally update performed")   
    
                    conn.commit()  
    
                # Update or insert qcCheck, and daysTotal for the PRINTED stage 
                if station == 'printStation':  
                    if sku.startswith('NCK') or sku.startswith('RNG'):  
                        cursor.execute("SELECT qcCheck, daysTotal FROM cake.JEWELRY_TALLY WHERE employeeName = ? AND orderDate = ?", (signedInEmployeeName, datetime_date))  
                        updated_value = cursor.fetchone()  
                        if updated_value:  
                            update_tally_query = """UPDATE cake.JEWELRY_TALLY  
                                                SET qcCheck = COALESCE(qcCheck, 0) + 1,  
                                                    daysTotal = COALESCE(daysTotal, 0) + 1 
                                                WHERE employeeName = ? AND orderDate = ?"""  
                            cursor.execute(update_tally_query, (signedInEmployeeName, datetime_date))  
                        else:  
                            insert_tally_query = """INSERT INTO cake.JEWELRY_TALLY (employeeName, orderDate, qcCheck, daysTotal)  
                                                VALUES (?, ?, 1, 1)"""  
                            cursor.execute(insert_tally_query, (signedInEmployeeName, datetime_date))  
                            print(f"New record created for employee: {signedInEmployeeName} on date: {datetime_date}") 
                    else:  
                        print(f"SKU {sku} not recognized for this tally update. No tally update performed")   
    
                    conn.commit()  

                # Update or insert engravedCheck, hookedCheck, sizedCheck, daysTotal, and endedCheck for the SCANOUT stage 
                if station == 'scanOut':  
                    if sku.startswith('NCK'):  
                        cursor.execute("SELECT hookedCheck, daysTotal, endedCheck FROM cake.JEWELRY_TALLY WHERE employeeName = ? AND orderDate = ?", (signedInEmployeeName, datetime_date))  
                        updated_value = cursor.fetchone()  
                        
                        hooked_increment = 1  
                        total_increment = 1  
                        if sku.startswith("NCK02"):  
                            hooked_increment = 2  
                            total_increment = 2  
                        elif sku.startswith("NCK03"):  
                            hooked_increment = 3  
                            total_increment = 3  
                        elif sku.startswith("NCK04"):  
                            hooked_increment = 4  
                            total_increment = 4  
                        elif sku.startswith("NCKCLT"):  
                            hooked_increment = 5  
                            total_increment = 5  
                        
                        if updated_value:  
                            update_tally_query = """UPDATE cake.JEWELRY_TALLY  
                                                    SET hookedCheck = COALESCE(hookedCheck, 0) + ?,   
                                                        daysTotal = COALESCE(daysTotal, 0) + ?,   
                                                        endedCheck = COALESCE(endedCheck, 0) + 1  
                                                    WHERE employeeName = ? AND orderDate = ?"""  
                            cursor.execute(update_tally_query, (hooked_increment, total_increment, signedInEmployeeName, datetime_date))  
                        else:  
                            insert_tally_query = """INSERT INTO cake.JEWELRY_TALLY (employeeName, orderDate, hookedCheck, daysTotal, endedCheck)  
                                                    VALUES (?, ?, ?, ?, 1)"""  
                            cursor.execute(insert_tally_query, (signedInEmployeeName, datetime_date, hooked_increment, total_increment))  
                            print(f"New record created for employee: {signedInEmployeeName} on date: {datetime_date}")  
                
                    elif sku.startswith('RNG'):  
                        cursor.execute("SELECT sizedCheck, endedCheck FROM cake.JEWELRY_TALLY WHERE employeeName = ? AND orderDate = ?", (signedInEmployeeName, datetime_date))  
                        updated_value = cursor.fetchone()  
                        
                        if updated_value:  
                            update_tally_query = """UPDATE cake.JEWELRY_TALLY  
                                                    SET sizedCheck = COALESCE(sizedCheck, 0) + 1, 
                                                        daysTotal = COALESCE(daysTotal, 0) + 1,  
                                                        endedCheck = COALESCE(endedCheck, 0) + 1  
                                                    WHERE employeeName = ? AND orderDate = ?"""  
                            cursor.execute(update_tally_query, (signedInEmployeeName, datetime_date))  
                        else:  
                            insert_tally_query = """INSERT INTO cake.JEWELRY_TALLY (employeeName, orderDate, sizedCheck, daysTotal, endedCheck)  
                                                    VALUES (?, ?, 1, 1, 1)"""  
                            cursor.execute(insert_tally_query, (signedInEmployeeName, datetime_date))  
                            print(f"New record created for employee: {signedInEmployeeName} on date: {datetime_date}")  
                    
                    elif sku.startswith('SRN') or sku.startswith('BNCK') or sku.startswith('BCT') or sku.startswith('RWTF') or sku.startswith('DLTH'):  
                        cursor.execute("SELECT engravedCheck, daysTotal, endedCheck FROM cake.JEWELRY_TALLY WHERE employeeName = ? AND orderDate = ?", (signedInEmployeeName, datetime_date))  
                        updated_value = cursor.fetchone()  
                        
                        if updated_value:  
                            update_tally_query = """UPDATE cake.JEWELRY_TALLY  
                                                    SET engravedCheck = COALESCE(engravedCheck, 0) + 1,   
                                                        daysTotal = COALESCE(daysTotal, 0) + 1,   
                                                        endedCheck = COALESCE(endedCheck, 0) + 1  
                                                    WHERE employeeName = ? AND orderDate = ?"""  
                            cursor.execute(update_tally_query, (signedInEmployeeName, datetime_date))  
                        else:  
                            insert_tally_query = """INSERT INTO cake.JEWELRY_TALLY (employeeName, orderDate, engravedCheck, daysTotal, endedCheck)  
                                                    VALUES (?, ?, 1, 1, 1)"""  
                            cursor.execute(insert_tally_query, (signedInEmployeeName, datetime_date))  
                            print(f"New record created for employee: {signedInEmployeeName} on date: {datetime_date}")  
                    
                    else:  
                        print(f"SKU {sku} not recognized for this tally update. No tally update performed")  
                    
                    conn.commit()  

    
                return jsonify({  
                    'message': 'Status updated successfully',  
                    'line_id': result[0],  
                    'order_id': result[1],  
                    'sku': result[2],  
                    'description': result[3],  
                    'qty': result[4],  
                    'status': new_status,  
                    'cubby': cubbyID,  
                    'order_date': result[7],  
                    'scannedby': signedInEmployeeName,  
                    'datetime': datetime_now,  
                    'custom_id': result[10],  
                    'total_qty': result[11]  
                })  
            else:  
                return jsonify({'error': 'No matching record found'}), 404  
        except pyodbc.Error as ex:  
            print(f"Database query error: {ex}")  
            return jsonify({'error': 'Database query failed'}), 500  
        finally:  
            cursor.close()  
            conn.close()    

    @app.route('/override_status', methods=['POST'])  
    def override_status():  
        data = request.get_json()  
        print("Override Request Data:", data)  
  
        line_id = data.get('line_id')  
        custom_id = data.get('custom_id')  
        signedInEmployeeName = data.get('signedInEmployeeName') 
        password = data.get('password')  
  
        # Check if the password is correct  
        if password != "your_admin_password":
            return jsonify({'error': 'Invalid password'}), 403  
  
        print(f"Querying for line_id: {line_id}, custom_id: {custom_id}")  
  
        conn = get_connection()  
        if not conn:  
            return jsonify({'error': 'Database connection failed'}), 500  
  
        try:  
            cursor = conn.cursor()  
            if line_id:  
                query = """SELECT line_id, order_id, sku, description, qty, status, cubby, order_date, scannedby, datetime, custom_id FROM cake.JEWELRY_STATUS WHERE line_id = ?"""  
                cursor.execute(query, (line_id.replace('.0', ''),))  
            elif custom_id:  
                query = """SELECT line_id, order_id, sku, description, qty, status, cubby, order_date, scannedby, datetime, custom_id FROM cake.JEWELRY_STATUS WHERE custom_id = ?"""  
                cursor.execute(query, (custom_id,))  
            else:  
                return jsonify({'error': 'No line_id or custom_id provided'}), 400  
  
            result = cursor.fetchone()  
            if result:  
                # Print all information retrieved from the database  
                print(f"Retrieved Data: Line ID: {result[0]}, Order ID: {result[1]}, SKU: {result[2]}, Description: {result[3]}, Qty: {result[4]}, Status: {result[5]}, Cubby: {result[6]}, Order Date: {result[7]}, Scanned By: {result[8]}, Datetime: {result[9]}, Custom ID: {result[10]}")  
  
                update_query = """UPDATE cake.JEWELRY_STATUS SET status = ?, datetime = ?, scannedby = ? WHERE line_id = ?"""  
                datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M')  
                new_status = 'Scanned-In'  
                cursor.execute(update_query, (new_status, datetime_now, signedInEmployeeName, result[0]))  
                conn.commit()  
  
                return jsonify({  
                    'message': 'Status updated successfully',  
                    'line_id': result[0],  
                    'order_id': result[1],  
                    'sku': result[2],  
                    'description': result[3],  
                    'qty': result[4],  
                    'status': new_status,  
                    'cubby': result[6],  
                    'order_date': result[7],  
                    'scannedby': signedInEmployeeName,  
                    'datetime': datetime_now,  
                    'custom_id': result[10],
                    'total_qty': result[11] 
                })  
            else:  
                return jsonify({'error': 'No matching record found'}), 404  
        except odbc.Error as ex:  
            print(f"Database query error: {ex}")  
            return jsonify({'error': 'Database query failed'}), 500  
        finally:  
            cursor.close()  
            conn.close()  

    @app.route('/update_status', methods=['POST'])  
    def update_status():  
        data = request.get_json()  
        print("Received data for update_status:", data) 
        line_id = data.get('line_id')  
        new_status = data.get('new_status')  
    
        if not line_id or not new_status:  
            return jsonify({'error': 'line_id and new_status are required'}), 400  
    
        conn = get_connection()  
        if not conn:  
            return jsonify({'error': 'Database connection failed'}), 500  
    
        try:  
            cursor = conn.cursor()  
            print("Attempting to update status for line_id:", line_id)
            update_query = """UPDATE cake.JEWELRY_STATUS SET status = ?, [datetime] = ? WHERE line_id = ?"""  
            datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M')  
            cursor.execute(update_query, (new_status, datetime_now, line_id))  
            conn.commit()  
            print("Status updated successfully for line_id:", line_id)
            return jsonify({'message': 'Status updated successfully', 'line_id': line_id, 'new_status': new_status})  
        except odbc.Error as ex:  
            print(f"Database query error: {ex}") 
            return jsonify({'error': 'Database query failed'}), 500  
        finally:  
            cursor.close()  
            conn.close()  

 