import requests
import json
from datetime import date, datetime
from flask import  jsonify,  request
API_KEY = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJTQV9BUEkiLCJqa3UiOiJodHRwczovL2FwcC5za3VsYWJzLmNvbS9zL2FwaS9vYXV0aC9qd2tzIn0.eyJpc3MiOiJodHRwczovL2FwcC5za3VsYWJzLmNvbS9zL2FwaS9vYXV0aCIsInN1YiI6IjY2YzRhMmY1OWU5YWE3ZDNmNTc1NmE2MSIsImFjY291bnRfaWQiOiI2NjI5NzlmYmRiN2NkMTRkMjA5OTI1NjciLCJzZWVkIjoiSFF3QXJvdTUwZDB5LS1aT2JaZWU4dyIsImF1ZCI6Imh0dHBzOi8vYXBwLnNrdWxhYnMuY29tL3MvYXBpL29hdXRoIiwic2NvcGVzIjpbInByb2ZpbGUiLCJlbWFpbCIsInBob25lIiwicGxhdGZvcm1PcGVuIiwicGxhdGZvcm1HZW5lcmljIiwicGxhdGZvcm1BcGkiLCJ1c2VyU3RhbmRhcmQiLCJ1c2VyTWFuYWdlciIsInVzZXJBZG1pbiIsImV2ZXJ5b25lIl0sImF1dGhfdGltZSI6MTcyOTAyMjk1NiwiaWF0IjoxNzI5MDIyOTU2LCJqdGkiOiI2NzBlY2JlYzNkYmE2YmMzYWQzYjVlNGUifQ.DyCpSPtdl8FJgUkrvgii4hmUqQHvP8DJh3v8pRLu9QVH7YH3TTmlribAl1ld5SH_IuwC-DwaYsTSmNUkoINrSdFLwZ_leQKGxguwVIq5NJ8sCe37WEdOt5s37ZjzGsN8gzIAqgRbp9qQFl6Iud5zgdw24rijQViUZSBbyoU4v54jK1k4uG2_DC0SbSOBwdChPF3-xQoSR6T36Imxf3TSOKtlTzM69tZcjbcChvTseSV6Nswig57I_1GjBFHu3c2HHThNacT2OvnsfkmlTbh5ej02gga-nJQ7vIM0fk-c3WRfVVielsPMTG8dkkfNo7zc07MIuPk-Oxg3eco9FvdfMw"
STORE_ID = "66578a3a08851e1cf8e5cfcb"


def init_api_routes(app): 

    @app.route('/api/sku-labs-batching', methods=['POST'])  
    def api_sku_labs_batching():  
        order_number = request.json.get("orderNumber")  
        if not order_number:  
            return jsonify({'error': 'order_number is required'}), 400  
        
        result = sku_labs_batching(order_number)  
        print(result)
        return jsonify({'message': result})   
    
def list_to_dict(lst):
    output_dict = {}
    for item in lst:
        # Split at the first colon only (maxsplit=1)
        key, value = item.split(":", 1)
        # Strip leading/trailing whitespace from key and value
        output_dict[key.strip()] = value.strip()
    return output_dict

def order_status(order_number):
    url = "https://api.skulabs.com/order/status"
    querystring = {"store_id":STORE_ID,"order_number":order_number}
    headers = {"Authorization": API_KEY}
    response = requests.request("GET", url, headers=headers, params=querystring)
    output = json.loads(response.text)
    if "error" in output:
        message = output.get("error")
        status = "error"
        
    else:
        message = 'Status retrieved successfully'
        status = output.get("status")
    return message, status 

def order_get_single(line_id,orderNumber):
    url = "https://api.skulabs.com/order/get_single"
    querystring = {"order_number":orderNumber,"store_id":STORE_ID}
    headers = {"Authorization": API_KEY}
    response = requests.request("GET", url, headers=headers, params=querystring)
    order_data= json.loads(response.text)
    return order_data

