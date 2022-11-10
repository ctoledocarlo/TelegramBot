import time
import datetime


def getTime():
	dateToday = datetime.date.today
	day = time.strftime("%A")
	hour = time.strftime("%H")
	minute = time.strftime("%M")
	sec = time.strftime("%S")

	return {"date" : datetime.date(dateToday), "day": day, "hour": hour, "minute": minute, "sec": sec}


class ScheduleParser:

	def __init__(self):
		pass

	def checkSched(row):
		now = getTime()

		print(str(now['date']))

		return False

	def viewRaw(row):
		return dict(row)


# Repeat commands: once, daily, every_week, weekdays
# Date command: MM/DD/YYYY
# hourMinute command: HH:MM
# People Involved: 'everyone', usernames





# Currently cannot access dates using MM/DD/YYYY format. Tried time and datetime modules
