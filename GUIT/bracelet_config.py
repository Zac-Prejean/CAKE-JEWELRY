import os  

sku_to_image = { 

    "BCT4GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'braceletSM.png'),
    "BCT4SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'braceletSM.png'),
    "BCT4RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'braceletSM.png'),
    "BCT6GLD": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'braceletLG.png'),
    "BCT6SIL": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'braceletLG.png'),
    "BCT6RSG": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'jewlery', 'braceletLG.png'),

}

design_to_font = { 

    "MVBoli": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'MVBoli.ttf'), 
    "Serif": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'NotoSerif.ttf'), 
    "PTSerif-Bold": os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts_JEW', 'PTSerif-Bold.ttf'),

}

sku_to_fontsize_placement = {
    "MVBoli": {   
        1: (430, 100),  2: (430, 100),  3: (430, 100),  4: (430, 100),  5: (430, 100),  
        6: (430, 100),  7: (430, 100),  8: (430, 100),  9: (430, 100), 10: (430, 100),  
       11: (430, 100), 12: (430, 100), 13: (430, 100), 14: (430, 100), 15: (430, 100),  
       16: (430, 100), 17: (430, 100), 18: (430, 100), 19: (430, 100), 20: (430, 100),  
    },
    "Serif": {   
        1: (430, 100),  2: (430, 100),  3: (430, 100),  4: (430, 100),  5: (430, 100),  
        6: (430, 100),  7: (430, 100),  8: (430, 100),  9: (430, 100), 10: (430, 100),  
       11: (430, 100), 12: (430, 100), 13: (430, 100), 14: (430, 100), 15: (430, 100),  
       16: (430, 100), 17: (430, 100), 18: (430, 100), 19: (430, 100), 20: (430, 100),  
    },
    "PTSerif-Bold": {   
        1: (430, 100),  2: (430, 100),  3: (430, 100),  4: (430, 100),  5: (430, 100),  
        6: (430, 100),  7: (430, 100),  8: (430, 100),  9: (430, 100), 10: (430, 100),  
       11: (430, 100), 12: (430, 100), 13: (430, 100), 14: (430, 100), 15: (430, 100),  
       16: (430, 100), 17: (430, 100), 18: (430, 100), 19: (430, 100), 20: (430, 100),  
    },
}