def tag_get():  
    url = "https://api.skulabs.com/tag/get"  
    headers = {"Authorization": API_KEY}  
    response = requests.request("GET", url, headers=headers)  
  
    try:  
        tag_data = json.loads(response.text)  
    except json.JSONDecodeError:  
        print("Error: Failed to decode JSON response")  
        return []  
  
    if not isinstance(tag_data, list):  
        print(f"Error: tag_data is not a list, received: {tag_data}")  
        return []  
  
    return tag_data  
  
    ## TAGS to remember ##
    #ID: 663bcc2478eca5a71a28bb83 -> Name: Completeful
    #ID: 66cce4f15e4d61aa8169b0f6 -> Name: _madeondemand
    #ID: 66e0967e338fc5dc343cddff -> Name: CPLBatch: Tiny Stackable NR
    #ID: 668efa08a8b24a339be83932 -> Name: CPL-NonPersonalizedBatch

def order_get_tags(order_number):  
    url = "https://api.skulabs.com/order/get_single"  
    querystring = {"order_number": order_number, "store_id": STORE_ID}  
    headers = {"Authorization": API_KEY}  
    response = requests.request("GET", url, headers=headers, params=querystring)  
  
    try:  
        order_data = response.json()  
    except json.JSONDecodeError:  
        print(f"Error: Failed to decode JSON response for order {order_number}")  
        return {}  
  
    if 'order' not in order_data or not order_data['order']:  
        print(f"Error: 'order' key is missing or None in order_data for order {order_number}")  
        return {}  
  
    order = order_data.get('order')  
    id_list = order.get('tags', [])  
  
    dataset = tag_get()  
    if not isinstance(dataset, list):  
        print(f"Error: dataset is not a list for order {order_number}")  
        return {}  
  
    id_to_name_mapping = {item["_id"]: item["name"] for item in dataset if isinstance(item, dict)}  
  
    # Match IDs and get their names  
    matched_names = {id_: id_to_name_mapping.get(id_, "Not Found") for id_ in id_list}  
  
    return matched_names  
   

    # Print the matched names
    #for id_, name in matched_names.items():
        #print(f"ID: {id_} -> Name: {name}")
    #return order_data
## TAGS to remember ##
    #Step 1 Filter and make sure this tag exists
    #ID: 663bcc2478eca5a71a28bb83 -> Name: Completeful

    #Step 2 Segregate into one of these 2 tags
    #ID: 66cce4f15e4d61aa8169b0f6 -> Name: _madeondemand 
    #ID: 668efa08a8b24a339be83932 -> Name: CPL-NonPersonalizedBatch

    #Step 3 For items with _madeondemand take items with only one of these tags and put them individual batches
    #These items are engraved
    #Personalized can be used to seperated CPL batches even further
    #ID: 66578ef6045f7916672be10f -> Name: personalized
    #--------------------------------------------------------
    #ID: 66e0967e338fc5dc343cddff -> Name: CPLBatch: Tiny Stackable NR
    #ID: 66e0ac4c9199e868d1671202 -> Name: CPLBatch: Pillar Bar Necklace
    #ID: 66e0ac3f338fc5dc343d3a28 -> Name: CPLBatch: Inventory
    #ID: 66e0ac339199e868d16711aa -> Name: CPLBatch: Cuff Bracelet
    
    #These items are electroplated / require assembly
    #ID: 66e0ac29338fc5dc343d39b2 -> Name: CPLBatch: Name Ring
    #ID: 66e0ac1d9199e868d1671150 -> Name: CPLBatch: Name Necklace	
    #ID: 66e9e03592ec849f210d006b -> Name: CPLBatch: Letter Necklace
    #Step 4 For items with _madeondemand and multiple CPLBatch tags Batch as items with:
    #items with plated only
    #items with engrave only
    #items with plated and engraved 
    
    #Step 5 Batch items With _madeondemand and have inventory tag are a mix of madeondemand jewelry and 3PL
    #ID: 66e0ac3f338fc5dc343d3a28 -> Name: CPLBatch: Inventory


