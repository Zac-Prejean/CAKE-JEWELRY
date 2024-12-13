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
def get_all():  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        query = "SELECT *  FROM cake.Scan_Tracking"  
        cursor.execute(query)  
        employees = cursor.fetchall()  
        if  employees:  
            employees_list = []  
            for item in  employees:  
                employees_list.append(item)
            return employees_list
        else:  
            print("No Employees found.")  
            return []  
    except odbc.Error as ex:  
        print(f"Error querying Tags: {ex}")  
        return []  
    finally:  
        if conn:  
            cursor.close()  
            conn.close()  
            print("Connection closed.")

def make_data_table():
    data = []
    scans = get_all()
    for item in scans:
        order_number, station_type, employee, scan_time = item
        data.append({ 'order_number': order_number, 'station_type': station_type, 'employee': employee, 'scan_time': scan_time })
    return data

def get_all_employees():  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        query = "SELECT DISTINCT employee FROM cake.Scan_Tracking"  
        cursor.execute(query)  
        employees = cursor.fetchall()  
        if  employees:  
            employees_list = []  
            for item in  employees:  
                employees_list.append(item)
            print(employees_list)
            return employees_list
        else:  
            print("No Employees found.")  
            return []  
    except odbc.Error as ex:  
        print(f"Error querying Tags: {ex}")  
        return []  
    finally:  
        if conn:  
            cursor.close()  
            conn.close()  
            print("Connection closed.")

def count_scan_by_employee(employee):  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        query = "SELECT COUNT(*) FROM cake.Scan_Tracking where employee = ?"  
        cursor.execute(query, (employee,))  
        dbcount = cursor.fetchall()  
        if  dbcount: 
            count = [row[0] for row in dbcount][0]
            
            #print(count)
            return count
        else:  
            count = 0
            return count 
        
    except odbc.Error as ex:  
        print(f"Error querying Tags: {ex}")  
        return []  
    finally:  
        if conn:  
            cursor.close()  
            conn.close()  
            #print("Connection closed.")

def station_by_employee(employee):  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        query = "SELECT station_type FROM cake.Scan_Tracking where employee = ?"  
        cursor.execute(query, (employee,))  
        dbcount = cursor.fetchall()  
        if  dbcount: 
            count = [row[0] for row in dbcount][0]
            
            #print(count)
            return count
        else:  
            count = 0
            return count 
        
    except odbc.Error as ex:  
        print(f"Error querying Tags: {ex}")  
        return []  
    finally:  
        if conn:  
            cursor.close()  
            conn.close()  
            #print("Connection closed.")

def add_scan(order_number, station_type, employee, scan_time):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Check if the order has already been scanned by the same employee at the same station
        match_query = '''
            SELECT COUNT(*)
            FROM cake.Scan_Tracking
            WHERE order_number = ? AND station_type = ? AND employee = ?
        '''
        cursor.execute(match_query, (order_number, station_type, employee))
        result = cursor.fetchone()

        if result[0] > 0:
            print(f"Order {order_number} has already been scanned by {employee} at {station_type}. Skipping insertion.")
        else:
            # Insert data into the table
            insert_data_query = '''
                INSERT INTO cake.Scan_Tracking (order_number, station_type, employee, scan_time)
                VALUES (?, ?, ?, ?)
            '''
            cursor.execute(insert_data_query, (order_number, station_type, employee, scan_time))
            connection.commit()
            print(f"Data inserted successfully for order {order_number} by {employee} at {station_type}.")

    except odbc.Error as ex:
        print("ERROR: COULD NOT ENTER", employee)

    finally:
        # Close the connection
        if connection:
            cursor.close()
            connection.close()

def calculate_average_scan_time(employee):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # SQL query to fetch rows for the current date only
        match_query = """
            SELECT * 
            FROM cake.Scan_Tracking 
            WHERE employee = ? AND CAST(scan_time AS DATE) = CAST(GETDATE() AS DATE)
        """
        cursor.execute(match_query, (employee,))
        speed_check = cursor.fetchall()

        # Process the fetched rows
        times = []
        for item in speed_check:
            order_number, station_type, employee, scan_time = item
            times.append(item)

        # Extract the datetime objects
        timestamps = [row[3] for row in times]

        # Calculate the differences between consecutive timestamps
        time_differences = [
            (timestamps[i + 1] - timestamps[i]).total_seconds()
            for i in range(len(timestamps) - 1)
        ]

        # Calculate the average time difference
        if time_differences:
            average_time = sum(time_differences) / len(time_differences)
        else:
            average_time = 0

        return average_time

    except odbc.Error as ex:
        print("ERROR: Could not calculate for employee:", employee, ex)

    finally:
        # Close the connection
        if connection:
            cursor.close()
            connection.close()
            
def make_leaderboard_entry(employee):
    station = station_by_employee(employee)
    scan_count = count_scan_by_employee(employee)
    average_time = calculate_average_scan_time(employee)
    return {'Employee':employee, 'Station':station,'Total_Scans':  scan_count,'Average_Time':average_time}
    
def getleaderboard(push):
    push = push
    employees = get_all_employees()
    leaderboard = []
    for employee in employees:
        #print(employee)
        employee = employee[0]
        leaderboard_entry = make_leaderboard_entry(employee)
        leaderboard.append(leaderboard_entry)
    #print(leaderboard)
    return leaderboard

#add_scan(451651945, 'Laser Station', 'Joe', datetime.now())