# Avenue Liquors Analysis

This code is to analyze 2017-2019 retail transaction data to create promotional bundles for increasing revenue. 


## Files
RawDataCleansing.py - Code for parsing the entire txt data file to create two pandas-friendly csv data files. <br />
SalesAnalysis_Pandas.ipynb - Beginning of data analysis in pandas <br />
input_salestransactions.TXT	- sample of original file containing 1,668,645 lines. <br />
output_sales_header.csv - sample of transaction level output	<br />
output_sales_line.csv - sample of line-item level output<br />

Note - only a sample of the data is shown online.

## Step 1: Data Cleaning
The raw data was extracted from a 15+ year old piece of software, which was never updated. The raw csv file ended up being very poorly formatted txt files. The file combined transaction level and line item level data, and there were a few consistent outliers, such as cancelled transactions, which needed to be parsed. Pandas could not read this data, and it did not seem easy to do all the cleansing in Pandas. I decided to clean the text files outside of Pandas, export them into two seperate csv files (transaction level, line item level), and then munch these two clean files in Pandas. 

### The Raw Data
![raw](../master/Screenshots/input_rawdata.png)

### The CSV Outputs
![header](../master/Screenshots/output_header.png)

![line](../master/Screenshots/output_lineitem.png)

## Step 2: Data Analysis - in progress
Now that the data is clean, the fun part begins!
