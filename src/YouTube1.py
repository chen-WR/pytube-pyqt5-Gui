"""
01/02/2021
C.W.R.
YouTube Video Downloader
"""

from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
from videoScrap1 import Tab
import os
import subprocess
import re

class Video:
	def __init__(self, url, path):
		self.url = url
		self.path = path
		self.ffmpeg = self.resource_path("./binary/ffmpeg.exe")
		self.video = f"{self.path}/tempVideo.mp4"
		self.audio = f"{self.path}/tempAudio.mp4"
		self.music = f"{self.path}/tempMusic.mp4"
		self.title = ""
		self.error = ""
		self.repeat = 0
		self.check = self.checkUrl()

	# def checkUrl(self):
	# 	single = 'https://www.youtube.com/watch?v=.*'
	# 	playlist = 'https://www.youtube.com/playlist?list=.*'
	# 	channel = 'https://www.youtube.com/c.*/.*/videos'
	# 	if bool(re.match(single,self.url)):
	# 		job = 1
	# 	elif bool(re.match(playlist, self.url)):
	# 		job = 2
	# 	elif bool(re.match(channel,self.url)):
	# 		job = 3
	# 	else:
	# 		job = 0
	# 	return job
		
	def editText(self, title):
		rmSpecial = re.sub("[\"<>:*?|/]", "", title)
		rmBackslash = rmSpecial.replace("\\", "")
		title = rmBackslash.replace(" ", "_")
		return title

	def resource_path(self, relative_path):
	    try:
	        base_path = sys._MEIPASS
	    except Exception:
	        base_path = os.path.dirname(__file__)
	    return os.path.join(base_path, relative_path)	

	def rmFile(self):
		if os.path.exists(self.video) or os.path.exists(self.audio):
			os.remove(self.video)
			os.remove(self.audio)
		elif os.path.exists(self.music):
			os.remove(self.music)

	def checkDuplicate(self):
		outputfile = f"{self.path}/{self.title}.mp4"
		while True:
			if os.path.exists(outputfile):
				self.repeat+=1
				outputfile = f"{self.path}/{self.title}{str(self.repeat)}.mp4"
			else:
				break
		return self.ffmpegFormat(outputfile)

	def ffmpegFormat(self,file):
		return f'\"{file}\"'

	def getlink(self):
		try:
			self.link = YouTube(self.url, on_progress_callback=on_progress)
			self.title = self.editText(self.link.title)
		except:
			self.link = None				

	def getVideo(self):
		query1 = self.link.streams.filter(fps=60, only_video=True, file_extension="mp4", progressive=False)
		query2 = self.link.streams.filter(only_video=True, file_extension="mp4", progressive=False)
		query3 = self.link.streams.filter(only_audio=True, mime_type="audio/mp4")
		query4 = self.link.streams.filter(only_audio=True)
		video = query1.first() if query1 else query2.first()
		audio = query3.first() if query3 else query4.first()
		video.download(self.path, filename='tempVideo')
		audio.download(self.path, filename='tempAudio')

	def getMusic(self):
		query1 = self.link.streams.filter(only_audio=True, mime_type="audio/mp4")
		query2 = self.link.streams.filter(only_audio=True)
		audio = query1.first() if query1 else query2.first()
		audio.download(self.path, filename="tempMusic")

	def convertVideo(self):
		outputfile = self.checkDuplicate()
		try:
			command = f"{self.ffmpeg} -i {self.ffmpegFormat(self.video)} -i {self.ffmpegFormat(self.audio)} -c copy {outputfile} -hide_banner -loglevel error"
			subprocess.run(command)
		except:
			pass
		finally:
			self.rmFile()

	def convertMusic(self):
		outputfile = self.checkDuplicate()
		try:
			command = f"{self.ffmpeg} -i {self.ffmpegFormat(self.music)} -b:a 192k -vn {outputfile} -hide_banner -loglevel error"
			subprocess.run(command)
		except:
			pass
		finally:
			self.rmFile()

	def downloadSingleVideo(self):
		self.getlink()
		if self.link is not None:
			self.getVideo()
			self.convertVideo()

	def downloadSingleMusic(self):
		self.getlink()
		if self.link is not None:
			self.getMusic()
			self.convertMusic()

	def downloadMultVideo(self):
		playlist = Playlist(self.url).video_urls
		for video in playlist:
			self.url = video
			self.getlink()
			self.downloadSingleVideo()

	def downloadMultMusic(self):
		playlist = Playlist(self.url).video_urls
		for video in playlist:
			self.url = video
			self.getlink()
			self.downloadSingleMusic()

	def downloadSearchVideo(self):
		tab = Tab(self.url)
		for video in tab.searchResult():
			self.url = video
			self.getlink()
			self.downloadSingleVideo()

	def downloadSearchMusic(self):
		tab = Tab(self.url)
		for video in tab.searchResult():
			self.url = video
			self.getlink()
			self.downloadSingleMusic()

	def downloadChannelVideo(self):
		pass

	def downloadChannelMusic(self):
		pass

def main():
	while True:
		url = input('url')
		path = "C://Users//CR//Downloads"
		video = Video(url, path)
		print(video.check)
	
if __name__ == "__main__":
	main()