def sku_labs_batching(order_number, max_retries=5):  
    retry_count = 0  # Initialize the retry counter  
    while retry_count < max_retries:  
        tags = order_get_tags(order_number)  
        tags = tags.values()  
        CPLBatch_count = sum('CPLBatch' in value for value in tags)  
          
        # Log the tags for debugging 
        print()
        print()  
        print(f"Order {order_number} tags: {tags}")  
          
        if 'Completeful' in tags:  
            if '_madeondemand' in tags:  
                # if CPLBatch_count > 1:  
                #     print(f"Order {order_number} classified as Madetoorder (multiple CPLBatch tags)")  
                #     return 'Madetoorder'  
                # else:  
                #     print(f"Order {order_number} classified as Madetoorder (single CPLBatch tag or none)")  

                return 'Madetoorder'  
            else:

                print(f"Order {order_number} classified as 3PL order") 
                return '3PL order'
                  
        else: 

            print(f"Order {order_number} is not a completeful order, retrying")  
            retry_count += 1 
      
    # If the loop exits without finding 'Completeful' in tags  
    return 'not a completeful order skipping'  

# BCT
def bct_get_metadata(line_id, orderNumber):   
    data = order_get_single(line_id, orderNumber)  
  
    # Check if 'order' key exists in the response data  
    if 'order' not in data:  
        print(f"'order' key not found in the response data: {data}")  
        return {'error': "'order' key not found in the response data"}  
  
    try:  
        order = data['order']['stash']['items']  
    except KeyError as e:  
        print(f"KeyError accessing 'order' data: {e}, data: {data}")  
        return {'error': f"KeyError accessing 'order' data: {e}"}  
      
    for item in order:  
        line_item = item['line_id']  
        if line_item == int(line_id):  
            metadata = item['metadata'].replace('<br>', '')  
            metadata = metadata.replace('_cuff_fulfillment:', '')  
            metadata = metadata.split("\n")  
            result_dict = list_to_dict(metadata)  
            # print(result_dict)  
            outside_engraving = False  
            outside_engraving2 = False  
            inside_engraving = False  
            inside_engraving2 = False  
            outside_personalization = ""  
            outside_personalization2 = ""  
            inside_personalization = ""  
            inside_personalization2 = ""  
            try:  
                for key, value in result_dict.items():  
                    if 'Outside' in key:  
                        outside_engraving = True  
                        if 'OutsideTextLine1' in key:  
                            outside_personalization = value.replace('<br>', '')  
                            outside_personalization = outside_personalization.replace(' ', '')  
                            if outside_personalization == '':  
                                outside_engraving = False  
                        if 'OutsideTextLine2' in key:  
                            outside_engraving2 = True  
                            outside_personalization2 = value.replace('<br>', '')  
                            if outside_personalization2 == '':  
                                outside_engraving2 = False  
                        else:  
                            outside_personalization = value.replace('<br>', '')  
                            outside_personalization = outside_personalization.replace(' ', '')  
                            if outside_personalization == '':  
                                outside_engraving = False  
                    if 'Inside' in key:  
                        inside_engraving = True  
                        if 'InsideTextLine1' in key:  
                            inside_personalization = value.replace('<br>', '')  
                            inside_personalization = inside_personalization.replace(' ', '')  
                            if inside_personalization == '':  
                                inside_engraving = False  
                        if 'InsideTextLine2' in key:  
                            inside_engraving2 = True  
                            inside_personalization2 = value.replace('<br>', '')  
                            if inside_personalization2 == '':  
                                inside_engraving2 = False  
                        else:  
                            inside_personalization = value.replace('<br>', '')  
                            inside_personalization = inside_personalization.replace(' ', '')  
                            if inside_personalization == '':  
                                inside_engraving = False  
                if outside_engraving or outside_engraving2:  
                    print("Outside Inscription: ", outside_personalization or outside_personalization2)  
                if inside_engraving or inside_engraving2:  
                    print("Inside Inscription: ", inside_personalization or inside_personalization2)  
                # print('Success!-------------------------------------')  
                return {  
                    'outside_personalization': outside_personalization,  
                    'outside_personalization2': outside_personalization2,  
                    'inside_personalization': inside_personalization,  
                    'inside_personalization2': inside_personalization2  
                }  
            except Exception as e:  
                # print(metadata)  
                print(f"Order Failed {result_dict} due to error: {e}")  
                return {  
                    'outside_personalization': "",  
                    'outside_personalization2': "",  
                    'inside_personalization': "",  
                    'inside_personalization2': ""  
                }  
            
def sku_labs_order_getsingle(orderNumber):
    url = "https://api.skulabs.com/order/get_single"
    querystring = {"store_id": STORE_ID,"order_number":str(orderNumber)}
    headers = {"Authorization":API_KEY }
    response = requests.request("GET", url, headers=headers, params=querystring)
    
