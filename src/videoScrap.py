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


class Tab:
	def __init__(self, keyword, maxRange):
		self.option = webdriver.ChromeOptions()
		self.option.add_argument("headless")
		self.driver = webdriver.Chrome(executable_path=self.resource_path('./binary/chromedriver.exe'),options=self.option)
		# self.driver = webdriver.Chrome()
		self.url = 'http://www.youtube.com/'
		self.name = "search_query"
		self.id = "video-title"
		self.class_name = "a.yt-simple-endpoint.style-scope.yt-formatted-string"
		self.script = "window.scrollTo(0, document.documentElement.scrollHeight);"
		self.linkSingle = []
		self.linkPlaylist = []
		self.linkPlaylistvideos = []
		self.finalList = []
		self.fixList = []
		self.playlistUrl = []
		self.playlistTitle = []
		self.keyword = keyword
		self.length = 0
		self.maxLink = 150
		self.maxRange = maxRange

	def resource_path(self, relative_path):
	    try:
	        base_path = sys._MEIPASS
	    except Exception:
	        base_path = os.path.dirname(__file__)
	    return os.path.join(base_path, relative_path)

	def webpage(self):
		self.driver.maximize_window()
		site = self.driver.get(self.url)

	def search(self, keyword):
		box = self.driver.find_element_by_name(self.name)
		box.send_keys(keyword)
		box.submit()

	def listUrl(self):
		query = self.driver.find_elements_by_id(self.id)
		for result in query:
			lists = result.get_attribute("href")
			if lists != None:
				if lists not in self.linkSingle:
					self.linkSingle.append(lists)

	def listPlaylist(self):
		query = self.driver.find_elements_by_css_selector(self.class_name)
		for result in query:
			lists = result.get_attribute("href")
			if "playlist" in lists:
				if lists not in self.linkPlaylist:
					self.linkPlaylist.append(lists)

	def listPlaylisturl(self):
		for url in self.linkPlaylist:
			plist = Playlist(url)
			for videos in plist.video_urls:
				if videos not in self.linkPlaylistvideos:
					self.linkPlaylistvideos.append(videos)

	def combineList(self):
		for single in self.linkSingle:
			if single not in self.finalList:
				self.finalList.append(single)
		for multi in self.linkPlaylistvideos:
			if multi not in self.finalList:
				self.finalList.append(multi)

	def infiniteScroll(self):
		flag = True
		while flag:
			time.sleep(3)
			self.listUrl()
			self.listPlaylist()
			self.listPlaylisturl()
			self.combineList()
			self.length = len(self.finalList)
			if self.length > self.maxLink:
				flag = False
			else:
				self.driver.execute_script(self.script)
				time.sleep(3)

	def close(self):
		return self.driver.quit()

	def start(self):
		self.webpage()
		self.search(self.keyword)
		self.infiniteScroll()
		self.close()
		for i in range(self.maxRange):
			self.fixList.append(self.finalList[i])
		return self.fixList

def main():
	# pass
	tab = Tab("jpop", 3)
	list1 = tab.start()
	print(list1)

if __name__ == "__main__":
	main()

