# config.py

import os    
import re    
import io    
import csv
import json
import random
import qrcode 
import img2pdf
import textwrap 
import tempfile
import requests
import pandas as pd
import pyodbc as odbc  
from pathlib import Path    
from datetime import date, datetime
from create_labels import create_label
from sqlalchemy.orm import sessionmaker
from combined_labels import combined_label
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import create_engine, Column, Integer, String, text 
from flask import Flask, jsonify, render_template, request, redirect, Response, stream_with_context, send_from_directory, url_for

##############################GLobal path changer#####################################
remote_activator = 1
'''Change to 1 for 192.168.80.254 and 0 for comwin2k19'''

if remote_activator == 1:
    DESIGNS_DTG_PATH = '\\\\192.168.80.254\\Shares\\Designs-DTG'
    CAKE_PATH = '\\\\192.168.80.254\\Shares\\CAKE'
    DB_DIR = r'\\192.168.80.254\Shares\Cake' 
    TALLY_DB_DIR = r'\\192.168.80.254\Shares\CAKE\Batch.txt\DTG\tallyStatus'  
else:
    DESIGNS_DTG_PATH = '\\\\comwin2k19dc01\\Shares\\Designs-DTG'
    CAKE_PATH = '\\\\comwin2k19dc01\\Shares\\CAKE'
    DB_DIR = r'\\comwin2k19dc01\Shares\Cake' 
    TALLY_DB_DIR = r'\\comwin2k19dc01\Shares\CAKE\Batch.txt\DTG\tallyStatus'  

from admin import get_all_status, get_connection, init_admin_routes
from cubby import init_cubby_routes, get_cubby
from status import add_status, add_status_combined, sku_labs_add_tag, sku_labs_update_status, init_status_routes
from precheck import init_precheck_routes
from redo import init_redo_routes
from JEWELRY_REDO_DB import add_redo, get_all_redos

from neckless_config import (  
    sku_to_image as nck_sku_to_image,    
    sku_to_fontsize_placement as nck_sku_to_fontsize_placement,
    design_to_font, design_to_sku_to_second_fontsize_placement, design_to_sku_to_third_fontsize_placement, design_to_sku_to_fourth_fontsize_placement,   
) 
from ring_config import (     
    sku_to_font as rng_sku_to_font,    
    sku_to_fontsize_placement as rng_sku_to_fontsize_placement,    
    sku_to_second_fontsize_placement as rng_sku_to_second_fontsize_placement,    
    sku_to_second_line_font as rng_sku_to_second_line_font,   
    rng_sku_needs_white_background, rng_sku_to_image_one_line, rng_sku_to_image_two_line, 
    handle_rng_skus, draw_white_background_if_needed,
)    

# Merge dictionaries    
sku_to_image = {**nck_sku_to_image}    
sku_to_font = {**rng_sku_to_font}    
sku_to_fontsize_placement = {**nck_sku_to_fontsize_placement, **rng_sku_to_fontsize_placement}    
sku_to_second_fontsize_placement = {**rng_sku_to_second_fontsize_placement}
sku_to_second_line_font = {**rng_sku_to_second_line_font}  
  
csv_load_count = 0  

# customtagID 
used_numbers = set()  
index_counter = 0  
  
def generate_custom_id_tag():  
    global index_counter  
      
    # Get the current date formatted as MMDD  
    current_date = datetime.now().strftime("%m%d")  
      
    # Generate a 2-digit random number  
    random_number = random.randint(1000, 9999)  
      
    # Ensure the random number is unique  
    while random_number in used_numbers:  
        random_number = random.randint(1000, 9999)  
    used_numbers.add(random_number)  
      
    # Format the index to be 4 digits, incrementing by 1  
    index = f"{index_counter:04d}"  
    index_counter += 1  
      
    # Combine the components to form the custom ID  
    return f"{current_date}{random_number}{index}"  

