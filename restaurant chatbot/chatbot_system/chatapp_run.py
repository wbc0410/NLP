# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 15:52:37 2020

@author: chest
"""

#set your directory to where the function codes are
from os import chdir
chdir(r"C:\Users\chest\Desktop\Projects\Restaurant Chatbot\chatbot_system\assets")

# Self-package
from RestaurantTelegram import *
from  TelegramDB import * #DB Connection established with import #connection = conn


import sqlite3
import pandas as pd
from sqlite3 import Error
from time import sleep

# As this is a prototype, we will use sqlite3. 
# Actual production will be on a more secured database

bot = telegramBot("1032172824:AAEsCGdpFpQldr25WYmHCbqu8Q2MRxCCMcA")

#functions for the process flow
def welcome_message(bot, chat_id):
    message = "Hi, I am the tasty assistant. Please choose from the following options below. Type tastyassist to return to main menu."
    option_list = ["Leave a review", "Reservations", "Other Questions"]
    options = bot.build_options(option_list)
    reply = bot.send_options(message, chat_id, options)

def review_respond(bot, chat_id):
    reply = "Please let us know what you think about our restaurant."
    bot.send_reply(reply, chat_id)

def reservation_respond(bot, chat_id):
    reply = "Please tell us the date and time u would like to visit in the following format(eg;DD-MM-YY HH:MM)."
    bot.send_reply(reply, chat_id)


# while True:
#Telegram API requests
while True:
    try:
        last_updateID = bot.get_lastUpdate() + 1
        batch_update = bot.getUpdates()
        bot.getUpdates(last_updateID)
        TelegramDF = telegramDF(batch_update)
        temp_df = TelegramDF.getDataFrame()
        
        # Database connection part
        telegramDBT = DBTransform(conn, temp_df)
        telegramDBT.uploadWhole()
        telegramDBT.createCustTable()
        try:
            telegramDBT.getReview()
        except:
            pass
        # To do chatflow
        for ind, row in temp_df.iterrows():
            #Process Flow 1
            if row.message == "/start":        
                chat_id = row.sender_id
                welcome_message(bot, chat_id)
            if  row.message == "Leave a review":
                chat_id = row.sender_id
                review_respond(bot, chat_id)
            if row.message == "Reservations":
                chat_id = row.sender_id
                reservation_respond(bot, chat_id)
    except:
        sleep(1)
        pass

            

    
        
#     if row.message == "Reservations":


test = pd.read_sql("SELECT * FROM ReviewTable", conn, index_col=None)



# temp_df.to_sql('masterChat', conn, if_exists='append', index=False)