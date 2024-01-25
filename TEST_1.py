import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import numpy as np
import os
import math
import re

from teradataml import create_context,copy_to_sql,get_connection,remove_context, execute_sql, DataFrame, fastexport
from teradataml.common import exceptions as TD_exceptions

from sqlalchemy.sql import sqltypes


class CSVUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Uploader")
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, foreground="green")
        self.status_bar.pack(pady=5)

        self.error_var = tk.StringVar()
        self.error_bar = ttk.Label(root, textvariable=self.error_var, foreground="red")
        self.error_bar.pack(pady=5)

        self.file_path_label = ttk.Label(root, text="No file selected")
        self.file_path_label.pack(pady=10)

        self.browse_button = ttk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=10)
        
        self.create_ddl = ttk.Button(root, text="Create SQL DDL", command=self.create_insert_sql)
        self.create_ddl.pack(pady=10)

        self.variable_types = {}
        self.variable_lengths = {}
        self.types_frame = ttk.Frame(root)
        self.types_frame.pack(pady=10)

        self.username_label = ttk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = ttk.Entry(root)
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.pack(pady=10)

        self.connect_button = ttk.Button(root, text="Connect to Teradata", command=self.connect_to_teradata)
        self.connect_button.pack(pady=10)

        self.append_button = ttk.Button(root, text="Append to Teradata", command=self.append_to_teradata)
        self.append_button.pack(pady=10)
    
    def __del__(self):
        self.disconnect_from_teradata()
    
    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.file_path_label.config(text=self.file_path)
        self.load_csv(self.file_path)
        self.dirname = os.path.dirname(self.file_path)

    def load_csv(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            file_name = os.path.basename(file_path)
            df_shape = self.df.shape
            rows = df_shape[0]
            cols = df_shape[1]
            self.show_status(f"Sucessfully Read {file_name}.\nFile contains {rows} rows & {cols} columns")
            self.transform_df()
        except pd.errors.EmptyDataError:
            self.show_error("Selected file is empty.")

    def transform_df(self):
        try:
            self.df['HCC_MIN_AMT'] = self.df['HCC_MIN_AMT'].str.replace(',','')
            self.df['Sub_Limit'] = self.df['Sub_Limit'].str.replace(',','')
            self.df['BoB_CONTR_DATE'] = self.df['BoB_CONTR_DATE'].fillna('0001-01-01')
            self.df['HAS_GO_LIVE_DATE'] = self.df['HAS_GO_LIVE_DATE'].fillna('0001-01-01')
            self.df['RPT_EFF_DT'] = self.df['RPT_EFF_DT'].fillna('0001-01-01')
            self.df['LOAD_DATE'] = self.df['LOAD_DATE'].fillna('0001-01-01')

            self.df = self.df.astype({
                'ACCT' : 'string'
                , 'PG_YEAR' : 'int32'
#                , 'HAS_GO_LIVE_DATE' :'datetime64[ns]'
#                , 'BoB_CONTR_DATE' :'datetime64[ns]'
#                , 'RPT_EFF_DT' :'datetime64[ns]'
                , 'HAS_GO_LIVE_DATE' :'string'
                , 'BoB_CONTR_DATE' :'string'
                , 'RPT_EFF_DT' :'string'
                , 'BoB_CONTR_FLAG' :'int32'
                , 'ACCT_ID' : 'string'
                , 'STATE' : 'string'
                , 'HAS_SERVICE' : 'string'
                , 'HCC_MIN_AMT' : 'float32'
                , 'Acct_Cycle' : 'string'
                , 'HAS_FEE_TYPE' : 'string'
                , 'BoB_FLAG' : 'string'
                , 'PG_FLAG' : 'int32'
                , 'PG_ORDER' : 'int32'
                , 'PERFORMANCE_GUARANTEE' : 'string'
                , 'BILLED_PEPM_FEE' : 'float32'
                , 'BREAK_EVEN_SUM_PEPM' : 'float32'
                , 'BREAK_EVEN_AMOUNT_PEPM' : 'float32'
                , 'MAX_RETURN_PEPM' : 'float32'
                , 'TIER' : 'int32'
                , 'RETURN_LEVEL' : 'string'
                , 'PERFORMANCE_STANDARD_LOWER' : 'float32'
                , 'PERFORMANCE_STANDARD_HIGHER' : 'float32'
                , 'RETURN_AT_RISK' : 'float32'
                , 'PERFORMANCE_STANDARD' : 'string'
                , 'FEE_AT_RISK' : 'float32'
                , 'Estimated_Settlement_Amt' : 'float32'
                , 'LOAD_DATE' : 'string'
                , 'APR_FLAG' : 'int32'
                , 'SUB_CNT' : 'int32'
                , 'Sub_Limit' : 'int32'
                , 'MBR_CNT' : 'int32'
                , 'Status': 'string'
                , 'MBRSHP_HAS_UPDATE_YYYYMM' : 'string'
                , 'EDUCATED_RATE_IND' : 'int32'
                , 'HCC_RATE_IND' : 'int32'
                , 'BoB_Contr_Rate_Ind' : 'int32'
                , 'BoB_Contr_Survey_Ind' : 'int32'
                , 'BoB_Contr_Calnd_Ind' : 'int32'

            
                            }
                            , errors='ignore'

            )
            for a,b in self.df.dtypes.reset_index().iterrows():
                #print(b['index'],b[0])
                if b[0] in ['string[python]']:
                    col_name = b['index']
                    self.df[col_name] = self.df[col_name].replace(pd.NA,'?')

        except Exception as e:
            self.show_error(f'Error: {e}')
    
    def show_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def show_error(self, message):
        self.error_var.set(message)
        self.root.update_idletasks()

    def connect_to_teradata(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        host='teradata-data.fyiblue.com'
        logmech ='LDAP'


        if not username or not password:
            self.show_error("Please enter both username and password.")
            return

        try:
            self.td_connection = create_context(
                username=username,
                password=password,
                host=host,
                logmech=logmech
            )

            self.show_status(f"UserName {username} has connected 2 Teradata :)")
        except Exception as e:
            self.show_error(f"Error connecting to Teradata: {e}")
    
    def create_insert_sql(self):
        self.ddl_file_name = os.path.join(self.dirname,'DDL.sql')
        row_number = 0
        df_cols = self.df.columns.tolist()
        sql_insert_all = ''
        for row in self.df.itertuples():
            #if row_number == 1:
                #break
            sql_insert = 'INSERT INTO CAS.HAS_PERFORMANCE_GUARANTEES_TEST_SH ('
            for idx, col_x in enumerate(df_cols):
                if len(df_cols) == idx +1:
                    sql_insert += f'{col_x})'
                else:
                    sql_insert += f'{col_x}, '

            sql_insert += 'VALUES ('

            for i in range(1,len(row)):
                if len(row) - 1 == i:
                    col_number = i - 1
                    df_col = df_cols[col_number]
                    df_col_type = self.df[df_col].dtype
                    if (type(row[i]) == float):
                        if math.isnan(row[i]) == True:
                            sql_insert += 'NULL'
                        else:
                            row_temp = float(row[i])
                            sql_insert += f'{row_temp}'
                    elif df_col_type == 'string':
                        temp_row = row[i].replace("'","''")
                        row_temp = f"'{temp_row}'"
                        sql_insert += f'{row_temp}'
                        #print(df_col,'||',df_col_type,'||',row_temp)
                    elif df_col_type == 'int32':
                        row_temp = int(row[i])
                        sql_insert += f'{row_temp}'
                        #print(df_col,'||',df_col_type,'||',row_temp)
                    else:
                        print(type(row[i]))
                        row_temp = row[i]
                        print(df_col,'||',df_col_type,'||',row_temp)
                else:
                    col_number = i - 1
                    df_col = df_cols[col_number]
                    df_col_type = self.df[df_col].dtype
                    if (type(row[i]) == float):
                        if math.isnan(row[i]) == True:
                            sql_insert += 'NULL,'
                        else:
                            row_temp = float(row[i])
                            sql_insert += f'{row_temp},'
                    elif df_col_type == 'string':
                        temp_row = row[i].replace("'","''")
                        row_temp = f"'{temp_row}'"
                        sql_insert += f'{row_temp},'
                        #print(df_col,'||',df_col_type,'||',row_temp)
                    elif df_col_type == 'int32':
                        row_temp = int(row[i])
                        sql_insert += f'{row_temp},'
                        #print(df_col,'||',df_col_type,'||',row_temp)
                    else:
                        print(type(row[i]))
                        row_temp = row[i]
                        print(df_col,'||',df_col_type,'||',row_temp)


            sql_insert += ');\n'
            row_number += 1
            sql_insert_all += sql_insert
        
        with open(self.ddl_file_name,'w') as file:
            file.write(sql_insert_all)

    def append_to_teradata(self):

        if self.df.empty:
            self.show_error("DataFrame is Empty.")
            return
        
        
        input_schema = 'CAS'
        input_table_name = "HAS_PERFORMANCE_GUARANTEES_TEST_SH"  # Replace with your actual Teradata table name
        input_p_idx = 'ACCT_ID'
        date_types = {
            'ACCT' : sqltypes.VARCHAR
            , 'PG_YEAR' : sqltypes.INTEGER
            , 'HAS_GO_LIVE_DATE' : sqltypes.DATE
            , 'BoB_CONTR_DATE' : sqltypes.DATE
            , 'RPT_EFF_DT' : sqltypes.DATE
            , 'BoB_CONTR_FLAG' : sqltypes.INTEGER
            , 'ACCT_ID' : sqltypes.VARCHAR
            , 'STATE' : sqltypes.VARCHAR
            , 'HAS_SERVICE' : sqltypes.VARCHAR
            , 'HCC_MIN_AMT' : sqltypes.FLOAT
            , 'Acct_Cycle' : sqltypes.VARCHAR
            , 'HAS_FEE_TYPE' : sqltypes.VARCHAR
            , 'BoB_FLAG' : sqltypes.VARCHAR
            , 'PG_FLAG' : sqltypes.INTEGER
            , 'PG_ORDER' : sqltypes.INTEGER
            , 'PERFORMANCE_GUARANTEE' : sqltypes.VARCHAR
            , 'BILLED_PEPM_FEE' : sqltypes.FLOAT
            , 'BREAK_EVEN_SUM_PEPM' : sqltypes.FLOAT
            , 'BREAK_EVEN_AMOUNT_PEPM' : sqltypes.FLOAT
            , 'MAX_RETURN_PEPM' : sqltypes.FLOAT
            , 'TIER' : sqltypes.INTEGER
            , 'RETURN_LEVEL' : sqltypes.VARCHAR
            , 'PERFORMANCE_STANDARD_LOWER' : sqltypes.FLOAT
            , 'PERFORMANCE_STANDARD_HIGHER' : sqltypes.FLOAT
            , 'RETURN_AT_RISK' : sqltypes.FLOAT
            , 'PERFORMANCE_STANDARD' : sqltypes.VARCHAR
            , 'FEE_AT_RISK' : sqltypes.FLOAT
            , 'Estimated_Settlement_Amt' : sqltypes.FLOAT
            , 'LOAD_DATE' : sqltypes.DATE
            , 'APR_FLAG' : sqltypes.INTEGER
            , 'SUB_CNT' : sqltypes.INTEGER
            , 'Sub_Limit' : sqltypes.INTEGER
            , 'MBR_CNT' : sqltypes.INTEGER
            , 'Status' : sqltypes.VARCHAR
            , 'MBRSHP_HAS_UPDATE_YYYYMM' : sqltypes.VARCHAR
            , 'EDUCATED_RATE_IND' : sqltypes.INTEGER
            , 'HCC_RATE_IND' : sqltypes.INTEGER
            , 'BoB_Contr_Rate_Ind' : sqltypes.INTEGER
            , 'BoB_Contr_Survey_Ind' : sqltypes.INTEGER
            , 'BoB_Contr_Calnd_Ind' : sqltypes.INTEGER

        }
        
        with open(self.ddl_file_name,'r') as file:
            ddl_statemetns = file.readlines()

        row_count = 0
        for idx,sql in enumerate(ddl_statemetns):
            sql = re.sub(r'[^\x00-\x7f]',r'',sql) 
            try:
                execute_sql(sql)
                row_count +=1
                
            except Exception as e:
                self.show_error(f"Error appending data to Teradata: {e}")
                error_path = os.path.join(self.dirname,'errors.txt')
                with open(error_path,'a') as file:
                    file.write(sql)
        self.show_status(f"Sucessfully Appended {row_count} Rows into {input_table_name}")
    def disconnect_from_teradata(self):
        try:
            remove_context()
        except TD_exceptions.TeradataMlException:
            print('No Connection or Engine')
    
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVUploaderApp(root)
    root.mainloop()
