import pandas as pd
import os

dir_xlsx = os.path.join(os.getcwd(), "cleaned_xlsx") 
dir_csv = os.path.join(os.getcwd(), "cleaned_csv") 
xlsx_files = ['blinkit_customer_feedback.xlsx','blinkit_customers.xlsx','blinkit_delivery_performance.xlsx', 
         'blinkit_inventory.xlsx','blinkit_marketing_performance.xlsx','blinkit_order_items.xlsx', 
         'blinkit_orders.xlsx','blinkit_products.xlsx']

csv_files = ['blinkit_customer_feedback.csv','blinkit_customers.csv','blinkit_delivery_performance.csv', 
         'blinkit_inventory.csv','blinkit_marketing_performance.csv','blinkit_order_items.csv', 
         'blinkit_orders.csv','blinkit_products.csv']

for xlsx_file, csv_file in zip(xlsx_files, csv_files):

    xlsx_path = os.path.join(dir_xlsx, xlsx_file)
    csv_path = os.path.join(dir_csv, csv_file)

    df = pd.read_excel(xlsx_path)        
    df.to_csv(csv_path, index=False, encoding='utf-8')  



    