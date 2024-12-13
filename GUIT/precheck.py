# precheck.py

import requests  
import json  
from flask import request, jsonify, render_template  
  
API_KEY = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJTQV9BUEkiLCJqa3UiOiJodHRwczovL2FwcC5za3VsYWJzLmNvbS9zL2FwaS9vYXV0aC9qd2tzIn0.eyJpc3MiOiJodHRwczovL2FwcC5za3VsYWJzLmNvbS9zL2FwaS9vYXV0aCIsInN1YiI6IjY2YzRhMmY1OWU5YWE3ZDNmNTc1NmE2MSIsImFjY291bnRfaWQiOiI2NjI5NzlmYmRiN2NkMTRkMjA5OTI1NjciLCJzZWVkIjoiSFF3QXJvdTUwZDB5LS1aT2JaZWU4dyIsImF1ZCI6Imh0dHBzOi8vYXBwLnNrdWxhYnMuY29tL3MvYXBpL29hdXRoIiwic2NvcGVzIjpbInByb2ZpbGUiLCJlbWFpbCIsInBob25lIiwicGxhdGZvcm1PcGVuIiwicGxhdGZvcm1HZW5lcmljIiwicGxhdGZvcm1BcGkiLCJ1c2VyU3RhbmRhcmQiLCJ1c2VyTWFuYWdlciIsInVzZXJBZG1pbiIsImV2ZXJ5b25lIl0sImF1dGhfdGltZSI6MTcyOTAyMjk1NiwiaWF0IjoxNzI5MDIyOTU2LCJqdGkiOiI2NzBlY2JlYzNkYmE2YmMzYWQzYjVlNGUifQ.DyCpSPtdl8FJgUkrvgii4hmUqQHvP8DJh3v8pRLu9QVH7YH3TTmlribAl1ld5SH_IuwC-DwaYsTSmNUkoINrSdFLwZ_leQKGxguwVIq5NJ8sCe37WEdOt5s37ZjzGsN8gzIAqgRbp9qQFl6Iud5zgdw24rijQViUZSBbyoU4v54jK1k4uG2_DC0SbSOBwdChPF3-xQoSR6T36Imxf3TSOKtlTzM69tZcjbcChvTseSV6Nswig57I_1GjBFHu3c2HHThNacT2OvnsfkmlTbh5ej02gga-nJQ7vIM0fk-c3WRfVVielsPMTG8dkkfNo7zc07MIuPk-Oxg3eco9FvdfMw"  
STORE_ID = "66578a3a08851e1cf8e5cfcb"  
  
def list_to_dict(lst):  
    output_dict = {}  
    for item in lst:  
        key, value = item.split(":", 1)  
        output_dict[key.strip()] = value.strip()  
    return output_dict  
  
def order_get_single(line_id, orderNumber):  
    url = "https://api.skulabs.com/order/get_single"  
    querystring = {"order_number": orderNumber, "store_id": STORE_ID}  
    headers = {"Authorization": API_KEY}  
    response = requests.request("GET", url, headers=headers, params=querystring)  
    order_data = json.loads(response.text)  
    return order_data  
  
def bct_get_metadata(line_id, orderNumber):  
    data = order_get_single(line_id, orderNumber)  
    order = data['order']['stash']['items']  
    for item in order:  
        line_item = item['line_id']  
        if line_item == int(line_id):  
            metadata = (item['metadata']).replace('<br>', '')  
            metadata = (item['metadata']).replace('_cuff_fulfillment:', '')  
            metadata = metadata.split("\n")  
            result_dict = list_to_dict(metadata)  
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
                return {  
                    'outside_personalization': outside_personalization,  
                    'outside_personalization2': outside_personalization2,  
                    'inside_personalization': inside_personalization,  
                    'inside_personalization2': inside_personalization2  
                }  
            except Exception as e:  
                print(f"Order Failed {result_dict} due to error: {e}")  
                return {  
                    'outside_personalization': "",  
                    'outside_personalization2': "",  
                    'inside_personalization': "",  
                    'inside_personalization2': ""  
                }  
  
def item_get_location_by_sku(sku):  
    url = "https://api.skulabs.com/item/get"  
    querystring = {"selector": f'{{"sku":"{sku}"}}'}  
    headers = {"Authorization": API_KEY}  
    try:  
        response = requests.request("GET", url, headers=headers, params=querystring)  
        response.raise_for_status()  
        data = response.json()  
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
  
def init_precheck_routes(app):  
    @app.route('/api/fetch-metadata', methods=['GET'])  
    def fetch_metadata():  
        line_id = request.args.get('line_id')  
        order_number = request.args.get('orderNumber')  
        if not line_id or not order_number:  
            return jsonify({'error': 'line_id and orderNumber are required'}), 400  
        metadata = bct_get_metadata(line_id, order_number)  
        if metadata:  
            return jsonify({'metadata': metadata})  
        else:  
            return jsonify({'error': 'Metadata not found'}), 404  
  
    @app.route('/api/get-api-key', methods=['GET'])  
    def get_api_key():  
        return jsonify({'api_key': API_KEY})  
  
    @app.route('/api/location', methods=['GET'])  
    def get_location():  
        sku = request.args.get('sku')  
        if not sku:  
            return jsonify({'error': 'SKU is required'}), 400  
        location = item_get_location_by_sku(sku)  
        return jsonify({'location': location}) 