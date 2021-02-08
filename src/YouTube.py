"""
01/02/2021
C.W.R.
YouTube Video Downloader
"""

from pytube import YouTube
from pytube import Playlist
# from pytube.cli import on_progress
# import ffmpeg
from videoScrap import Tab
import pytube
import os
import subprocess
import re
import time
import random
import socket 

class Video:
	def __init__(self, url, path, maxRange, vpn):
		self.url = url
		self.path = path
		self.maxRange = maxRange
		self.ffmpeg = self.resource_path("./binary/ffmpeg.exe")
		self.fps = 60
		self.res = "1080p"
		self.file_extension = "mp4"
		self.mime_type = "audio/mp4"
		self.progressive = False
		self.tempVideo = "tempVideo"
		self.tempAudio = "tempAudio"
		self.tempMusic = "tempMusic"
		self.video = f"\"{self.path}/{self.tempVideo}.mp4\""
		self.audio = f"\"{self.path}/{self.tempAudio}.mp4\""
		self.music = f"\"{self.path}/{self.tempMusic}.mp4\""
		self.findVideo = self.path + "/" + self.tempVideo + ".mp4"
		self.findAudio = self.path + "/" + self.tempAudio + ".mp4"
		self.findMusic = self.path + "/" + self.tempMusic + ".mp4"
		self.codec = "copy"
		self.raw = ""
		self.title = ""
		self.vpn = vpn
		self.playlistUrl = []
		self.playlistTitle = []
		self.randomVideos = []
		self.dict = {}
		self.repeat = 0
		self.check = 0
		self.error = ""
		self.errorList = [	"Error: Unexepected Error",
							"Error: KeyError",
							"Error: HTTP Error",
							"Error: Internet Error"
							]
	
	def resource_path(self, relative_path):
	    try:
	        base_path = sys._MEIPASS
	    except Exception:
	        base_path = os.path.dirname(__file__)
	    return os.path.join(base_path, relative_path)		

	def timeDelay(self):
		if self.vpn == False:
			time.sleep(10)

	def checkUrl(self):
		if "youtube.com/watch" in self.url:
			self.check = 1
		elif "youtube.com/playlist" in self.url:
			self.check = 2
		else:
			self.check = 3

	# Get Link to the video
	def getlink(self):
		if self.check == 1:
			try:
				self.link = YouTube(self.url)
				self.timeDelay()
				self.title = self.editText(self.link.title)
			except pytube.exceptions.PytubeError:
				self.error = "Error: Unexepected Error"
				self.writeError()
				pass
			except KeyError:
				self.error = "Error: KeyError"
				self.writeError()
				pass
			except urllib.error.HTTPError:
				self.error = "Error: HTTP Error"
				self.writeError()
				pass
			except socket.error:
				self.error = "Error: Internet Error"
				self.writeError()
				pass
		elif self.check == 2:
			playlist = Playlist(self.url)
			for videos in playlist.video_urls:
				try:
					self.link = YouTube(videos)
					self.timeDelay()
					self.title = self.editText(self.link.title)
					self.playlistUrl.append(self.link)
					self.playlistTitle.append(self.title)
				except pytube.exceptions.PytubeError:
					self.error = "Error: Unexepected Error"
					self.writeError()
					pass
				except KeyError:
					self.error = "Error: KeyError"
					self.writeError()
					pass
				except urllib.error.HTTPError:
					self.error = "Error: HTTP Error"
					self.writeError()
					pass
				except socket.error:
					self.error = "Error: Internet Error"
					self.writeError()
					pass
		elif self.check == 3:
			tab = Tab(self.url, self.maxRange)
			self.randomVideos = tab.start()
			for videos in self.randomVideos:
				try:
					self.link = YouTube(videos)
					self.timeDelay()
					self.title = self.editText(self.link.title)
					self.playlistUrl.append(self.link)
					self.playlistTitle.append(self.title)
				except pytube.exceptions.PytubeError:
					self.error = "Error: Unexepected Error"
					self.writeError()
					pass
				except KeyError:
					self.error = "Error: KeyError"
					self.writeError()
					pass
				except urllib.error.HTTPError:
					self.error = "Error: HTTP Error"
					self.writeError()
					pass
				except socket.error:
					self.error = "Error: Internet Error"
					self.writeError()
					pass
				
	# Edit text to prevent error
	def editText(self, title):
		rmSpecial = re.sub("[\"<>:*?|/]", "", title)
		rmBackslash = rmSpecial.replace("\\", "")
		title = rmBackslash.replace(" ", "_")
		return title

	def getTitle(self):
		return self.title

	def writeError(self):
		file = open("ErrorLog.txt", "a+", encoding="utf-8")
		file.write(self.url + "->" + self.error + "\n")
		file.close()

	# Remove file 
	def rmFile(self):
		if os.path.exists(self.findVideo) or os.path.exists(self.findAudio):
			os.remove(self.findVideo)
			os.remove(self.findAudio)
		elif os.path.exists(self.findMusic):
			os.remove(self.findMusic)

	def getTemp(self):
		query1 = self.link.streams.filter(fps=self.fps, only_video=True, file_extension=self.file_extension, progressive=self.progressive)
		query2 = self.link.streams.filter(only_video=True, file_extension=self.file_extension, progressive=self.progressive)
		query3 = self.link.streams.filter(only_audio=True, mime_type=self.mime_type)
		query4 = self.link.streams.filter(only_audio=True)
		if query1:
			list1 = query1
		else:
			list1 = query2
		if query3:
			list2 = query3
		else:
			list2 = query4
		video = list1.first()
		audio = list2.first()
		video.download(self.path, filename=self.tempVideo)
		audio.download(self.path, filename=self.tempAudio)

	def getMusic(self):
		query3 = self.link.streams.filter(only_audio=True, mime_type=self.mime_type)
		query4 = self.link.streams.filter(only_audio=True)
		if query3:
			list2 = query3
		else:
			list2 = query4
		audio = list2.first()
		audio.download(self.path, filename=self.tempMusic)

	def combineVideo(self):
		outputfile = f"\"{self.path}/{self.title}.mp4\""
		outputfileFind = self.path + "/" + self.title + ".mp4"
		flag = True
		while flag:
			if os.path.exists(outputfileFind):
				self.repeat+=1
				outputfile = f"\"{self.path}/{self.title}{str(self.repeat)}.mp4\""
				outputfileFind = self.path + "/" + self.title + str(self.repeat) + ".mp4"
			else:
				flag = False
		try:
			#ffmpeg.concat(inputv, inputa, v=1, a=1).output(outputfile).run()
			subprocess.run(f"{self.ffmpeg} -i {self.video} -i {self.audio} -c {self.codec} {outputfile} -hide_banner -loglevel error")
			#-hide_banner -loglevel error", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
		except:
			pass
		finally:
			self.rmFile()

	def convertMusic(self):
		outputfile = f"\"{self.path}/{self.title}.mp3\""
		outputfileFind = self.path + "/" + self.title + ".mp3"
		flag = True
		while flag:
			if os.path.exists(outputfileFind):
				self.repeat+=1
				outputfile = f"\"{self.path}/{self.title}{str(self.repeat)}.mp3\""
				outputfileFind = self.path + "/" + self.title +  str(self.repeat) + ".mp3"
			else:
				flag = False
		try:
			subprocess.run(f"{self.ffmpeg} -i {self.music} -b:a 192k -vn {outputfile} -hide_banner -loglevel error")
			# subprocess.run(f"ffmpeg -i {self.music} {outputfile}")
		except:
			pass
		finally:
			self.rmFile()

	def getSingleTitle(self):
		self.checkUrl()
		self.getlink()
		if self.error in self.errorList:
			title = self.error
		else:
			title = self.getTitle()
		return title

	def getDict(self):
		self.checkUrl()
		self.getlink()
		return self.playlistUrl, self.playlistTitle

	def downloadSingleVideo(self):
		if self.error in self.errorList:
			pass
		else:
			self.getTemp()
			self.combineVideo()

	def downloadSingleMusic(self):
		if self.error in self.errorList:
			pass
		else:
			self.getMusic()
			self.convertMusic()

	def downloadMultVideo(self, videos, titles):
		self.link = videos
		self.title = titles
		self.getTemp()
		self.combineVideo()

	def downloadMultMusic(self, videos, titles):
		self.link = videos
		self.title = titles
		self.getMusic()
		self.convertMusic()

def main():
	# pass
	url = input()
	path = "C://Users//School//Desktop//New folder"
	video = Video(url, path)
	video.getSingle()
	video.downloadSingleVideo()
	
if __name__ == "__main__":
	main()

