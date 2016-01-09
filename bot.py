import time
import telepot
import json
import sys

# TOKEN = sys.argv[1]
TOKEN = '118865412:AAG8iNbj0NTQxyfSjhhoITNplHNP3_1x1Sg'
RUNNING = {}

with open('data.json', 'r') as fp:
    stickerTriggers = json.load(fp)

bot = telepot.Bot(TOKEN)
BOTNAME = bot.getMe()['username']

def saveJson(data):
 with open('data.json', 'w') as fp:
  json.dump(data, fp)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance2(msg)

    if chat_id not in RUNNING:
        RUNNING[chat_id] = True
    
    print ""
    print msg
    print ""
    if content_type == "text":
     text = msg['text'].lower()
     if chat_type == "private" and "reply_to_message" in msg and "sticker_id: " in msg["reply_to_message"]["text"]:
     	file_id = msg["reply_to_message"]["text"].split()[-1]
     	for dict in stickerTriggers:
      	 if dict["trigger"] in text:
     		bot.sendMessage(chat_id, "Oops. \"" + dict["trigger"]+ "\" is already in use for the sticker: ")
     		bot.sendSticker(chat_id, dict["file_id"])
     		return
     	stickerTriggers.append({"file_id": file_id, "trigger":text + " ", "creator":msg['from']})
        saveJson(stickerTriggers)
    	bot.sendMessage(chat_id, "trigger: \"" + text + "\" added for sticker:")
     	bot.sendSticker(chat_id, file_id)
     elif text == "/list":
     	triggers = "Available triggers:\n \n"
     	for dict in stickerTriggers:
     		triggers += dict["trigger"] + "\n"
        triggers += " \nYou can add more triggers by sending @" + BOTNAME + " a sticker in a private message"
     	bot.sendMessage(chat_id, triggers)
     elif text == "/stop" or text == "/shutup":
        bot.sendMessage(chat_id, "Shutting up")
        RUNNING[chat_id] = False
     elif text == "/start":
        bot.sendMessage(chat_id, "Stickers enabled")
        RUNNING[chat_id] = True
     elif text == "/help" or "@"+BOTNAME.lower() in text:
        if RUNNING[chat_id] == False:
            bot.sendMessage(chat_id, "I've been silenced. Enable me again by typing \"/start\"")
     	bot.sendMessage(chat_id, "You can add sticker triggers by sending @" + BOTNAME + " a sticker in a private message")
     elif RUNNING[chat_id]:
      for dict in stickerTriggers:
      	if dict["trigger"] in text:
      		bot.sendSticker(chat_id, dict["file_id"])
    elif chat_type == "private" and content_type == "sticker":
      bot.sendMessage(chat_id, "reply the trigger word to the following message:")
      bot.sendMessage(chat_id, "sticker_id: " + msg['sticker']['file_id'])

print BOTNAME + " is now running"
bot.notifyOnMessage(handle)
# Keep the program running.
while 1:
    time.sleep(10)