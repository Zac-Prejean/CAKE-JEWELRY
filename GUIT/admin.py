# admin.py 

from config import *
  
# Define connection parameters  
server = 'completefulserver.database.windows.net,1433'  
database = 'MainDatabase'  
username = 'JoeF'  
password = 'SEg4FFFoQUP*5Fi**rD#kh3'  
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'  
  
# SQLAlchemy setup  
Base = declarative_base()  
engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server')  
Session = sessionmaker(bind=engine)  
  
# Define models if needed (Example for AdminUser)  
class Employee(Base):  
    __tablename__ = 'CAKE_EMPLOYEE'  
    id = Column(Integer, primary_key=True)  
    name = Column(String, nullable=False)  
    title = Column(String, nullable=False)  
    passcode = Column(String, nullable=False)  
    department = Column(String, nullable=False)  
    category = Column(String, nullable=False)  
    access = Column(Integer, nullable=False)  
  
def get_connection():  
    try:  
        conn = odbc.connect(connection_string)  
        return conn  
    except odbc.Error as ex:  
        print(f"Connection error: {ex}")  
        return None  
  
def get_all_status():  
    conn = get_connection()  
    try:  
        cursor = conn.cursor()  
        query = "SELECT * FROM cake.JEWELRY_STATUS"  
        cursor.execute(query)  
        tags = cursor.fetchall()  
        if tags:  
            tag_list = []  
            for tag in tags:  
                line_id, order_id, custom_id, sku, description, qty, status, cubby, order_date, scanned_in, printed, scanned_out, shipped, datetime, total_qty = tag  
                # Check if line_id contains multiple values  
                if ',' in str(line_id):  
                    line_id = "MULTI"  
                tag_list.append({  
                    "line_id": str(line_id),
                    "custom_id": custom_id,  
                    "order_id": str(order_id), 
                    "sku": sku,  
                    "description": description,  
                    "qty": qty,  
                    "status": status,  
                    "cubby": cubby,  
                    "order_date": order_date, 
                    "scanned_in": scanned_in,  
                    "printed": printed,  
                    "scanned_out": scanned_out,  
                    "shipped": shipped, 
                    "datetime": datetime,  
                    "total_qty": total_qty  
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
  
def init_admin_routes(app):  
    @app.route('/fetch_status', methods=['GET'])  
    def fetch_status():  
        try:  
            data = get_all_status()  
            return jsonify(data)  
        except Exception as e:  
            return jsonify({"error": str(e)}), 500  
  
    @app.route('/admin_update_status', methods=['POST'])  
    def admin_update_status():  
        line_id = request.form.get('line_id')  
        order_id = request.form.get('order_id')  
        new_status = request.form.get('status')  
    
        if not line_id or not order_id or not new_status:  
            return jsonify({"error": "Missing required parameters"}), 400  
    
        try:  
            conn = get_connection()  
            cursor = conn.cursor()  
    
            if line_id == "MULTI":  
                # Fetch all line_ids associated with the given order_id  
                query_fetch = """  
                SELECT line_id FROM cake.JEWELRY_STATUS WHERE order_id = ?  
                """  
                cursor.execute(query_fetch, (order_id,))  
                line_id_rows = cursor.fetchall()  
                line_id_list = [row[0] for row in line_id_rows]  
            else:  
                line_id_list = [line_id]  
    
            print(f"Processing line_ids: {line_id_list}")  
    
            # Update each line_id individually  
            for single_line_id in line_id_list:  
                print(f"Updating line_id: {single_line_id.strip()}")  
                query = """  
                UPDATE cake.JEWELRY_STATUS 
                SET status = ?, [datetime] = ?, scanned_in= ?, printed= ?, scanned_out = ?  
                WHERE line_id = ? AND order_id = ?  
                """  
                datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M')  
                scanned_in = 'Admin'  # Or fetch from session if user-specific  
                printed = 'Admin'
                scanned_out = 'Admin'
                cursor.execute(query, (new_status, datetime_now, scanned_in, printed, scanned_out, single_line_id.strip(), order_id))  
            
            conn.commit()  
            return jsonify({"message": "Status updated successfully"}), 200  
        except Exception as e:  
            print(f"Error updating status: {e}")  
            return jsonify({"error": str(e)}), 500  
        finally:  
            if cursor:  
                cursor.close()  
            if conn:  
                conn.close()  
  
    @app.route('/api/search', methods=['GET'])  
    def search():  
        # Get the query and date parameters  
        query = request.args.get('query', '').strip().lower()  
        date_query = request.args.get('date', '').strip().lower()  
    
        # Check if neither query nor date is provided  
        if not query and not date_query:  
            return jsonify({'error': 'Query or date is required'}), 400  
    
        conn = get_connection()  
    
        try:  
            cursor = conn.cursor()  
            if query:  
                query_string = """  
                    SELECT * FROM cake.JEWELRY_STATUS 
                    WHERE LOWER(CAST(line_id AS varchar(max))) LIKE ? OR  
                        LOWER(CAST(order_id AS varchar(max))) LIKE ? OR  
                        LOWER(CAST(custom_id AS varchar(max))) LIKE ? OR  
                        LOWER(CAST(sku AS varchar(max))) LIKE ? OR  
                        LOWER(CAST(status AS varchar(max))) LIKE ? OR  
                        LOWER(CAST(description AS varchar(max))) LIKE ?  
                """  
                search_query = f"%{query}%"  
                cursor.execute(query_string, (search_query, search_query, search_query, search_query, search_query, search_query))  
            elif date_query:  
                query_string = """  
                    SELECT * FROM cake.JEWELRY_STATUS 
                    WHERE CAST(order_date AS DATE) = ?  
                """  
                cursor.execute(query_string, (date_query,))  
    
            results = cursor.fetchall()  
            if results:  
                results_list = []  
                for row in results:  
                    line_id, order_id, custom_id, sku, description, qty, status, cubby, order_date, scanned_in, printed, scanned_out, shipped, datetime, total_qty = row  
                    results_list.append({  
                        "line_id": line_id,  
                        "custom_id": custom_id,  
                        "order_id": order_id,  
                        "sku": sku,  
                        "description": description,  
                        "qty": qty,  
                        "status": status,  
                        "cubby": cubby,  
                        "order_date": order_date,  
                        "scanned_in": scanned_in,  
                        "printed": printed,  
                        "scanned_out": scanned_out,  
                        "shipped": shipped,  
                        "datetime": datetime,  
                        "total_qty": total_qty  
                    })  
                return jsonify(results_list)  
            else:  
                return jsonify([])  
        except odbc.Error as ex:  
            print(f"Error querying database: {ex}")  
            return jsonify({"error": str(ex)}), 500  
        finally:  
            if conn:  
                cursor.close()  
                conn.close() 

    @app.route('/check_password', methods=['POST'])  
    def check_password():  
        password = request.json.get('password', '').strip()  
        session = Session()  
        try:  
            employee = session.execute(  
                text("SELECT * FROM cake.CAKE_EMPLOYEE WHERE passcode = :password"),  
                {'password': password}  
            ).fetchone()  
            if employee and employee.access in [1, 2]:  # Admin access levels  
                print("Password check successful")  
                return jsonify({"result": "success"})  
            else:  
                print("Password check failed")  
                return jsonify({"result": "failure"})  
        except Exception as e:  
            print(f"Error during password check: {e}")  
            return jsonify({"error": str(e)}), 500  
        finally:  
            session.close()  
  
    @app.route('/signin', methods=['POST'])  
    def signin():  
        employee_id = request.json.get('employeeID', '').strip()  
        session = Session()  
        try:  
            employee = session.execute(  
                text("SELECT * FROM cake.CAKE_EMPLOYEE WHERE passcode = :password"),  
                {'password': employee_id}  
            ).fetchone()  
            if employee:  
                print(f"User signed in: {employee.name}")  
                return jsonify({"result": "success", "employeeName": employee.name})  
            else:  
                print("Sign-in failed")  
                return jsonify({"result": "failure"})  
        except Exception as e:  
            print(f"Error during sign-in: {e}")  
            return jsonify({"error": str(e)}), 500  
        finally:  
            session.close()    
  
    @app.route('/delete_item', methods=['POST'])  
    def delete_item():  
        line_id = request.form.get('line_id')  
        order_id = request.form.get('order_id')  
  
        if not line_id or not order_id:  
            return jsonify({"error": "Missing required parameters"}), 400  
  
        try:  
            conn = get_connection()  
            cursor = conn.cursor()  
            query = "DELETE FROM cake.JEWELRY_STATUS WHERE line_id = ? AND order_id = ?"  
            cursor.execute(query, (line_id, order_id))  
            conn.commit()  
            return jsonify({"message": "Item deleted successfully"}), 200  
        except Exception as e:  
            print(f"Error deleting item: {e}")  
            return jsonify({"error": str(e)}), 500  
        finally:  
            if cursor:  
                cursor.close()  
            if conn:  
                conn.close()  
 
