# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 16:29:04 2020

@author: chest
"""

import sqlite3
import pandas as pd
from sqlite3 import Error

# to keep things simple as this is only prototype
# the datastructure and relations are kept simple. Actual production will be more complicated

from os import chdir
chdir(r"C:\Users\chest\Desktop\Projects\Restaurant Chatbot\chatbot_system\assets")

def create_connection(db_file):
    """ create a database connection to a database that resides
        in the memory
        ram: ':memory:'
        file: file_path
    """
    conn = None;
    try:
        conn = sqlite3.connect(db_file) #change to ram / memory
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

db_name = "restaurant_sample.db"
create_connection(db_name)
conn = sqlite3.connect(db_name)

class DBTransform():
    
    def __init__(self, conn, df):
        self.connection = conn
        self.df = df
    
    def uploadWhole(self):
        df = self.df
        conn = self.connection
        df = df.drop(columns=["Responded"])
        df.to_sql('masterChat', conn, if_exists='append', index=False)
   
    def createCustTable(self):
        df = self.df
        conn = self.connection
        sender_ids = list(df["sender_id"].unique())
        for sender_id in sender_ids:
            table_name = f"table_{sender_id}"
            sender_table = df[df["sender_id"] == sender_id]
            sender_table.to_sql(table_name, conn, if_exists="append", index=False)
    
    def getReview(self):
        df = self.df
        conn = self.connection
        sender_ids = list(df["sender_id"].unique())
        schema = {'update_id': int, # schema needed as dtypes lost after transpose
                  'message_id': int,
                  'date': int,
                  'message': str,
                  'is_bot': bool,
                  'first_name': str,
                  'last_name': str,
                  'language_code': str,
                  'sender_id': int,
                  'duration': int,
                  'mime_type': str,
                  'file_id': str,
                  'file_unique_id': str,
                  'file_size': int,
                  'Responded': bool}
        for sender_id in sender_ids:
            sql_query = f"SELECT * FROM table_{sender_id}"
            cust_table = pd.read_sql(sql_query, conn)
            responded_ind = list(cust_table.index[cust_table["Responded"] == 0])
            max_row = cust_table.shape[0] 
            for responded_no in range(len(responded_ind)):
                ind = responded_ind[responded_no]
                if cust_table.loc[ind, "message"] == "Leave a review":
                    next_ind = responded_no + 1
                    if next_ind < max_row:
                        cust_table.loc[next_ind, "Responded"] = 1
                        cust_table.loc[ind, "Responded"] = 1
                        review = cust_table.iloc[next_ind, :]
                        review = review.to_frame().T
                        review = review.astype(schema) #Needed as object type is bad
                        review.to_sql("ReviewTable", conn, if_exists="append", index=False)
                        cust_table.to_sql(f"table_{sender_id}", conn, if_exists="replace", index=False)
                        
                


# Codes to create table, might not be used depending on approach
# Create table (we try to use integer instead of text to save space)
# def create_table(conn, create_table_sql):
#     """ create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement
#     :return:
#     """
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)
# sql_create_table_dailyChat = """ CREATE TABLE IF NOT EXISTS dailyChat (
#                                     update_id integer PRIMARY KEY,
#                                     msg_id integer NOT NULL,
#                                     from_id integer NOT NULL,
#                                     first_name text NOT NULL,
#                                     last_name text NOT NULL,
#                                     language text NOT NULL,
#                                     msg_type text NOT NULL,
#                                     date integer NOT NULL,
#                                     voice bool NOT NULL,
#                                     mime_type text,
#                                     file_id text,
#                                     file_unique_id text,
#                                     file_size interger
#                                 ); """

# sql_create_table_overallChat = """ CREATE TABLE IF NOT EXISTS overallChat (
#                                     update_id integer PRIMARY KEY,
#                                     msg_id integer NOT NULL,
#                                     from_id integer NOT NULL,
#                                     first_name text NOT NULL,
#                                     last_name text NOT NULL,
#                                     language text NOT NULL,
#                                     msg_type text NOT NULL,
#                                     date integer NOT NULL,
#                                     voice bool NOT NULL,
#                                     mime_type text,
#                                     file_id text,
#                                     file_unique_id text,
#                                     file_size interger
#                                 ); """
# create_table(conn, sql_create_table_dailyChat)
# create_table(conn, sql_create_table_overallChat)