def pre_check_get_order_details(line_id, order_id):
    line_id = int(line_id)
    order_id = str(order_id)
    data = order_get_single(line_id,order_id)
    order = data['order']
    stash = data['order']['stash']
    items = data['order']['stash']['items']
    
    for item in items:
        #print(item)
        line_item = item['line_id']
        if line_item == int(line_id):
            item = item
            break
    
    qty = item['quantity']
    description = item['lineName']
    sku = item['lineSku']
    location = item_get_location_by_sku(sku)
    order_date = datetime.strptime(stash['date'], "%Y-%m-%dT%H:%M:%S.000Z").strftime("%Y-%m-%d")

    return line_id, order_id, sku, description, qty, order_date, location

# PICK&PACK 
def item_get_location_by_sku(sku):  
    url = "https://api.skulabs.com/item/get"  
    querystring = {"selector": f'{{"sku":"{sku}"}}'}  
    headers = {"Authorization": API_KEY}  
      
    try:  
        response = requests.request("GET", url, headers=headers, params=querystring)  
        response.raise_for_status()  # Raise an exception for HTTP errors  
        data = response.json()  
          
        # Check if the response contains the expected data  
        if data and isinstance(data, list) and len(data) > 0:  
            item = data[0]  
            if 'alias_locations' in item and item['alias_locations']:  
                location = list(item['alias_locations'].values())[0]  
                return location  
            else:  
                print(f"No alias_locations found for SKU: {sku}")  
                return "Location not found"  
        else:  
            print(f"No data found for SKU: {sku}")  
            return "Location not found"  
    except requests.exceptions.RequestException as e:  
        print(f"Error fetching location for SKU: {sku} - {e}")  
        return "Location not found"  

def sku_labs_update_status(orderNumber,status):
    url = "https://api.skulabs.com/order/modify_status"
    status_date = str(date.today())
    payload = {
        "store_id": STORE_ID,
        "order_number": str(orderNumber),
        "status": status,
        "status_date": status_date
    }
    headers = {"Authorization": API_KEY,
        "Content-Type": "application/json"}

    response = requests.request("PUT", url, json=payload, headers=headers)
    print(response.text)

def sku_labs_add_error_tag(orderNumber,Reason_string):
    url = "https://api.skulabs.com/order/add_tag_by_name"
    payload = {"orders": [{"order_number": orderNumber, "store_id": STORE_ID}],"tag_name": "CAKE_PROCESSING_ERROR","reason": Reason_string}
    headers = { "Authorization": API_KEY, "Content-Type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)

def sku_labs_add_tag(orderNumber,tag_name, Reason_string):
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
    payload = {"orders": [{"order_number": orderNumber, "store_id": STORE_ID}],"tag_name": tag_name,"reason": Reason_string}
    headers = { "Authorization": API_KEY, "Content-Type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response)
    message = response.text
    print(message)
    return message


def sku_labs_modify_status(orderNumber,STATUS_STRING):
    url = "https://api.skulabs.com/order/modify_status"
    payload = {"store_id": STORE_ID,"order_number": orderNumber,"status": STATUS_STRING, "status_date": "10-23-2024"}
    headers = {"Authorization": API_KEY, "Content-Type": "application/json"}
    response = requests.request("PUT", url, json=payload, headers=headers)
    print(response.text)

def get_shipping_info(order_id):
    url = "https://api.skulabs.com/order/get_single"
    querystring = {"order_number":order_id,"store_id":STORE_ID}
    headers = {"Authorization": API_KEY}
    response = requests.request("GET", url, headers=headers, params=querystring)
    order_data= json.loads(response.text)
    package_info = order_data['order']['stash']['items']
    #print(package_info)
    shipping_info = order_data['order']['stash']['shipping_information']
    #print(shipping_info)
    preview_dict = []
    order_dict = []
    order_qty = 0  
    for item in package_info:
        item_id = item.get('line_id')
        sku = item['lineSku']
        qty = item.get('quantity')
        
        order_qty = order_qty + int(qty)
        item_dict = [item_id,sku,qty]
        order_dict.append(item_dict)
        #print(item_dict)

    #print(order_qty)
    return shipping_info, order_qty, preview_dict, order_dict
