# ring_config.py

import os 
from PIL import ImageDraw 
  
def handle_rng_skus(clean_sku, lines, rng_sku_to_image_one_line, rng_sku_to_image_two_line, original_background_image_path):  
    background_image_path = original_background_image_path  
  
    if clean_sku.startswith("RNG"):  
        if len(lines) == 1:  
            background_image_path = rng_sku_to_image_one_line.get(clean_sku, original_background_image_path)  
        elif len(lines) == 2:  
            background_image_path = rng_sku_to_image_two_line.get(clean_sku, original_background_image_path)  
    elif clean_sku.startswith("SRN"):  
        background_image_path = rng_sku_to_image_one_line.get(clean_sku, original_background_image_path)  
  
    return background_image_path 

def draw_white_background_if_needed(clean_sku, rng_sku_needs_white_background, font, line, text_x, text_y, draw_white_background, draw, is_first_line):  
    if rng_sku_needs_white_background(clean_sku):  
        left, text_y1, right, text_y2 = font.getbbox(line)  
        text_width = right - left  
        text_height = text_y2 - text_y1  
        num_chars_line2 = len(line)   
        draw_white_background(draw, text_x, text_y, text_width, text_height, num_chars_line2, is_first_line)  

rng_sku_to_image_two_line = { 

   # size 4-6
    "RNG35GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),  
    "RNG35SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),     
    "RNG35RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),    
    "RNGDBL35GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),    
    "RNGDBL35SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),     
    "RNGDBL35RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),    

    "RNG46GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),  
    "RNG46SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),     
    "RNG46RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),    
    "RNGDBL46GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),    
    "RNGDBL46SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),     
    "RNGDBL46RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'), 

   # size 7-8
    "RNG68GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),  
    "RNG68SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),
    "RNG68RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),
    "RNGDBL68GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'), 
    "RNGDBL68SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),  
    "RNGDBL68RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),

    "RNG78GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'), 
    "RNG78SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),  
    "RNG78RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),
    "RNGDBL78GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'), 
    "RNGDBL78SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),  
    "RNGDBL78RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size-DBL.png'),

   # size 9-11
    "RNG910GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),  
    "RNG910SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),  
    "RNG910RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),   
    "RNGDBL910GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),   
    "RNGDBL910SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),    
    "RNGDBL910RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'), 

    "RNG911GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),  
    "RNG911SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),  
    "RNG911RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),   
    "RNGDBL911GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),   
    "RNGDBL911SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),    
    "RNGDBL911RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11-DBL.png'),   

} 

rng_sku_to_image_one_line = { 
   
   # size 4-6
    "RNG35GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),  
    "RNG35SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),  
    "RNG35RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),
    "RNGDBL35GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),  
    "RNGDBL35SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),  
    "RNGDBL35RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),

    "RNG46GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),  
    "RNG46SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),  
    "RNG46RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),
    "RNGDBL46GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),  
    "RNGDBL46SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),  
    "RNGDBL46RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size4-6.png'),

   # size 7-8
    "RNG68GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),  
    "RNG68SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),  
    "RNG68RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),
    "RNGDBL68GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),  
    "RNGDBL68SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),  
    "RNGDBL68RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),

    "RNG78GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),  
    "RNG78SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),  
    "RNG78RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),
    "RNGDBL78GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),  
    "RNGDBL78SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),  
    "RNGDBL78RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size7-8.png'),

   # size 9-11
    "RNG910GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),  
    "RNG910SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),  
    "RNG910RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),  
    "RNGDBL910GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),   
    "RNGDBL910SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),    
    "RNGDBL910RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),

    "RNG911GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),  
    "RNG911SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),  
    "RNG911RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),  
    "RNGDBL911GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),   
    "RNGDBL911SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),    
    "RNGDBL911RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'size9-11.png'),

   # SMOL RINGS
    "SRN004GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN004SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN004RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'), 

    "SRN005GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN005SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN005RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'), 

    "SRN006GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN006SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN006RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),

    "SRN007GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN007SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN007RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'), 

    "SRN008GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN008SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN008RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'), 

    "SRN009GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN009SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN009RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'), 

    "SRN010GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN010SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN010RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'), 

    "SRN011GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN011SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN011RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'), 

    "SRN012GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN012SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'),  
    "SRN012RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'SRNring.png'), 
} 

