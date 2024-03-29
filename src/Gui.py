import sys
import time
import os
from threading import Thread
from helper import resource_path,get_default_path,check_connection,get_internet_speed, get_estimate_time
from ctypes import windll
from video import Video
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class App(QMainWindow):
	progress_bar_changed = pyqtSignal(int)
	def __init__(self):
		super().__init__()
		self.hashmap = dict()
		self.path = get_default_path()
		self.video_object = Video(self.path)
		self.window = QMainWindow()
		self.widget = QWidget()
		self.font = QFont("Tisa", 15)
		self.icon = QIcon(resource_path("./icon/icon.ico"))
		self.check_mark = u'\u2713'
		self.internet_speed_thread = Thread(target=self.get_internet_speed_thread,daemon=True)
		self.internet_speed_thread.start()

	def get_internet_speed_thread(self):
		# get inteernet speed
		self.download_speed = get_internet_speed()

	def initUI(self):
		self.make_main_window()
		self.test_internet_connection()
		self.make_folder_label()
		self.make_folder_button()
		self.make_combobox()
		self.url_text_box()
		self.check_url_button()
		self.make_lookup_button()
		self.show()
	"""
	main window where the size, title, and other setting lays
	"""
	def make_main_window(self):
		self.setWindowTitle("YouTube Downloader")
		self.setGeometry(0,0,300,220)
		self.setFixedSize(300,220)
		self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		self.setStyleSheet("QMainWindow {background-color: rgb(44, 210, 172);}")
		win = self.frameGeometry()
		center = QDesktopWidget().availableGeometry().center()
		win.moveCenter(center)
		self.move(win.topLeft())
		self.setWindowIcon(self.icon)
	"""
	test internet before opening the app, user with no internet connection will be getting warning pop up, user can try connection again or close the app
	"""
	def test_internet_connection(self):
		if check_connection() == 0:
			self.no_internet_warning_popup()
	def no_internet_warning_popup(self):
		self.internet_warning_popup = QMessageBox(QMessageBox.Question, "Connection Issue", "There is no Internet Connection, press Retry to reconnect or Cancel to close the app \n")
		self.internet_warning_popup.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
		self.internet_warning_popup.setWindowTitle("Warning")
		self.internet_warning_popup.setIcon(QMessageBox.Critical)
		self.internet_warning_popup.setWindowIcon(self.icon)
		result = self.internet_warning_popup.exec_()
		if result == QMessageBox.Retry:
			self.test_internet_connection()
		elif result == QMessageBox.Close:
			sys.exit(0)

	"""
	folder_label init the label display the current folder it will download to by use self.path, default to the download folder
	folder_button create button allow user to interact with browse folder to browse and change the download path to another folder
	"""
	def make_folder_label(self):
		self.folder_label = QLabel(self.path, self)
		self.folder_label.setGeometry(110,90,151,71)
		self.folder_label.setWordWrap(True)
	def make_folder_button(self):
		self.folder_button = QPushButton("Browse", self)
		self.folder_button.setGeometry(10,110,81,31)
		self.folder_button.clicked.connect(self.browse_folder_function)
	def browse_folder_function(self):
		self.dialog = QFileDialog()
		self.dialog.setFileMode(QFileDialog.Directory)
		if self.dialog.exec_():
			folder_name = self.dialog.selectedFiles()
			self.path = folder_name[0]
			self.video_object = Video(self.path)
		self.folder_label.setText(self.path)
	"""
	confirmation when the user click on the X close button on the top right of the ui
	"""
	def closeEvent(self, event):
		result = QMessageBox.question(self, "Confirm Exit?","Are you sure you want to exit ?",QMessageBox.Yes | QMessageBox.No)
		event.ignore()
		if result == QMessageBox.Yes:
			event.accept()
			self.video_object.remove_temp()
			self.widget.close()
			self.window.close()

	"""
	combo box for the user to select from video or music, depend on the selection it will download mp4 or mp3 format of the content
	combo_box method make the combobox
	combox_box_update_value to connect update function so the value self.combox_value will change every time user change the selection
	"""
	def make_combobox(self):
		self.combobox = QComboBox(self)
		self.combobox.setGeometry(10, 10, 111, 21)
		self.combobox.addItem("Video")
		self.combobox.addItem("Music")
		self.combobox_value = self.combobox.currentText()
		self.combobox.activated.connect(self.combobox_updated)
	def combobox_updated(self):
			#updating
			self.combobox_value = self.combobox.currentText()

	"""
	text_box will take the url input from user, check button press to verify the url:
		1. user enter the correct url, start button will be enabled
		2. user enter url thats not supported, invalid warning will popup
	"""
	def url_text_box(self):
		self.text_box = QLineEdit(self)
		self.text_box.setPlaceholderText("Enter URL")
		self.text_box.setGeometry(10, 50, 171, 21)
		self.text_box.textChanged.connect(self.text_box_update)
	def text_box_update(self):
		# disable the lookup button if user change the url to recheck
		self.look_button.setEnabled(False)

	"""
	Check if the url is valid so the lookup button will be enabled
	"""
	def check_url_button(self):
		self.check_button = QPushButton("check",self)
		self.check_button.setGeometry(200,50,50,20)
		self.check_button.clicked.connect(self.verify_url)
	def verify_url(self):
		url = self.text_box.text()
		if "youtube.com/watch" in url or "youtube.com/playlist" in url:
			self.look_button.setEnabled(True)
		elif "www.youtube.com/results?search_query" in url:
			self.look_button.setEnabled(True)
			self.search_function_uasge_popup()
		else:
			self.look_button.setEnabled(False)
			self.invalid_url_warning_popup()
	def invalid_url_warning_popup(self):
		self.invalid_url_popup = QMessageBox()
		self.invalid_url_popup.setWindowIcon(self.icon)
		self.invalid_url_popup.setIcon(QMessageBox.Warning)
		self.invalid_url_popup.setWindowTitle("Warning")
		self.invalid_url_popup.setText("Invalid URL")
		self.invalid_url_popup.exec()
	def search_function_uasge_popup(self):
		self.invalid_url_popup = QMessageBox()
		self.invalid_url_popup.setWindowIcon(self.icon)
		self.invalid_url_popup.setIcon(QMessageBox.Information)
		self.invalid_url_popup.setWindowTitle("FYI")
		self.invalid_url_popup.setText("Searched result may contain large playlist which will take time to show up as list, please be patient")
		self.invalid_url_popup.exec()


	"""
	when the lookup button is enable by valid url, clicking it will bring up another window which will display video list by the url:
		1. it will be single video, displaying the title
		2. it will be playlist displaying all the video from the playlist
		3. it will be mix of single videos scraped from the search query that may or may not contain playlist videos, result will be random
	"""
	def make_lookup_button(self):
		self.look_button = QPushButton("Lookup", self)
		self.look_button.setGeometry(100, 160, 50, 35)
		self.look_button.setCheckable(True)
		self.look_button.setEnabled(False)
		self.look_button.clicked.connect(self.make_download_widget)

	"""
	make download widget that will display the video choseable by the user to download"
		1. it can display single video because user enter single video link
		2. it can display a list of videos by playlist link
		flow:
			lookup button clicked
			thread to lookup by the url and display the video in list, meanwhile display searching in the window
			if the url is not valid, it will display error and not downloadable
			download button will start download the videos and once they are downloaded, there will be checkmark and it cant be select again from the same list
	"""
	def make_download_widget(self):
		self.make_widget_window()
		self.make_progress_bar()
		self.make_download_button()
		self.make_listwidget()
		self.widget.show()

	def make_widget_window(self):
		self.widget.setWindowTitle("Video List")
		self.widget.setWindowIcon(self.icon)
		self.widget.setGeometry(0, 0, 300, 380)
		self.widget.setFixedSize(300, 380)
		self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		win = self.widget.frameGeometry()
		center = QDesktopWidget().availableGeometry().center()
		win.moveCenter(center)
		self.widget.move(win.topLeft())

	def make_listwidget(self):
		self.list_widget = QListWidget(self.widget)
		self.list_widget.setGeometry(0, 0, 300, 320) 
		self.list_widget.setSelectionMode(2)
		self.list_widget.addItem("Searching Video....")
		item = self.list_widget.item(0)
		item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
		self.download_button.setEnabled(False)
		self.display_video_thread = Thread(target=self.display_video,daemon=True)
		self.display_video_thread.start()

	def display_video(self):
		url = self.text_box.text()
		if "youtube.com/watch" in url:
			try:
				self.hashmap = self.video_object.get_single_link(url)
			except:
				self.hashmap = None
		elif "youtube.com/playlist" in url:
			try:
				self.hashmap = self.video_object.get_playlist_link(url)
			except:
				self.hashmap = None
		elif "youtube.com/results?search_query" in url:
			try:
				self.hashmap = self.video_object.get_search_link(url)
			except:
				self.hashmap = None
		if self.hashmap is None:
			self.hashmap = {"Invalid Video":{"video_length":"NA","video_object":"NA"}}
			self.download_button.setEnabled(False)
		else:
			self.download_button.setEnabled(True)
		self.list_widget.clear()
		for title, sub_dict in self.hashmap.items():
			self.list_widget.addItem(f"{title}")

	def make_progress_bar(self):
		self.progress_bar = QProgressBar(self.widget)
		self.progress_bar.setGeometry(5,340,200,20)
		self.progress_bar_changed.connect(self.progress_bar.setValue)

	def update_progress_bar(self,estimate_time):
		up = int(100 / estimate_time)
		for i in range(0,99,up):
			self.progress_bar_changed.emit(i)
			time.sleep(1)

	def make_download_button(self):
		self.download_button = QPushButton("Download",self.widget)
		self.download_button.setGeometry(220, 340, 70, 20)
		self.download_button.setCheckable(True)
		self.download_button.clicked.connect(self.make_download_thread)

	def make_download_thread(self):
		self.download_thread = Thread(target=self.download_action,daemon=True)
		self.download_thread.start()

	def download_action(self):
		for item in self.list_widget.selectedItems():
			item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
			title = item.text()
			item.setText(f"Downloading   {title}")
			self.internet_speed_thread.join()
			if self.combobox_value == "Video":
				try:
					video_stream,audio_stream = self.hashmap[title]["video_object"],self.hashmap[title]["audio_object"]
					estimate_time = get_estimate_time(self.download_speed,video_stream.filesize+audio_stream.filesize)
					self.downloading_thread = Thread(target=self.video_object.download_video,args=(title,video_stream,audio_stream,),daemon=True)
					self.progress_bar_thread = Thread(target=self.update_progress_bar,args=(estimate_time,),daemon=True)
					self.downloading_thread.start()
					self.progress_bar_thread.start()
					self.progress_bar_thread.join()
					self.downloading_thread.join()
					self.progress_bar_changed.emit(100)
					item.setText(f"{self.check_mark}   {title}")
				except Exception as e:
					print(e)
					item.setText(f"{e} Error  {title}")
			elif self.combobox_value == "Music":
				try:
					audio_stream = self.hashmap[title]["audio_object"]
					estimate_time = get_estimate_time(self.download_speed,audio_stream.filesize)
					self.downloading_thread = Thread(target=self.video_object.download_music,args=(title,audio_stream,),daemon=True)
					self.progress_bar_thread = Thread(target=self.update_progress_bar,args=(estimate_time,),daemon=True)
					self.downloading_thread.start()
					self.progress_bar_thread.start()
					self.progress_bar_thread.join()
					self.downloading_thread.join()
					self.progress_bar_changed.emit(100)
					item.setText(f"{self.check_mark}   {title}")
				except Exception as e:
					print(e)
					item.setText(f"{e} Error  {title}")
			self.progress_bar_changed.emit(0)

def main():
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
	app = QApplication(sys.argv)
	software = App()
	software.initUI()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()
