import sqlite3

conn = sqlite3.connect('assets\DashTemp.db')

c = conn.cursor()
c.execute('''CREATE TABLE if not EXISTS RESERVATION
       (ID INT PRIMARY KEY NOT NULL,
       NAME           TEXT,
       TABLES            INT,
       TIME        CHAR(50),
       PEOPLE         INT);''')

c.execute('''CREATE TABLE if not EXISTS REVIEW
       (ID INT PRIMARY KEY NOT NULL,
       REVIEW           TEXT,
       TIME        CHAR(50),
       SENTIMENT         INT);''')

c.execute('''CREATE TABLE if not EXISTS ASPECT
       (ID INT PRIMARY KEY NOT NULL,
       REVIEW_ID           INT,
       ASPECT        CHAR(50),
       SENTIMENT         INT);''')

c.execute('''CREATE TABLE if not EXISTS DAY
       (ID INT PRIMARY KEY NOT NULL,
       TIME        CHAR(50),
       RATE           INT,
       POS_REVIEW        INT,
       NEG_REVIEW         INT,
       PEOPLE         INT);''')


conn.commit()
conn.close()