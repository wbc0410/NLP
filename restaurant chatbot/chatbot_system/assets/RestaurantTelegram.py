# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 15:54:33 2020

@author: chest
"""

#runs on python 3

import json
import requests
import time
import pandas as pd

class telegramBot:
    
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}/"
        
    def get_url(self, command, offset=None):
        # this is flexible method which is like a general get request call
        # however, we mainly use to  do getUpdates 
        base_url = self.base_url
        url = base_url + command 
        if command == "getUpdates":
            url = f"{url}?offset={offset}"
        response = requests.get(url)
        content = response.content.decode("utf8")
        content_js = json.loads(content)
        return content_js

    def get_lastUpdate(self):
        url = self.base_url + "getUpdates"
        response = requests.get(url)
        content = response.content.decode("utf8")
        content_js = json.loads(content)
        results = content_js["result"]
        last_id = results[-1]["update_id"]
        return last_id
    
    def getUpdates(self, offset=None):
        url = self.base_url + "getUpdates"
        if bool(offset):
            url = url + f"?offset={offset}"
        response = requests.get(url)
        content = response.content.decode("utf8")
        content_js = json.loads(content)
        results = content_js["result"]
        return results
        
    def send_reply(self, reply, chat_id):
        # reply is the reply that you would like to send to the person
        bot_token = self.bot_token
        reply_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={reply}"
        response = requests.get(reply_url)
        content = response.content.decode("utf8")
        content_js = json.loads(content)
        return content_js
                
    @staticmethod
    def build_options(items):
        #Example of items: ["Leave a review", "Talk to me", "Reservations"]
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)
    
    def send_options(self, reply, chat_id, options):
        # reply here should be in the form of a keyboard 
        # This is different from send_reply as it gives people an option to choose
        # options = output of build_options 
        base_url = self.base_url
        url = base_url + f"sendMessage?text={reply}&chat_id={chat_id}&parse_mode=Markdown&reply_markup={options}"
        response = requests.get(url)
        content = response.content.decode("utf8")
        content_js = json.loads(content)
        return content_js
    
    def delete_message(self, chat_id, message_id):
        # this is to allow merchants to retract certain messages 
        base_url = self.base_url
        delete_url = base_url + f"deleteMessage?chat_id={chat_id}&message_id={message_id}"
        response = requests.get(delete_url)
        content = response.content.decode("utf8")
        content_js = json.loads(content)
        return content_js
    
    # to convert content_js into dataframe
    
class telegramDF:

    def __init__(self, result_list):
        self.results = result_list
        
    def check_text(self, msg_dict):
        # to determine if this is a text message
        if "text" in msg_dict.keys():
            text = msg_dict["text"]
        else:
            text = ""
        return text
    
    def check_voice(self, msg_dict):
        # to determine if this is a voice message
        if "voice" in msg_dict.keys():
            voice_dict = msg_dict["voice"]
        else:
            voice_dict = {"duration":0, "mime_type":"",
                          "file_id":"", "file_unique_id":"",
                          "file_size":0}
        return voice_dict
        
    def getDataFrame(self):
        # Transform dictionary into dataframe
        results = self.results
        list_of_result = []
        for result in results:
            update_id = result["update_id"]
            msg = result["message"]
            text = self.check_text(msg)
            voice = self.check_voice(msg)
            result_dict = {"update_id":update_id, "message_id":msg["message_id"], 
                           "date":msg["date"], "message":text}
            #to take in sender details
            sender = msg["from"]
            sender_id = sender.pop("id")
            sender["sender_id"] = sender_id
            result_dict.update(sender)
            result_dict.update(voice)
            list_of_result.append(result_dict)
        df = pd.DataFrame(list_of_result)
        df["Responded"] = False
        return df

        
    

