# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 17:37:12 2021

@author: claum
"""
import pandas as pd
customer_json_file = 'aircraft.json'
customers_json = pd.read_json(customer_json_file,
   convert_dates=True)
customers_json.head()
print(customers_json)

from IPython.display import HTML, display
# render dataframe as html
subvar = customers_json
h1 = subvar.to_html()
#write html to file
text_file = open("index1.html", "w")
text_file.write(h1)
text_file.close()

display(h1)
# print(html)
# display(HTML('html'))