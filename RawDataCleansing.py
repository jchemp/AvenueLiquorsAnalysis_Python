import pandas as pd

class TransformationObject:
    '''
    Author: Joshua Chemparathy
    Purpose: Cleansing of txt file from 15-year-old software. Text file combined transaction and line item data, as well as had other errors.
    Date: January 16, 2019
    Last Modified:
        June 9, 2023 - This was a bit of an unnecessary update, but it was a nice little exercise to remind myself of my previous work.
        Run by updating the input_datafile_name.txt, then run FILENAME.py from the terminal.
    '''

    def __init__(self):
        self.LIST_INPUT_SALES_DATA = [
            'input_salestransactions.TXT'
            ,
        ]
        self.transform_files()

    def transform_files(self):
        for file in self.LIST_INPUT_SALES_DATA:
            df = self.open_file(file_name=file)
            df = self.transformation_steps(df=df)
            self.export_file(df=df, save_file_name='modified_' + file)
        return df

    def open_file(self, file_name):
        df = pd.read_csv(file_name, sep=',', header=None, encoding='ISO-8859-1', engine='python', names=['col' + str(x) for x in range(50)])
        return df

    def transformation_steps(self, df):
        df = self.isolate_transaction_date_time(df=df)
        df = self.isolate_transaction_total(df=df)
        df = self.correct_deviation(df=df)
        df = self._forward_fill_transaction_dates(df=df)
        df = self._back_fill_transaction_summary(df=df)
        df = self.remove_transaction_summary_lines(df=df)
        df = self.rename_line_item_columns(df=df)
        df = self.limit_columns(df=df)
        return df

    def isolate_transaction_date_time(self, df):
        subset_condition = df['col5'] == 'Cash'
        df.loc[subset_condition, 'transaction_id'] = df.loc[subset_condition, 'col0']
        df.loc[subset_condition, 'transaction_date'] = df.loc[subset_condition, 'col1']
        df.loc[subset_condition, 'transaction_time'] = df.loc[subset_condition, 'col2']
        return df

    def isolate_transaction_total(self, df):
        first_condition = df['col0'].str.startswith(('ƒ', 'Ä'))
        df.loc[first_condition, 'code'] = df.loc[first_condition, 'col14']
        df.loc[first_condition, 'transaction_subtotal'] = df.loc[first_condition, 'col2']
        df.loc[first_condition, 'transaction_tax_percent'] = df.loc[first_condition, 'col11']
        df.loc[first_condition, 'transaction_tax_amount'] = df.loc[first_condition, 'col13']
        df.loc[first_condition, 'transaction_total'] = df.loc[first_condition, 'col16']
        return df

    def correct_deviation(self, df):
        error_condition = df['col8'] != 'Shipping:'
        df.loc[error_condition, 'transaction_tax_percent'] = df.loc[error_condition, 'col14']
        df.loc[error_condition, 'transaction_tax_amount'] = df.loc[error_condition, 'col16']
        df.loc[error_condition, 'transaction_total'] = df.loc[error_condition, 'col19']
        return df

    def _forward_fill_transaction_dates(self, df):
        target_columns = ['transaction_id', 'transaction_date', 'transaction_time']
        df[target_columns] = df[target_columns].ffill()
        return df

    def _back_fill_transaction_summary(self, df):
        target_columns = ['transaction_subtotal', 'transaction_tax_percent', 'transaction_tax_amount', 'transaction_total']
        df[target_columns] = df[target_columns].bfill()
        return df

    def remove_transaction_summary_lines(self, df):
        df = df[~(df['col5'] == 'Cash')]
        df = df[~(df['col0'].str.startswith(('ƒ', 'Ä')))]
        return df

    def rename_line_item_columns(self, df):
        LINE_ITEM_RENAME = {
            "col0": "product_id",
            "col1": "product_desc",
            "col2": "product_code",
            "col3": "product_qty",
            "col6": "product_price",
            "col7": "product_tax_id"
        }
        df = df.rename(columns=LINE_ITEM_RENAME)
        return df

    def limit_columns(self, df):
        export_columns = [
            'transaction_id', 'transaction_date', 'transaction_time', 'transaction_subtotal',
            'transaction_tax_percent', 'transaction_tax_amount', 'transaction_total', 'product_id',
            'product_desc', 'product_code', 'product_qty', 'product_price', 'product_tax_id'
        ]
        df = df[export_columns]

        df['price*qty'] = df['product_price'] * df['product_qty']

        return df

    def export_file(self, df, save_file_name):
        df.to_csv(save_file_name, index=False)


if __name__ == "__main__":
    transformed = TransformationObject()
