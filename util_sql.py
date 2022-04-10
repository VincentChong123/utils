"""
this is a utility class to encapsulate SQLite command
"""
# %%
import cmd
import sqlite3
import logging
import os
from matplotlib.pyplot import table 
import pandas as pd

logger = logging.getLogger(__name__)
FORMAT = "%(levelname)s [%(filename)s:%(lineno)s - %(funcName)15s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

class Sqlcmd():    
    def __init__(self, dbpath=""):
        super(Sqlcmd, self).__init__()
        logger.info(f"Input dbpath is \"{dbpath}\"")
        assert len(dbpath), print(f"Input dbpath is invalid")
        self.connection = sqlite3.connect(dbpath)
        self.cursor = self.connection.cursor()
        self.col_name_dtype = ""
        self.dbpath=dbpath
        self.query = None
        self.dtype_dict = {
            "text": "text",
            "str": "text",
            "int" : "int",
            "real": "real",
            "float": "real",
            "null": "null",
            "blob": "blob"
        }        

    def insert_col_header(self, header="", dtype=""):
        if len(header) and len(dtype):
            datatype=self.dtype_dict[dtype]
            self.col_name_dtype += f"{header} {datatype},"
        else:
            logger.error("invalid header or dtype")
        
        logger.info(f"{len(self.col_name_dtype.split(','))} {self.col_name_dtype} ")

    def execute(self, cmd):
        logger.info(f"cmd {cmd}")
        self.cursor.execute(cmd)

    def create(self, table = ""):
        cmd = f"CREATE TABLE {table} ({self.col_name_dtype[:-1]})"
        self.execute(cmd)
                
    def get_col_info(self):
        logger.info(f"{self.col_name_dtype}")
        return self.col_name_dtype

    def insert(self, table = "", values = ""):        
        cmd = f"INSERT INTO {table} VALUES ({values})"
        self.execute(cmd)

    def get_total_changes(self):        
        logger.info(f"total_changes = {self.connection.total_changes}")
        return self.connection.total_changes

    def commit(self):
        logger.info("commit")
        self.connection.commit()

    def close(self):
        logger.info("close")
        self.connection.close()
    
    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor
    
    def db2df(self, table=""):
        df=pd.read_sql_query(f"SELECT * from {table}", self.connection) 
        return df
    
    # def query2df(self):
    #     if self.query != None:
    #         df = pd.DataFrame.from_records(data=self.cursor.fetchall(), 
    #         columns=self.query.description)
    #         return df
    #     else:
    #         logger.error("query is empty, please execute select query first!")
        
    def delete(self, table="", condition=""):
        cmd = f"DELETE FROM {table} WHERE {condition}"
        self.execute(cmd)

    def select(self, table="", header="*", condition=""):
        cmd = f"SELECT {header} FROM {table}"
        if len(condition):
            cmd += f" WHERE {condition}"            

        self.query = self.cursor.execute(cmd)

        return self.cursor.fetchall()

if __name__ == "__main__":
    print(__file__)

    dbpath = "sqlcmd.db"
    if os.path.exists(dbpath):
        os.remove(dbpath)
        logger.info(f"deleted existing {dbpath}")

    sqlcmd = Sqlcmd(dbpath)
    con = sqlcmd.get_connection()
    # logger.info(f"get_connection {con} {type(con)}")

    #------------------------------------------------------
    sample_col_name = ["first_name", "last_name", "email_address"]
    sample_type = ["text", "text", "text"]

    # cmd_create = ""
    # for t, name in enumerate(sample_col_name):
    #     cmd_create += f"{name} {sample_type[t]}"
    #     if t < (len(sample_col_name)-1):
    #         cmd_create += ","
    # #------------------------------------------------------
    table_name = "customer_table"    
    # logger.info(f"cmd_create {cmd_create} {list((cmd_create,))}")
    # sqlcmd.create(table=table_name, col_name_dtype=cmd_create)
    
    for t,_ in enumerate(sample_col_name):
        sqlcmd.insert_col_header(header=sample_col_name[t], dtype=sample_type[t])
    
    sqlcmd.create(table=table_name)
    sqlcmd.get_col_info()
    sqlcmd.insert(table=table_name, values="'first1', 'last1', '1@g.com'")
    sqlcmd.insert(table=table_name, values="'first2', 'last2', '2@g.com'")
    sqlcmd.insert(table=table_name, values="'first3', 'last3', '3@g.com'")
    sqlcmd.get_total_changes()
    df = sqlcmd.db2df(table=table_name)
    print(df.head())

    rows = sqlcmd.select(table=table_name, header="*")
    for t,r in enumerate(rows):
        print(t, r)
    
    # %%
    # df = sqlcmd.query2df()
    # print(df.head())
    # %%
    rows = sqlcmd.select(table=table_name, 
                        header="first_name, last_name", 
                        condition="email_address == '1@g.com'")
    for t,r in enumerate(rows):
        print(t, r)
# %%
    # df = self.query2df()
    # print(df.head())

# # %%
#     print(sqlcmd.db2df(table=table_name).head())
#     sqlcmd.delete(table=table_name, condition="email_address == '1@g.com'")
#     sqlcmd.commit()
#     print(sqlcmd.db2df(table=table_name).head())

# %%
    sqlcmd.close()