# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 17:34:53 2021

@author: claum
"""
import json 
from types import SimpleNamespace
# from collections import defaultdict
# from pprint import pprint
# =======================================
JSONFileName1 = "aircraft.json"
with open(JSONFileName1, "r") as f:
    # ===================================
    # CREATING A DATABASE
    # ===================================
    aircraft_data = json.load(f)
# ===================================================
#   DEFINING AN OBJECT WITH ALL THE DATA
# ===================================================    
Aircraft_Data     = SimpleNamespace(**aircraft_data)
# =======================================
#   PRINTING ALL THE DATA
# =======================================