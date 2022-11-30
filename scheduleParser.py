import time
# import datetime


weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
workdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def getTime():
	day = str(time.strftime("%A"))
	# date = str(datetime.datetime.now().date())
	hour = str(time.strftime("%H"))
	minute = str(time.strftime("%M"))
	sec = str(time.strftime("%S"))

	return {"day": day, "hour": hour, "minute": minute, "sec": sec}


class ScheduleParser:

	def __init__(self):
		pass

	def checkSched(row):
		now = getTime()
		
		# chatID, message, repeat, date, hour, minute, peopleInvolved
		
		if row['repeat'] == 'daily':
			if now['hour'] == row['hour'] and now['minute'] == row['minute']:
				return True
			
		if row['repeat'] == 'every_week':
			if now['day'] == row['day'] and now['hour'] == row['hour'] and now['minute'] == row['minute']:
				return True
			
		if row['repeat'] == 'weekdays':
			if now['day'] in weekdays and now['hour'] == row['hour'] and now['minute'] == row['minute']:
				return True

		if row['repeat'] == 'workdays':
			if now['day'] in workdays and now['hour'] == row['hour'] and now['minute'] == row['minute']:
				return True

		return False

	
	def viewRaw(row):
		return dict(row)

	
	def readTime():
		now = getTime()
		return(f"{now['hour']}:{now['minute']}:{now['sec']}")

# Repeat commands: daily, every_week, weekdays
# Date command: MM/DD/YYYY
# hourMinute command: HH:MM
# People Involved: 'everyone', usernames