sku_to_font = { 

    "RNG35GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 
    "RNG35SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNG35RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 
    "RNGDBL35GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),  
    "RNGDBL35SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNGDBL35RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 

    "RNG46GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 
    "RNG46SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNG46RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 
    "RNGDBL46GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),  
    "RNGDBL46SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNGDBL46RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 

    "RNG68GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNG68SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNG68RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 
    "RNGDBL68GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNGDBL68SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNGDBL68RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 

    "RNG78GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),  
    "RNG78SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNG78RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 
    "RNGDBL78GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNGDBL78SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),  
    "RNGDBL78RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 

    "RNG910GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNG910SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),  
    "RNG910RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 
    "RNGDBL910GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNGDBL910SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNGDBL910RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 

    "RNG911GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNG911SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),  
    "RNG911RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'), 
    "RNGDBL911GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNGDBL911SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),   
    "RNGDBL911RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyTop.ttf'),

   # SMOL RINGS
    "SRN004GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 
    "SRN004SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'),   
    "SRN004RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 

    "SRN005GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 
    "SRN005SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'),   
    "SRN005RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 

    "SRN006GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 
    "SRN006SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'),   
    "SRN006RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 

    "SRN007GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 
    "SRN007SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'),   
    "SRN007RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 

    "SRN008GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 
    "SRN008SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'),   
    "SRN008RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 

    "SRN009GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 
    "SRN009SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'),   
    "SRN009RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 

    "SRN010GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 
    "SRN010SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'),   
    "SRN010RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 

    "SRN011GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 
    "SRN011SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'),   
    "SRN011RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 

    "SRN012GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 
    "SRN012SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'),   
    "SRN012RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'JMH Typewriter.ttf'), 

} 

sku_to_second_line_font = {  

    "RNG35GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 
    "RNG35SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNG35RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 
    "RNGDBL35GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),  
    "RNGDBL35SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNGDBL35RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 

    "RNG46GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 
    "RNG46SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNG46RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 
    "RNGDBL46GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),  
    "RNGDBL46SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNGDBL46RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 

    "RNG68GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNG68SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNG68RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 
    "RNGDBL68GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNGDBL68SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNGDBL68RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 

    "RNG78GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),  
    "RNG78SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNG78RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 
    "RNGDBL78GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNGDBL78SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),  
    "RNGDBL78RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 

    "RNG910GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNG910SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),  
    "RNG910RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 
    "RNGDBL910GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNGDBL910SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNGDBL910RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 

    "RNG911GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNG911SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),  
    "RNG911RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 
    "RNGDBL911GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNGDBL911SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'),   
    "RNGDBL911RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'ShelbyBottom.ttf'), 

} 

