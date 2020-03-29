
import sqlite3
import pandas as pd
import numpy as np
##################################################
#reservation
###############################################3


from random import choice
from random import sample



# listTime = [x.strftime("%Y-%m-%d %H:%M") for x in pd.period_range(start="2020-03-28 12:00", end="2020-05-25 18:00", freq = "6h")]
# listTime = list(filter(        (lambda x: (x.find("06:00")<0)&(x.find("00:00")<0)&(x.find("08:00")<0)  ),listTime))
# conn = sqlite3.connect('assets/DashTemp.db')
# c = conn.cursor()


# tables_list = list(np.random.randint(low=1, high=10, size=len(listTime)))

# nameList = ["Lee","Chou","Kate","Dan","Ellet","Sam","Mr. Zhang","Mr. Rutledge","Mr. Sabine","Mr. Kate","Mr. Dan","Mr. Ellet","Mr. Sam","Mr. Zhang",
#                             "Mansfield","Maple","Balfe","Bale","Alpert","Alphonsus","Mr. Zhang","Lee","Chou","Kate","Dan"]

# random_select = [1,2,3,4,5,6,7,8,9,10]

# people = [1,2,3,4]
# #随机一下每天每个时段的订单数
# n = 0
# for index,time in enumerate(listTime):
#     tableID = sample(random_select,tables_list[index])
#     for tablenum in tableID:
#         #tablenum
#         #time
#         n = n+1
#         c.execute(f"INSERT INTO RESERVATION (ID,NAME,TABLES,TIME,PEOPLE) \
#             VALUES ({n}, '{choice(nameList)}', {tablenum}, '{time}', {choice(people)} )")


# conn.commit()
# conn.close()
#########################################################################
#review
########################################################################

# import pickle as pk



# with open("reviewfordatabase.pkl","rb")as input:
#     df_review = pk.load(input)


# conn = sqlite3.connect('assets/DashTemp.db')
# c = conn.cursor()

# # c.execute('''CREATE TABLE REVIEW
# #        (ID INT PRIMARY KEY NOT NULL,
# #        REVIEW           TEXT,
# #        TIME        CHAR(50),
# #        SENTIMENT         INT);''')

# for n,index in enumerate(df_review.index):
#     n = n+1
#     review = df_review['text'].loc[index]
#     date = str(df_review['date'].loc[index])
#     sentiment = 1 if df_review['stars'].loc[index]>2 else -1
#     sql_l = f"INSERT INTO REVIEW (ID,REVIEW,TIME,SENTIMENT) \
#             VALUES (?,?,?,?)"
#     c.execute(sql_l,(n,review,date,sentiment))



# conn.commit()
# conn.close()


################################################################
#aspect

#############################################################

# c.execute('''CREATE TABLE ASPECT
#        (ID INT PRIMARY KEY NOT NULL,
#        REVIEW_ID           INT,
#        ASPECT        CHAR(50),
#        SENTIMENT         INT);''')

#读取

import sqlite3
import pandas as pd
import numpy as np

from random import choice
# conn = sqlite3.connect('assets/DashTemp.db')
# c = conn.cursor()

import nltk

from nltk.tokenize import sent_tokenize
 

from datetime import datetime as dt
conn = sqlite3.connect('assets/DashTemp.db')
c = conn.cursor()

sql = "delete from ASPECT"
c.execute(sql)


sql = "select * from REVIEW"

df = pd.read_sql(sql,conn)


apect_list = ["Food", "Service", "Price", "Anecdotes","Ambience"]
sen = [1,-1,1,1,1,1]
n = 0
for index in df.index:
    reviewid = int(df["ID"].loc[index])
    document=df["REVIEW"].loc[index]
    sentences=sent_tokenize(document)
    for i in range(len(sentences)):
        id = n
        
        aspect = choice(apect_list)
        SENTIMENT = choice(sen)
        sql_l = f"INSERT INTO ASPECT (ID,REVIEW_ID,ASPECT,SENTIMENT) \
             VALUES (?,?,?,?)"
        c.execute(sql_l,(id,reviewid,aspect,SENTIMENT))
        n = n+1
conn.commit()
conn.close()

################################################################################################
#day
###############################################################################################


# sql = "delete from day"
# c.execute(sql)


# sql = "select * from REVIEW"
# df_review = pd.read_sql(sql,conn)

# sql = "select * from ASPECT"
# df_aspect = pd.read_sql(sql,conn)

"""
c.execute('''CREATE TABLE if not EXISTS DAY
       (ID INT PRIMARY KEY NOT NULL,
       TIME        CHAR(50),
       RATE           INT,
       POS_REVIEW        INT,
       NEG_REVIEW         INT,
       PEOPLE         INT);''')
"""

# peoplelist = list(range(100,200))

# df_review["year"] = pd.to_datetime(df_review["TIME"]).dt.year
# df_review["month"] = pd.to_datetime(df_review["TIME"]).dt.month
# df_review["day"] = pd.to_datetime(df_review["TIME"]).dt.day

# df_senti = df_review.groupby(["year","month","day","SENTIMENT"],as_index=False).count()

# n = 0
# for index in df_senti.index:
#     if index%2 == 0:
#         n = n+1

#         time = str(df_senti['year'].loc[index]) + "-"  + (str(df_senti['month'].loc[index]) if df_senti['month'].loc[index]>9 else ("0" + str(df_senti['month'].loc[index])))+ "-" + (str(df_senti['day'].loc[index]) if df_senti['day'].loc[index]>9 else ("0" + str(df_senti['day'].loc[index])))


#         NEG_REVIEW = int(df_senti["ID"].loc[index])
#         POS_REVIEW = int(df_senti["ID"].loc[index+1])
#         RATE = POS_REVIEW/(POS_REVIEW + NEG_REVIEW)
#         sql_l = f"Insert INTO DAY (ID,TIME,RATE,POS_REVIEW,NEG_REVIEW,PEOPLE) \
#              VALUES (?,?,?,?,?,?)"
#         c.execute(sql_l,(n,time,RATE,POS_REVIEW,NEG_REVIEW,choice(peoplelist)))

    

# # (df_review["date"].min(),dt.today())

# conn.commit()
# conn.close()



