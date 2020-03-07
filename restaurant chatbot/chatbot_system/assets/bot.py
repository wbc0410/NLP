# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 11:54:53 2020

@author: chest
"""

import json
import requests
import time
import telegram


#bot information
bot_token = "1032172824:AAEsCGdpFpQldr25WYmHCbqu8Q2MRxCCMcA"
base_url = f"https://api.telegram.org/bot{bot_token}/"
 # getUpdates

#telegram functions
#the commands available <getme, getUpdates
#base function to call commands
def get_url(command, offset=None):
    url = base_url + command 
    if command == "getUpdates":
        url = f"{url}?offset={offset}"
    response = requests.get(url)
    content = response.content.decode("utf8")
    content_js = json.loads(content)
    return content_js

#to send message to our customer
def send_reply(reply, chat_id="427241602"):
    reply_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={reply}"
    response = requests.get(reply_url)
    content = response.content.decode("utf8")
    content_js = json.loads(content)
    return content_js

def send_options(reply, chat_id="427241602", reply_markup=None):
    url = base_url + f"sendMessage?text={reply}&chat_id={chat_id}&parse_mode=Markdown&reply_markup={reply_markup}"
    response = requests.get(url)
    content = response.content.decode("utf8")
    content_js = json.loads(content)
    return content_js

#delete message
def delete_message(chat_id, message_id):
    delete_url = base_url + f"deleteMessage?chat_id={chat_id}&message_id={message_id}"
    response = requests.get(delete_url)
    content = response.content.decode("utf8")
    content_js = json.loads(content)
    return content_js

#get the last message we sent out
    #NOTE: TELEGRAM ONLY KEEP UPDATES FOR 24 hours

def build_options(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def welcome_message(message):
    updates = get_url("getUpdates")
    for update in updates["result"]:
        text = update["message"]["text"]
        if text == "/start":
            reply = send_options(message, update["message"]["chat"]["id"], options)
            print(reply)

def welcome_message2(message):
    updates = get_url("getUpdates")
    for update in updates["result"]:
        text = update["message"]["text"]
        if text == "Tasty Yelp":
            reply = send_options(message, update["message"]["chat"]["id"], options)
            print(reply)

def reply_reservation():
    updates = get_url("getUpdates")
    for update in updates["result"]:
        if update["message"]["text"] == "Reservations":
            message = "Please input your date and time in the following format..(eg; DDMMYYYY HHMM pm/am"
            reply = send_reply(message, update["message"]["chat"]["id"])
            print(reply)

def reservation_confirmation(chat_id):
    message = "Thank you for choosing our restaurant. Your reservation has been confirmed. Ticket Number 888."
    reply = send_reply(message, chat_id)
    print(reply)

        
def reply_review():
    updates = get_url("getUpdates")
    for update in updates["result"]:
        if update["message"]["text"] == "Leave a review":
            message = "Please share with me your thoughts on our restaurant?"
            reply = send_reply(message, update["message"]["chat"]["id"])
            print(reply)

def talk_tasty():
    updates = get_url("getUpdates")
    for update in updates["result"]:
        if update["message"]["text"] == "Talk to me":
            message = "Feel free to ask me any questions relating to our restaurants."
            reply = send_reply(message, update["message"]["chat"]["id"])
            print(reply)


message2 = "I hope you like your chat with me so far. How can I help?"
option_list = ["Leave a review", "Talk to me", "Reservations"]
options = build_options(option_list)
welcome_message(message)
reply_review()
reply_reservation()
reservation_confirmation("427241602")
option_list = ["Leave a review", "Talk to me", "Reservations"]
options = build_options(option_list)
welcome_message2(message2)
talk_tasty()
