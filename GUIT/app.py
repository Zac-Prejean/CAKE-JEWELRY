# app.py

import requests
import json
from config import *
from designer import export_images
from PIL import Image, ImageDraw, ImageFont
from designer import export_images as export_images_ml  
from nonML_designer import export_images as export_images_non_ml
from tally import get_all 
from redo import init_redo_routes
from api_sku_labs import init_api_routes
from tally import get_all, get_today_started_total, get_today_ended_total
  
app = Flask(__name__)  

init_status_routes(app)
init_redo_routes(app)

# HOME   
@app.route('/')    
def home():    
    return render_template('home.html')  

# ADMIN 
@app.route('/admin')  
def admin():  
    try:  
        data = get_all_status()  
        print(f"Passing {len(data)} items to the template.")  
        return render_template('admin.html', data=data)  
    except Exception as e:  
        print(f"Error: {e}")  
        return render_template('admin.html', error=str(e)) 
init_admin_routes(app)

# CUBBYSYSTEM
@app.route('/cubbySystem')  
def cubbysystem():    
    return render_template('cubbySystem.html')
  
# TALLYPAGE   
@app.route('/tallyPage')  
def tallyPage():  
    tally_data = get_all()  
    total_started_today = get_today_started_total()  
    total_ended_today = get_today_ended_total()
    return render_template('tallyPage.html', tally_data=tally_data, total_started_today=total_started_today, total_ended_today=total_ended_today)  
 
# PRECHECK
@app.route('/precheck')  
def precheck():  
    return render_template('precheck.html')
init_precheck_routes(app)    
    
# DESIGNER
def export_images(df, full_folder_path, use_non_ml):  
    if use_non_ml:  
        return export_images_non_ml(df, full_folder_path)  
    else:  
        return export_images_ml(df, full_folder_path)  
    
@app.route('/designer')    
def designer():    
    return render_template('designer.html')

@app.route('/run-script', methods=['POST'])  
def run_script():  
    csv_file = request.files.get('csv_file')  
    folder_path = request.form.get('folderPath', 'default_folder_path')  
    use_non_ml = 'folderOrganizationCheckbox' in request.form  
  
    if csv_file:  
        decoded_csv = csv_file.read().decode('utf-8')  
        if not decoded_csv.strip():  
            return jsonify({"error": "Empty CSV file provided"}), 400  
        df = pd.read_csv(io.StringIO(decoded_csv))  
        print(f"CSV loaded with {len(df)} rows")  
    else:  
        return jsonify({"error": "CSV file not provided"}), 400  
  
    # Corrected processing function call  
    result = export_images(df, full_folder_path=folder_path, use_non_ml=use_non_ml)  
    return jsonify(result)

# TEMPLATEMERGER    
@app.route('/templateMerger')    
def templatemerger():    
    return render_template('templateMerger.html')

# REDOPAGE
@app.route('/redo')    
def redo():    
    return render_template('redo.html')   
init_api_routes(app)

# SCAN-IN STATION
@app.route('/scanIn')      
def scanIn(): 
    return render_template('scanIn.html')  

# PRINT STATION
@app.route('/printStation')    
def printStation():    
    return render_template('printStation.html') 

# SCAN-OUT STATION
@app.route('/scanOut')
def scanOut():    
    return render_template('scanOut.html') 
init_cubby_routes(app)  

# SHIP-OUT STATION
@app.route('/shipOut')    
def shipOut():    
    return render_template('shipOut.html')   
   
if __name__ == '__main__':    
    print("Running Print Layout Lab application... at http://127.0.0.1:5000")    
    app.run(debug=True)