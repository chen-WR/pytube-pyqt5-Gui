import sys
import os 
import re

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