# error skus     
def create_check_csv_image(row, load_font):
    IDAutomationHC39M_font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'IDAutomationHC39M.ttf')   
    image = Image.new('RGB', (1000, 1000), color='white')  
    draw = ImageDraw.Draw(image)  
  
    # Text font  
    text_font = load_font('arial.ttf', 70)  
    text = "UNKNOWN ORDER"  
    left, _, right, _ = text_font.getbbox(text)  
    text_width = right - left  
    text_x = (1050 - text_width) // 2  
    text_y = (850 - 200) // 2  
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=text_font)  
  
    # Barcode font  
    barcode_font_size = 50  # font size  
    barcode_font = load_font(IDAutomationHC39M_font_path, barcode_font_size)  
    order_number = "*" + str(row['Order - Number']).strip('"') + "*"  
    barcode_font_color = (0, 0, 0)  # font color (black)  
    draw.text((225, 550), order_number, fill=barcode_font_color, font=barcode_font)  # position  
  
    return image     
 
# force font color   
def process_font_color(font_color, clean_sku, line_index):
    # line 1 = pink
    if (clean_sku == "JMUG11WBUVPPSNNCMUVP") and line_index == 0:   
        return (252, 192, 197)
    # line 1 = grey    
    elif (clean_sku == "JMUG11WBUVPPSLNTBBUVP" or clean_sku == "JMUG11WBUVPPSICG1UVP") and line_index == 0:   
        return (166, 166, 166) 
    elif (clean_sku == "JMUG11WBUVPPSPFCMUVP"):   
        return (223, 4, 4) 
    # black
    if clean_sku.startswith("JMUG11WB") or clean_sku in [  
                # golfballs
                "UVPCCGNHBTUVP",
                # planks  
                 "UVPCCGFSSMUVP", "UVPJMBNSSUVP", "UVPJMASSSUVP", "UVPJMBTSSUVP",                      
                # tumblers  
                 "UVPPSNUBRBUVP", "UVPPSTTPTBUVP", "UVPPSTTPTABUVP", "UVPPSTTOTBUVP",   
                 "UVPPSTTOTABUVP", "UVPPSSLPTBUVP", "UVPPSOPTTBUVP", "UVPPSVETTBUVP",
                 "UVPJMHDBSUVP",
                 ]:    
        font_color = (0, 0, 0)    
    return font_color  

def process_special_rules(clean_sku, line, line_index):  
    # replace between spaces
    if clean_sku in ["UVPCCGTUMBUVP", "UVPCCGTUMWUVP", "UVPJMMAMATBUVP", "UVPJMMAMATWUVP", "UVPPSAUNTTBUVP", "UVPPSAUNTTWUVP", "UVPJMMNSUVP"] and line_index == 1:  # line 2 edit  
        line = re.sub(r'[ ,]+', '_', line)      
    if clean_sku in ["UVPJMMNSUVP"] and line_index == 0:  # line 1 edit  
        line = re.sub(r'[ ,]+', ' * ', line) 
    if clean_sku in ["UVPPSGKNTPUVP", "UVPPSGKNTSUVP"] and line_index == 1:  # line 2 edit  
        line = re.sub(r'[ ,]+', '-*-', line)  
    # replace end spaces  
    if clean_sku in ["UVPPSTTUMBUVP", "UVPPSTTUMWUVP"]:  
        processed_line = f"[_{line}_]"  
    elif clean_sku in ["UVPPSSTILGBHUVP", "UVPPSSTILGWHUVP"]:  
        processed_line = f"{line}_"  
    elif clean_sku in ["UVPJMSLCLBUVP", "UVPJMSLCLWUVP"]:  
        processed_line = f"({line})"
    elif clean_sku in ["UVPCCGTUMBUVP", "UVPCCGTUMWUVP", "UVPJMMAMATBUVP", "UVPJMMAMATWUVP", "UVPPSAUNTTBUVP", "UVPPSAUNTTWUVP"] and line_index == 1:  # line 2 edit  
        processed_line = f"[_{line}_]"
    else:  
        processed_line = line 
    if clean_sku in["JMUG11WBUVPJMFMEMUVP"]:
        processed_line = f"{line}+"
    if clean_sku in["UVPCCGNHBTUVP"]: 
        processed_line = f"{line} did."
    if clean_sku in["JMUG11WBUVPPSPFCMUVP"]: 
        processed_line = f"(...It’s {line})"
  
    return processed_line  

