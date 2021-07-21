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
from threading import Thread

class Tab:
	def __init__(self, keyword=None, maxVideo=30):
		self.list = []
		self.keyword = keyword
		self.maxVideo = maxVideo

	def resource_path(self, relative_path):
	    try:
	        base_path = sys._MEIPASS
	    except Exception:
	        base_path = os.path.dirname(__file__)
	    return os.path.join(base_path, relative_path)

	def searchdriverInit(self):
		self.option = webdriver.ChromeOptions()
		# self.option.add_argument("headless")
		self.driver = webdriver.Chrome(executable_path=self.resource_path('./binary/chromedriver.exe'),options=self.option)
		self.driver.maximize_window()
		self.driver.get("http://www.youtube.com/")
		search = self.driver.find_element_by_name("search_query")
		search.send_keys(self.keyword)
		search.submit()

	def singleVideo(self):
		query1 = self.driver.find_elements_by_id("video-title")
		for result in query1:
			video = result.get_attribute("href")
			if video is not None:
				if video not in self.list:
					self.list.append(video)

	def listVideo(self):
		query2 = self.driver.find_elements_by_css_selector("a.yt-simple-endpoint.style-scope.yt-formatted-string")
		for result in query2:
			playlist = result.get_attribute("href")
			if playlist is not None and "playlist" in playlist:
				videos = Playlist(playlist).video_urls		
				for video in videos:
					if video not in self.list:
						self.list.append(video)

	def searchResult(self):
		self.searchdriverInit()
		thread1 = Thread(target=self.singleVideo).start()
		thread2 = Thread(target=self.listVideo).start()
		while True:
			self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
			time.sleep(3)
			if len(self.list) >= self.maxVideo:
				break
		return self.list[0:self.maxVideo]

	def channelResult(self):
		pass

def main():
	tab = Tab("jpop")
	li = tab.searchResult()

	
if __name__ == "__main__":
	main()