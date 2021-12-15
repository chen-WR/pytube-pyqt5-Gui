from pytube import YouTube, Playlist
from helper import edit_title, ffmpeg_format, resource_path
from search import search_list
from threading import Thread
import time
import os
import subprocess
import re
import sys
import logging

class Video:
	logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)

	def __init__(self, path):
		# path to save the video/audio or music file to
		self.path = path
		# ffmpeg dir to use the bin to combine video and audio into one file
		self.ffmpeg = resource_path("./binary/ffmpeg.exe")
		# temp file name for downloaded files that will need to be converted later
		self.video = f"{self.path}/tempVideo.mp4"
		self.audio = f"{self.path}/tempAudio.mp4"
		self.music = f"{self.path}/tempMusic.mp4"
		self.dict = dict()


	# set new path if user change the path
	def set_path(self,path):
		self.path = path

	# temp file name doesnt change, so this method will remove any temp file in the path
	def remove_temp(self):
		if os.path.exists(self.video) or os.path.exists(self.audio):
			os.remove(self.video)
			os.remove(self.audio)
		elif os.path.exists(self.music):
			os.remove(self.music)

	"""
	Input url: youtube.com/watch?
	add link and title to dictionary to be use later
	"""
	def get_single_link(self,url):
		hashmap = dict()
		try:
			link = YouTube(url)
			title = link.title
			hashmap[title] = link
			return hashmap
		except Exception as e:
			print(e)

	def get_playlist_link(self,url):
		hashmap = dict()
		playlist = Playlist(url).videos
		for link in playlist:
			title = link.title
			hashmap[title] = link
		return hashmap

	def get_search_link(self,url):
		url_list = search_list(url)

	def get_video(self,link,title):
		def convert_video():
			title = edit_title(title)
			outputfile = f"{self.path}/{title}.mp4"
			if os.path.exists(outputfile):
				print(f"{title} already exists")
			else:
				try:
					command = f"{self.ffmpeg} -i {ffmpeg_format(self.video)} -i {ffmpeg_format(self.audio)} -c copy {ffmpeg_format(outputfile)} -hide_banner -loglevel error"
					subprocess.run(command)
				except Exception as e:
					print(e)
		# query the desire video
		video_query = link.streams.filter(only_video=True, file_extension="mp4", progressive=False).order_by("fps").order_by('resolution').desc()
		audio_query = link.streams.filter(only_audio=True, mime_type="audio/mp4").order_by("abr").desc()
		# remove possible existing temp file in the path
		self.remove_temp()
		# download temp video and audio file 
		video_query.first().download(self.path, filename=self.video)
		audio_query.first().download(self.path, filename=self.audio)
		convert_video()
		self.remove_temp()

	def get_music(self,link,title):
		def convert_music():
			title = edit_title(title)
			outputfile = f"{self.path}/{title}.mp3"
			if os.path.exists(outputfile):
				print(f"{title} already exists")
			else:
				try:
					command = f"{self.ffmpeg} -i {ffmpeg_format(self.music)} -b:a 192k -vn {ffmpeg_format(outputfile)} -hide_banner -loglevel error"
					subprocess.run(command)
				except Exception as e:
					print(e)
		music_query = link.streams.filter(only_audio=True, mime_type="audio/mp4").order_by("abr").desc()
		self.remove_temp()
		music_query.first().download(self.path, filename=self.music)
		convert_music()
		self.remove_temp()


	# def download_video(self,video_list):
	# 	for video in video_list:
	# 		link = self.get_link(video)
	# 		if link is not None:
	# 			self.get_video(link)
			

	# def download_music(self):
	# 	link = self.get_link()
	# 	if link is not None:
	# 		self.get_music(link)
	# 		return title

	# def download_playlist(self):
	# 	playlist = Playlist(self.url).videos
	# 	count = len(playlist)
		return count,playlist

	# def downloadSearchVideo(self,maxVideo):
	# 	tab = Tab(self.url, int(maxVideo))
	# 	for video in tab.start():
	# 		self.url = video
	# 		self.getlink()
	# 		self.downloadSingleVideo()

	def test(self,url):
		hm = self.get_single_link(url)
		for i,j in hm.items():
			print(i,"---------",j)

url1 = "https://www.youtube.com/watch?v=IC-tUY1l_6E"
url = "https://www.youtube.com/playlist?list=PL0unWuWLqh0JJPqxuM7EY93cyfVa1lf9T"
path = "c:/users/main/desktop"
video = Video(path)

video.test(url1)