# color hexs
color_name_to_rgb = {  
    'blank': (0, 0, 0),
    'black': (0, 0, 0),    
    'white': (255, 255, 255),
    'coral': (255, 65, 103), 
    'purple': (128, 0, 128),
    'rose gold': (183, 110, 121),
    'teal': (0, 128, 128),
    'blush': (255, 192, 203),
    'lilac': (154, 113, 157),
    'maroon': (73, 5, 5),
    'baby blue': (163, 208, 230),
    'royal blue': (53, 82, 200),
    'navy': (50, 59, 96),
    'iceburg': (203, 217, 222),
    'seascape': (190, 233, 229),
    'gold': (255, 174, 51),
    'orange': (255, 145, 75),
    'yellow': (255, 211, 89),
    'gray': (166, 166, 166),
    'mint': (103, 230, 201),
    'baby pink': (254, 189, 198),
    'hot pink': (255, 102, 196),
    'pink': (255, 148, 202),  
     
}

# unicodes 
font_to_uni = {  
    "a": "0A01",  
    "b": "0A02",  
    "c": "0A03",  
    "d": "0A04",  
    "e": "0A05",  
    "f": "0A06",

    "g": "0B07",  
    "h": "0B08",  
    "i": "0B09",  
    "j": "0B10",  
    "k": "0B11",  
    "l": "0B12",

    "m": "0C13",  
    "n": "0C14",  
    "o": "0C15",  
    "p": "0C16",  
    "q": "0C17",  
    "r": "0C18",

    "s": "0D19",  
    "t": "0D20",  
    "u": "0D21",  
    "v": "0D22",  
    "w": "0D23",  
    "x": "0D24",

    "y": "0E25",  
    "z": "0E26",  
}

def handle_unicode_characters(clean_sku, processed_line, line_index, font_to_uni):  
    # Unicode last letter  
    rng_prefixes = ["RNG"]  
    nck_prefixes = ["NCKGLD", "NCKSIL", "NCKRSG", "NCK02GLD", "NCK02SIL", "NCK02RSG",   
                    "NCK03GLD", "NCK03SIL", "NCK03RSG", "NCK04GLD", "NCK04SIL", "NCK04RSG"]  
      
    if (any(clean_sku.startswith(prefix) for prefix in nck_prefixes) or   
       (any(clean_sku.startswith(prefix) for prefix in rng_prefixes) and line_index == 1)):  
        last_char = processed_line[-1].lower()  
        unicode_code = font_to_uni.get(last_char)  
        if unicode_code:  
            processed_line = processed_line[:-1] + chr(int(unicode_code, 16))  
        else:  
            print(f"Warning: Unicode character not found for '{last_char}'.")  
  
    # Unicode first letter (for NCK SKUs only)  
    month_codes = {  
        "NCKJAN": "1A01", "NCKFEB": "1A02", "NCKMAR": "1A03", "NCKAPR": "1A04",  
        "NCKMAY": "1A05", "NCKJUN": "1A06", "NCKJUL": "1A07", "NCKAUG": "1A08",  
        "NCKSEP": "1A09", "NCKOCT": "1A10", "NCKNOV": "1A11", "NCKDEC": "1A12",  
    }  
    for month, code in month_codes.items():  
        if clean_sku.startswith(month):  
            first_char = processed_line[0]  
            unicode_code = font_to_uni.get(first_char.lower())  
            if unicode_code:  
                processed_line = chr(int(code, 16)) + first_char + processed_line[1:]  
            else:  
                print(f"Warning: Unicode character not found for '{first_char}'.")  
            break  
  
    return processed_line

