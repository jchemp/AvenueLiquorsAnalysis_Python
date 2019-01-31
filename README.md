# Avenue Liquors Analysis

This code is analyze 2017-2019 retail transaction data to create promotional bundles for increasing revenue. 

## Step 1: Data Cleaning
The raw data was extracted from a 15+ year old piece of software, which was never updated. The raw csv file ended up being very poorly formatted txt files. The file combined transaction level and line item level data, and there were a few consistent outliers, such as cancelled transactions, which needed to be parsed. Pandas could not read this data, and it did not seem easy to do all the cleansing in Pandas. I was decided to clean the text files outside of Pands, export them into two seperate csv files (transaction level, line item level), and then munch these two clean files in Pandas. 

## Step 2: Data Analysis - in progress
Now that the data is clean, the fun part begins!
