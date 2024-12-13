# tally.py


import pyodbc  
from datetime import date, datetime  
  
# Define connection parameters  
server = 'completefulserver.database.windows.net,1433'  
database = 'MainDatabase'  
username = 'JoeF'  
password = 'SEg4FFFoQUP*5Fi**rD#kh3'  
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'  
  
def get_connection():  
    try:  
        conn = pyodbc.connect(connection_string)  
        return conn  
    except pyodbc.Error as ex:  
        print(f"Connection error: {ex}")  
        return None  
  
def get_today_started_total():  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        today = date.today().strftime('%Y-%m-%d')  
        query = """  
            SELECT SUM(startedCheck) AS total_started  
            FROM cake.JEWELRY_TALLY  
            WHERE CAST(orderDate AS DATE) = ?  
        """  
        cursor.execute(query, today)  
        result = cursor.fetchone()  
        if result and result.total_started:  
            return result.total_started  
        else:  
            return 0  
    except pyodbc.Error as ex:  
        print(f"Error querying started total: {ex}")  
        return 0  
    finally:  
        if conn:  
            cursor.close()  
            conn.close()  
            print("Connection closed.")  
  
def get_today_ended_total():  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        today = date.today().strftime('%Y-%m-%d')  
        query = """  
            SELECT SUM(endedCheck) AS total_ended  
            FROM cake.JEWELRY_TALLY  
            WHERE CAST(orderDate AS DATE) = ?  
        """  
        cursor.execute(query, today)  
        result = cursor.fetchone()  
        if result and result.total_ended:  
            return result.total_ended  
        else:  
            return 0  
    except pyodbc.Error as ex:  
        print(f"Error querying ended total: {ex}")  
        return 0  
    finally:  
        if conn:  
            cursor.close()  
            conn.close()  
            print("Connection closed.")  
  
def get_all():  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        today = date.today().strftime('%Y-%m-%d')  
        query = """  
            SELECT *  
            FROM cake.JEWELRY_TALLY  
            WHERE CAST(orderDate AS DATE) = ?  
            ORDER BY daysTotal DESC  
        """  
        cursor.execute(query, today)  
        employees = cursor.fetchall()  
        if employees:  
            employees_list = []  
            for item in employees:  
                employees_list.append({  
                    "employeeName": item.employeeName,  
                    "orderDate": item.orderDate,  
                    "sandedCheck": item.sandedCheck,  
                    "engravedCheck": item.engravedCheck,  
                    "hookedCheck": item.hookedCheck,  
                    "sizedCheck": item.sizedCheck,  
                    "qcCheck": item.qcCheck,  
                    "shippedCheck": item.shippedCheck,  
                    "startedCheck": item.startedCheck,  
                    "endedCheck": item.endedCheck,  # Fixed this to use endedCheck  
                    "daysTotal": item.daysTotal  
                })  
            return employees_list  
        else:  
            print("No Employees found.")  
            return []  
    except pyodbc.Error as ex:  
        print(f"Error querying Tags: {ex}")  
        return []  
    finally:  
        if conn:  
            cursor.close()  
            conn.close()  
            print("Connection closed.")  