sku_to_fontsize_placement = { # 2nd Name
     # size 4-6 
    "RNG35GLD": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG35SIL": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG35RSG": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL35GLD": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    }, 
    "RNGDBL35SIL": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL35RSG": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },

    "RNG46GLD": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG46SIL": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG46RSG": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL46GLD": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    }, 
    "RNGDBL46SIL": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL46RSG": {  
       "max_x": 3225,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },

    # size 7-8
    "RNG68GLD": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG68SIL": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG68RSG": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL68GLD": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL68SIL": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL68RSG": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },

    "RNG78GLD": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG78SIL": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG78RSG": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL78GLD": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL78SIL": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL78RSG": {  
        "max_x": 3485,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },

    # size 9-11
    "RNG910GLD": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG910SIL": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG910RSG": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL910GLD": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL910SIL": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL910RSG": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },

    "RNG911GLD": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG911SIL": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNG911RSG": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL911GLD": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL911SIL": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },
    "RNGDBL911RSG": {  
       "max_x": 3520,  
        1: (580, None, 100),  2: (580, None, 100),  3: (580, None, 100),  4: (580, None, 100),  5: (580, None, 100),  
        6: (580, None, 100),  7: (580, None, 100),  8: (580, None, 100),  9: (580, None, 100), 10: (580, None, 100),  
       11: (580, None, 100), 12: (580, None, 100), 13: (580, None, 100), 14: (580, None, 100), 15: (580, None, 100),  
       16: (580, None, 100), 17: (580, None, 100), 18: (580, None, 100), 19: (580, None, 100), 20: (580, None, 100),  
    },

   # SMOL RINGS
    "SRN004GLD": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN004SIL": {    
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },   
    "SRN004RSG": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    }, 
    "SRN005GLD": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN005SIL": {    
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },   
    "SRN005RSG": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN006GLD": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN006SIL": {    
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },   
    "SRN006RSG": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN007GLD": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN007SIL": {    
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },   
    "SRN007RSG": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN008GLD": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN008SIL": {    
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },   
    "SRN008RSG": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN009GLD": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN009SIL": {    
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },   
    "SRN009RSG": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN010GLD": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN010SIL": {    
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },   
    "SRN010RSG": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN011GLD": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN011SIL": {    
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },   
    "SRN011RSG": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN012GLD": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    "SRN012SIL": {    
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },   
    "SRN012RSG": {   
        1: (88, None, -15),  2: (88, None, -15),  3: (88, None, -15),  4: (88, None, -15),  5: (88, None, -15),  
        6: (88, None, -15),  7: (88, None, -15),  8: (88, None, -15),  9: (88, None, -15), 10: (88, None, -15),
       11: (88, None, -15), 12: (88, None, -15), 13: (88, None, -15), 14: (88, None, -15), 15: (88, None, -15),
    },
    
} 

sku_to_second_fontsize_placement = { # 1st Name
    
    # size 4-6
    "RNG35GLD": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNG35SIL": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNG35RSG": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL35GLD": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL35SIL": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL35RSG": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },

    "RNG46GLD": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNG46SIL": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNG46RSG": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL46GLD": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL46SIL": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL46RSG": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },

    # size 7-8
    "RNG68GLD": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNG68SIL": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNG68RSG": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL68GLD": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL68SIL": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL68RSG": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },

    "RNG78GLD": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNG78SIL": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNG78RSG": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL78GLD": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL78SIL": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },
    "RNGDBL78RSG": {  
        1: (580, 440, 100),  2: (580, 440, 100),  3: (580, 440, 100),  4: (580, 440, 100),  5: (580, 440, 100),  
        6: (580, 440, 100),  7: (580, 440, 100),  8: (580, 440, 100),  9: (580, 440, 100), 10: (580, 440, 100), 
       11: (580, 440, 100), 12: (580, 440, 100), 13: (580, 440, 100), 14: (580, 440, 100), 15: (580, 440, 100),  
       16: (580, 440, 100), 17: (580, 440, 100), 18: (580, 440, 100), 19: (580, 440, 100), 20: (580, 440, 100),  
    },


    # size 9-11
    "RNG910GLD": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },
    "RNG910SIL": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },
    "RNG910RSG": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },
    "RNGDBL910GLD": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },
    "RNGDBL910SIL": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },
    "RNGDBL910RSG": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },

    "RNG911GLD": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },
    "RNG911SIL": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },
    "RNG911RSG": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },
    "RNGDBL911GLD": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },
    "RNGDBL911SIL": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },
    "RNGDBL911RSG": {  
        1: (580, 310, 100),  2: (580, 310, 100),  3: (580, 310, 100),  4: (580, 310, 100),  5: (580, 310, 100),  
        6: (580, 310, 100),  7: (580, 310, 100),  8: (580, 310, 100),  9: (580, 310, 100), 10: (580, 310, 100), 
       11: (580, 310, 100), 12: (580, 310, 100), 13: (580, 310, 100), 14: (580, 310, 100), 15: (580, 310, 100),  
       16: (580, 310, 100), 17: (580, 310, 100), 18: (580, 310, 100), 19: (580, 310, 100), 20: (580, 310, 100),  
    },    
}  
   
def rng_sku_needs_white_background(clean_sku):  
    return clean_sku.startswith("RNG")

