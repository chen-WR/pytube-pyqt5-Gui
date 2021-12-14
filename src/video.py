from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
from helper import edit_title, ffmpeg_format, resource_path
from videoScrap1 import Tab
import os
import subprocess
import re
import sys
import logging

class Video:
	logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)

	def __init__(self, url, path):
		# youtube url, either watch or playlist in the link
		self.url = url
		# path to save the video/audio or music file to
		self.path = path
		# ffmpeg dir to use the bin to combine video and audio into one file
		self.ffmpeg = resource_path("./binary/ffmpeg.exe")
		# temp file name for downloaded files that will need to be converted later
		self.video = f"{self.path}/tempVideo.mp4"
		self.audio = f"{self.path}/tempAudio.mp4"
		self.music = f"{self.path}/tempMusic.mp4"
		# title of the file object
		self.title = str()

	def remove_temp(self):
		if os.path.exists(self.video) or os.path.exists(self.audio):
			os.remove(self.video)
			os.remove(self.audio)
		elif os.path.exists(self.music):
			os.remove(self.music)

	def get_link(self):
		try:
			link = YouTube(self.url, on_progress_callback=on_progress)
		except Exception as error:
			logging.error(f"{error}")
			link = None
		finally:
			return link

	def get_video(self,link):
		def convert_video():
			title = edit_title(link.title)
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

	def get_music(self,link):
		def convert_music():
			title = edit_title(link.title)
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


	def download_video(self):
		link = self.get_link()
		if link is not None:
			self.get_video(link)
			return link.title

	def download_music(self):
		link= self.get_link()
		if link is not None:
			self.get_music(link)
			return title

	def download_video_playlist(self):
		playlist = Playlist(self.url).videos
		for link in playlist:
			if link is not None:
				self.get_video(link)

	def download_music_playlist(self):
		playlist = Playlist(self.url).videos
		for link in playlist:
			if link is not None:
				self.get_music(link)

	# def downloadSearchVideo(self,maxVideo):
	# 	tab = Tab(self.url, int(maxVideo))
	# 	for video in tab.start():
	# 		self.url = video
	# 		self.getlink()
	# 		self.downloadSingleVideo()

