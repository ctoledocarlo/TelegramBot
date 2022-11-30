import os
from replit import db
import telebot

import csv
import time
import threading

from keepAlive import keep_alive
from scheduleParser import ScheduleParser

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

username = os.environ['BOT_USERNAME']
password = os.environ['BOT_PASSWORD']

reCommand = r"[A-Za-z]"

db["chatIDs"] = db['chatIDs']

db['commands'] = [
  'help', 'zoom', 'time', 'unlink',
  'confirmunlink', 'register', 'regme',
  'everyone', 'chatid'
]

db['commandDescription'] = [
  "BOT COMMANDS\n"
  "/help - retrieves the list of commands \n"
  "/register - Registers your ID to the database. \n"

  "\nSPECIFIC COMMANDS\n"
  "/zoom - sends the default zoom link \n"
  "/time - sends the current time \n"
	"/everyone - mentions everyone who is registered in the groupchat"
  "\nCommands are not case-sensitive"
]

db['adminCommands'] = [
		"adminregister", 'deletekey', 'deleteid', 'keys', 'properties', 'chatids'
]


def getTime():
	day = time.strftime("%A")
	hour = time.strftime("%H")
	minute = time.strftime("%M")
	sec = time.strftime("%S")

	return [day, hour, minute, sec]


def runSched():
	# chatID, message, repeat, date, hour, minute, peopleInvolved
	with open('schedules.csv', 'r') as schedules:
		fieldnames = ["chatID", "message", "repeat", "hour", "minute", "peopleInvolved"]
		dictReader = csv.DictReader(schedules, fieldnames=fieldnames)
	
		
		for row in dictReader:
			checkSched = ScheduleParser.checkSched(row=row)
			userRegistry = db[str(row['chatID'])]
			
			if checkSched:
				if row['peopleInvolved'] == 'everyone':
					everyone = ' '.join([f'@{user}' for user in userRegistry])
					update = row['message'].split('$')
					update = '\n\n'.join((update[0], update[1]))
					
					bot.send_message(row['chatID'], " ".join((everyone, update)))
					
				elif row['peopleInvolved'] != 'everyone':
					peopleInvolved = row['peopleInvolved'].split(" ")

					involved = ' '.join([f'@{username}' for username in peopleInvolved])
					update = row['message']
					
					bot.send_message(row['chatID'], " ".join((involved, update)))

	# print(ScheduleParser.readTime())
	# print(ScheduleParser.viewRaw(row))


def scheds():
	while True:
		runSched()

		time.sleep(60)
		

@bot.message_handler(regexp=reCommand)
def sendMessage(message):
	chatIDs = db['chatIDs']
	commands = db['commands']

	id = message.chat.id

	# Admin Commands
	if str(id) == "-884870438":
		messageTxt = message.text
		messageCommand = messageTxt.split(" ")[0][1:].lower()

		adminCommands = db['adminCommands']

		if messageCommand in adminCommands:
			
			if messageCommand == 'properties':
				bot.send_message(id, message)
			if messageCommand == 'chatids':
				bot.send_message(id, f'IDs Registered are {chatIDs}')
			if messageCommand == 'keys':
				print(db.keys())
	
			if '/deleteid' in messageTxt.split(" "):
				chatIDs.remove(int(messageTxt.split(" ")[1]))
				bot.send_message(id, f'Chat ID {messageTxt.split(" ")[1]} removed from the chatIDs list.')
	
			if '/deletekey' in messageTxt.split(" "):
				key = str(messageTxt.split(" ")[1])
				del db[key]
				bot.send_message(id, f'{key} has been removed from the database.')
	
			if '/adminregister' in messageTxt.split(" "):
						chatIDs.append(int(messageTxt.split(" ")[1]))	
						db[str(messageTxt.split(" ")[1])] = []
						print(db.keys())
				
						bot.send_message(id, f'Chat ID {messageTxt.split(" ")[1]} registered.')
				
						bot.send_message(int(messageTxt.split(" ")[1]), f'Chat ID {messageTxt.split(" ")[1]} registered. \n\nIt is recommended for everyone in this groupchat to register their usernames using "/register"')


	else:		
  	# Ensures that the chat ID is registered to the database
		if id in chatIDs:
			
			messageTxt = message.text
			messageCommand = messageTxt.split(" ")[0][1:].lower()
			timeNow = getTime()
	
			userRegistry = db[str(id)]
	
			if messageCommand not in commands:
				bot.send_message(id, 'Unknown Command')
	
	    # Bot Commands
			if messageCommand == 'help':
				bot.send_message(id, db["commandDescription"])
			if messageCommand == 'zoom':
				bot.send_message(id, 'banyuhay.ph/zoom')
			if messageCommand == 'time':
				bot.send_message(id, f"The time is {':'.join(timeNow[1:])}")
			if messageCommand == 'chatid':
				bot.send_message(id, f"This chat's ID is {id}")
	
	    # General Commands
			if messageCommand == 'everyone':
				bot.send_message(id, ' '.join([f'@{user}' for user in userRegistry]))
				
			if messageCommand == 'register':
				if message.from_user.username in userRegistry:
					bot.send_message(id, 'You are already registered.')
				else:
					userRegistry.append(message.from_user.username)
					bot.send_message(id, f'Thanks for registering @{message.from_user.username}!')
					
	
			if messageCommand == 'unlink':
				bot.send_message(id, "Are you sure? Every user registered within this chat will also be deleted from the bot's database. /confirmUnlink to unlink this chat."
	      )
			if messageCommand == 'confirmunlink':
				bot.send_message(id, f'Chat ID {id} removed. You may register again anytime.')
				chatIDs.remove(id)
				del db[str(id)]
				print(db.keys())
	
	  # If the chat ID is not registered to the database then...
		else:
			messageTxt = message.text
			messageCommand = messageTxt.split(" ")[0][1:].lower()
			
			if messageCommand == 'chatid':
				bot.send_message(id, f"This chat's ID is {id}")
			else:
				bot.send_message(id, "Register this chat's ID to continue.")


sched_check = threading.Thread(target=scheds)


sched_check.start()
keep_alive()
bot.infinity_polling()



# Currently, everything is working. I think it's ready to work on multiple
# groupchats. I just need to create the schedules feature and it's ready to deploy

# Nov 9 update. Scheduling does not work
