# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 11:54:53 2020

@author: chest
"""

import json
import requests
import time
import speech_recognition as sr
import subprocess
import os
import pyttsx3
from pydub import AudioSegment

#remember to change directory
os.chdir(r"C:\Users\chest\Desktop\Projects\Restaurant Chatbot\voices")

#PROTOTYPE FOR THE PROJECT
#   This is only a prototype to prove that speech input and speech output work well for the telegram
#   Logic to handle multiple users on the platform has not been done


#bot information
#replace with ur bot_token 
bot_token = "1029318260:AAGUCvEBcKPAFD3Ef7leXV48iEv27qL2WkA"
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

#to get the voice message (My testing done based on last chat..Last Chat must be microphone)
#   Here we are using the microphone of the telegram platform

def get_voiceID(update):
    if 'voice' in update["result"][-1]["message"].keys():
        file_id = update["result"][-1]["message"]["voice"]["file_id"]
        unique_id = update["result"][-1]["message"]["voice"]["file_unique_id"]
    return (file_id, unique_id)

def get_voicePath(voiceID):
    url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={voiceID}"
    response = requests.get(url)
    content = response.content.decode("utf8")
    content_js = json.loads(content)
    return content_js

def get_voiceFile(voice_path, unique_id):
    url = f"https://api.telegram.org/file/bot{bot_token}/{voice_path}"
    response = requests.get(url, allow_redirects=True)
    oga_file = "voice{}.oga".format(unique_id)
    wav_file = "voice{}.wav".format(unique_id)
    with open(oga_file, 'wb') as file:
        file.write(response.content)
    # process = subprocess.run(['ffmpeg', '-i', filename, wav_file]) #make sure u have ffmpeg installed in ur environment
    command = f'ffmpeg -i {oga_file} {wav_file}'
    process = subprocess.call(command) 
    if process == 0:
        os.remove(oga_file)
    else:
        print("Audio Conversion Error")
    return (wav_file, url)

def send_reply(reply, chat_id="427241602"):
    reply_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={reply}"
    response = requests.get(reply_url)
    content = response.content.decode("utf8")
    content_js = json.loads(content)
    return content_js

def welcome_message(message):
    updates = get_url("getUpdates")
    for update in updates["result"]:
        text = update["message"]["text"]
        if text == "/start":
            reply = send_reply(message, update["message"]["chat"]["id"])
            print(reply)

def sendAudio(chat_id, voice_file, reply_id=None):
    post_url = f"https://api.telegram.org/bot{bot_token}/sendAudio?chat_id={chat_id}"
    files = {'audio':open(voice_file, 'rb')}
    status = requests.post(post_url, files=files)
    content = status.content.decode("utf8")
    content_js = json.loads(content)
    # params = {"chat_id":chat_id, "voice":voice, "reply_to_message_id":reply_id}
    # response = requests.get(url, params=params)
    # content = response.content.decode("utf8")
    # content_js = json.loads(content)
    return content_js

# def sendAudio(chat_id, voice_id, reply_id=None):
#     url = f"https://api.telegram.org/bot{bot_token}/sendVoice"
#     params = {"chat_id":chat_id, "voice":str(voice_id), "reply_to_message_id":reply_id}
#     response = requests.get(url, params=params)
#     content = response.content.decode("utf8")
#     content_js = json.loads(content)
#     return content_js
# sent = sendAudio(chat_id="147255755", voice_id=file_id, reply_id="14")


#initiate with welcome message
message = "I am here to annoy you. Please speak to the microphone and say something."
welcome_message(message)

#the code after this is in relation to speech recognition homework

test = get_url("getUpdates")
voice_ids = get_voiceID(test)
voice_path = get_voicePath(voice_ids[0])["result"]["file_path"]
voice = get_voiceFile(voice_path, voice_ids[1])

r = sr.Recognizer()
with sr.AudioFile(voice[0]) as source:
    # listen for the data (load audio to memory)
    audio = r.record(source)
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    captured_word = r.recognize_google(audio)

#output speech to annoy the person
engine = pyttsx3.init()
engine.setProperty('rate', 50)
annoying_text = f"Did you just sayyy {captured_word}"
engine.save_to_file(annoying_text, "AnnoyingReply.wav")
engine.runAndWait()
engine.stop()

# subprocess.run(["ffmpeg", '-i', audio_path_wav, '-acodec', 'libopus', audio_path_ogg, '-y'])

command = 'ffmpeg -i AnnoyingReply.wav -acodec libopus AnnoyingReply.ogg -y'
process = subprocess.call(command) 
if process == 0:
    os.remove("AnnoyingReply.wav")
else:
    print("Audio Conversion Error")
    
# voiceAgAD-AADcD-wVQ.wav
#Rely on Telegram module to perform send voice
file_info = sendAudio(chat_id="943184853", voice_file="AnnoyingReply.ogg")
file_id = "AwACAgUAAxkDAAMXXjWszjKl08R7knIJvUAMwS1KgcQAAvwAA3A_sFWORdgltRt8yBgE"


 
# sendAudio(chat_id="427241602", voice_file="AnnoyingReply.oga", reply_id="11")





