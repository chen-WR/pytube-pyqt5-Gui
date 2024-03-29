from pytube import YouTube, Playlist
from helper import edit_title, ffmpeg_format, resource_path
from search import search_list
import os
import subprocess
import logging
import datetime
import traceback

class Video:
	def __init__(self, path):
		# path to save the video/audio or music file to
		self.path = path
		# ffmpeg dir to use the bin to combine video and audio into one file
		self.ffmpeg = resource_path("./binary/ffmpeg.exe")
		# temp file name for downloaded files that will need to be converted later
		self.video = f"{self.path}/tempVideo.mp4"
		self.audio = f"{self.path}/tempAudio.mp4"
		self.music = f"{self.path}/tempMusic.mp4"

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
	desire output = 
	{title:
		{
			"video_object":stream,
			"audio_object":stream,
			"music_object":stream
		}
	]}
	"""
	def get_single_link(self,url):
		hashmap = dict()
		try:
			link = YouTube(url)
			link.bypass_age_gate()
			title = link.title
			video_stream = link.streams.filter(only_video=True, file_extension="mp4", progressive=False).order_by("fps").order_by('resolution').desc().first()
			audio_stream = link.streams.filter(only_audio=True, mime_type="audio/mp4").order_by("abr").desc().first()
			hashmap.update({title:{"video_object":video_stream,"audio_object":audio_stream}})
			return hashmap
		except Exception as e:
			traceback.print_exc()
			hashmap = None
			return hashmap

	def get_playlist_link(self,url):
		hashmap = dict()
		playlist = Playlist(url).videos
		for link in playlist:
			try:
				link.bypass_age_gate()
				title = link.title
				video_stream = link.streams.filter(only_video=True, file_extension="mp4", progressive=False).order_by("fps").order_by('resolution').desc().first()
				audio_stream = link.streams.filter(only_audio=True, mime_type="audio/mp4").order_by("abr").desc().first()
				hashmap.update({title:{"video_object":video_stream,"audio_object":audio_stream}})
			except:
				pass
		return hashmap


	def get_search_link(self,url):
		hashmap = dict()
		url_list = search_list(url)
		for url in url_list:
			print(url)
			if "watch" in url:
				hashmap.update(self.get_single_link(url))
			elif "playlist" in url:
				hashmap.update(self.get_playlist_link(url))
		return hashmap

	def download_video(self,title,video_stream,audio_stream):
		def convert_video():
			formated_title = edit_title(title)
			outputfile = f"{self.path}/{formated_title}.mp4"
			if os.path.exists(outputfile):
				print(f"{formated_title} already exists")
			else:
				try:
					command = f"{self.ffmpeg} -i {ffmpeg_format(self.video)} -i {ffmpeg_format(self.audio)} -c copy {ffmpeg_format(outputfile)} -hide_banner -loglevel error"
					subprocess.run(command)
				except Exception as e:
					print(e)
		# remove possible existing temp file in the path
		self.remove_temp()
		# download temp video and audio file 
		video_stream.download(self.path, filename=self.video)
		audio_stream.download(self.path, filename=self.audio)
		convert_video()
		self.remove_temp()

	def download_music(self,title,audio_stream):
		def convert_music():
			formated_title = edit_title(title)
			outputfile = f"{self.path}/{formated_title}.mp3"
			if os.path.exists(outputfile):
				print(f"{formated_title} already exists")
			else:
				try:
					command = f"{self.ffmpeg} -i {ffmpeg_format(self.music)} -b:a 192k -vn {ffmpeg_format(outputfile)} -hide_banner -loglevel error"
					subprocess.run(command)
				except Exception as e:
					print(e)
		self.remove_temp()
		audio_stream.download(self.path, filename=self.music)
		convert_music()
		self.remove_temp()