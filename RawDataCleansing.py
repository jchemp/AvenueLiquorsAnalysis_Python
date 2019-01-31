# Author: Joshua Chemparathy
# Purpose: Cleansing of txt file from 15 year old software. Text file combined transaction and line item data, as well as had other errors.
# Date: January 16, 2019
# Last Modified: January 29, 2019

import os
import csv
import re
import pandas as pd

# raw data input 
fn = input('Enter file name: ')
if len(fn) < 1: fn = 'salestransactions.TXT'
fn_sales_line = "output_sales_line.csv"
fn_sales_header = "output_sales_header.csv"

#delete output files if exists
if os.path.exists(fn_sales_line):
  os.remove(fn_sales_line)
if os.path.exists(fn_sales_header):
  os.remove(fn_sales_header)

# check whether input file is a txt file. open two csv files to write line item and header data to after parsing. 
if fn[-4:] == '.TXT':
    fn_raw = open(fn, "r", encoding= "ISO-8859-1")
    fh_sales_line = open(fn_sales_line, 'w')
    fh_sales_header = open(fn_sales_header, 'w')
    fh_raw = list(csv.reader(fn_raw, delimiter = ','))
    fw_sales_line = csv.writer(fh_sales_line)
    fw_sales_header = csv.writer(fh_sales_header)

#write csv file headers
fw_sales_line.writerow(['trans_id', 'trans_date', 'trans_time', 'sale_id', 'product_desc','product_code', 'product_qty', 'product_price', 'product_tax_id'])
fw_sales_header.writerow(['trans_id', 'trans_date', 'trans_time', 'subtotal', 'tax_rate', 'tax_amt', 'total'])

#handle the first row of the file and assign it to another mutable variable
temp_list = [fh_raw[0][0], fh_raw[0][1], fh_raw[0][2]] 
temp_list_ext = temp_list[:]

for count,line in enumerate(fh_raw[1:],1):  #for loop and skip first row
    if count == len(fh_raw)-1:  #kill the loop at the last line
        break
    if re.search('^Ä', fh_raw[count][0]):
        if fh_raw[count][8] == 'Cash': #manage outlier lines in txt files
            temp_list_ext.extend([fh_raw[count][2],fh_raw[count][14],fh_raw[count][16],fh_raw[count][19]]) #create sales header and write for txt file outlier
            fw_sales_header.writerow(temp_list_ext)          
        else:
            temp_list_ext.extend([fh_raw[count][2],fh_raw[count][11],fh_raw[count][13],fh_raw[count][16]])#create sales header and write 
            fw_sales_header.writerow(temp_list_ext)
        temp_list = [fh_raw[count+1][0],fh_raw[count+1][1],fh_raw[count+1][2]] #set temp_list variable to new transaction id, date, and time for both files 
        temp_list_ext = temp_list[:]
        continue
    if (len(fh_raw[count])<7 or re.search('^Ä', fh_raw[count][6])): #skip the short header lines and blank sales
        continue
    temp_list_ext.extend([fh_raw[count][0],fh_raw[count][1],fh_raw[count][2],fh_raw[count][3],fh_raw[count][6],fh_raw[count][7]]) #create sales line and write
    fw_sales_line.writerow(temp_list_ext)
    temp_list_ext = temp_list[:] #reset the temp_list_ext variable to be used in for loop for similar sales lines

#test if pandas can now read these files
df = pd.read_csv(fn_sales_header)
print(df.head(n=5))
df = pd.read_csv(fn_sales_line)
print(df.head(n=5))

#close files
fn_raw.close()
fh_sales_line.close()
fh_sales_header.close()