# import sqlite3
# import pandas as pd
# import numpy as np

# from random import choice
# conn = sqlite3.connect('assets/DashTemp.db')
# c = conn.cursor()

# sql = "select * from RESERVATION"

# df = pd.read_sql(sql,conn)
# print(df)

# conn.commit()
# conn.close()

import sqlite3
import pandas as pd
import numpy as np

from random import choice
conn = sqlite3.connect('assets/DashTemp.db')
c = conn.cursor()


# c.execute('''CREATE TABLE REVIEW
#        (ID INT PRIMARY KEY NOT NULL,
#        REVIEW           TEXT,
#        TIME        CHAR(50),
#        SENTIMENT         INT);''')

sql = "select * from ASPECT"

df = pd.read_sql(sql,conn)
print(df)

conn.commit()
conn.close()

