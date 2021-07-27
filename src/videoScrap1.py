"""
01/02/2021
C.W.R.
YouTube Video Downloader
"""

from pytube import Playlist
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import re

class Tab:
	def __init__(self, keyword=None, maxVideo=None):
		self.list = []
		self.keyword = keyword
		self.maxVideo = maxVideo

	def resource_path(self, relative_path):
	    try:
	        base_path = sys._MEIPASS
	    except Exception:
	        base_path = os.path.dirname(__file__)
	    return os.path.join(base_path, relative_path)

	def driverInit(self):
		self.option = webdriver.ChromeOptions()
		self.option.add_argument("headless")
		self.driver = webdriver.Chrome(executable_path=self.resource_path('./binary/chromedriver.exe'),options=self.option)
		# self.driver.maximize_window()

	def searchDriver(self):
		self.driverInit()
		self.driver.get("http://www.youtube.com/")
		search = self.driver.find_element_by_name("search_query")
		search.send_keys(self.keyword)
		search.submit()

	def channelDriver(self):
		self.driverInit()
		self.driver.get(self.keyword)

	def getVideo(self):
		while True:
			query1 = self.driver.find_elements_by_id("video-title")
			for result in query1:
				video = result.get_attribute("href")
				if video is not None:
					if video not in self.list:
						self.list.append(video)
			self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
			time.sleep(3)
			if len(self.list) >= self.maxVideo:
				break

	def searchResult(self):
		self.searchDriver()
		self.getVideo()
		self.driver.quit()

	def channelResult(self):
		self.channelDriver()
		self.getVideo()
		self.driver.quit()

	def start(self):
		url = "https://www.youtube.com/c.*/.*"
		if re.match(url, self.keyword):
			self.channelResult()
		else:
			self.searchResult()
		return self.list[0:self.maxVideo]


def main():
	keyword = input()
	tab = Tab(keyword)
	tab.start()


if __name__ == "__main__":
	main()