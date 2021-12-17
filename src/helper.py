import sys
import os 
import re
import requests
import speedtest
from winreg import OpenKey,QueryValueEx,HKEY_CURRENT_USER

def edit_title(title):
	rmSpecial = re.sub("[\"<>:*?|/]", "", title)
	rmBackslash = rmSpecial.replace("\\", "")
	title = rmBackslash.replace(" ", "_")
	return title

def ffmpeg_format(file):
	return f'\"{file}\"'

def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.dirname(__file__)
	return os.path.join(base_path, relative_path)

def get_default_path():
	with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders') as key:
		Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
	return Downloads

def check_connection():
	connection = 1
	url = "http://www.youtube.com"
	try:
		res = requests.get(url)
		connection = 1
	except:
		connection = 0
	finally:
		return connection

# Return mbit speed for the pc
def get_internet_speed():
	speed_test = speedtest.Speedtest()
	speed = speed_test.download()
	megabit = (speed*(9.537*(10**(-7))))
	return int(megabit)

def get_estimate_time(speed,filesize):
	size = filesize * (7.6294*(10**-6)) + 20.0
	estimate_time = (size / speed)
	return estimate_time