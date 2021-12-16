import sys
import time
import os
from threading import Thread
from helper import resource_path,get_default_path,check_connection
from ctypes import windll
from video import Video
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

class App(QMainWindow):
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

	def initUI(self):
		self.make_main_window()

		self.folder_label()
		self.folder_button()
		
		self.test_connection()
		
		self.combo_box()

		self.url_input_text_box()

		self.check_input_url()

		self.lookup_button()

		# self.searchLink()
		
		self.show()

	"""
	main window where the size, title, and other setting lays
	"""
	def make_main_window(self):
		self.setWindowTitle("YouTube Downloader")
		self.setGeometry(0,0,270,220)
		self.setFixedSize(270,220)
		self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		self.setStyleSheet("QMainWindow {background-color: rgb(44, 210, 172);}")
		win = self.frameGeometry()
		center = QDesktopWidget().availableGeometry().center()
		win.moveCenter(center)
		self.move(win.topLeft())
		self.setWindowIcon(self.icon)

	"""
	folder_label init the label display the current folder it will download to by use self.path, default to the download folder
	folder_button create button allow user to interact with browse_folder to browse and change the download path to another folder
	"""
	def folder_label(self):
		self.folder_label = QLabel(self.path, self)
		self.folder_label.setGeometry(110,90,151,71)
		self.folder_label.setWordWrap(True)
	def folder_button(self):
		self.folder_button = QPushButton("Browse Folder", self)
		self.folder_button.setGeometry(10,110,81,31)
		self.folder_button.clicked.connect(self.browse_folder)
	def browse_folder(self):
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
			self.widget.close()
			self.window.close()
	"""
	test internet before opening the app, user with no internet connection will be getting warning pop up, user can try connection again or close the app
	"""
	def test_connection(self):
		if check_connection() == 0:
			self.no_internet_warning()
	def no_internet_warning(self):
		self.internet_warning_popup = QMessageBox(QMessageBox.Question, "Connection Issue", "There is no Internet Connection, press Retry to reconnect or Cancel to close the app \n")
		self.internet_warning_popup.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
		self.internet_warning_popup.setWindowTitle("Warning")
		self.internet_warning_popup.setIcon(QMessageBox.Critical)
		self.internet_warning_popup.setWindowIcon(self.icon)
		result = self.internet_warning_popup.exec_()
		if result == QMessageBox.Retry:
			self.test_connection()
		elif result == QMessageBox.Close:
			sys.exit(0)

	"""
	combo box for the user to select from video or music, depend on the selection it will download mp4 or mp3 format of the content
	combo_box method make the combobox
	combox_box_update_value to connect update function so the value self.combox_value will change every time user change the selection
	"""
	def combo_box(self):
		self.combobox = QComboBox(self)
		self.combobox.setGeometry(10, 10, 111, 21)
		self.combobox.addItem("Video")
		self.combobox.addItem("Music")
		self.combobox.activated.connect(self.combo_box_update_value)
	def combo_box_update_value(self):
			self.comboxbox_value = self.combobox.currentText()

	"""
	url_input_text_box will take the url input from user, check button press to verify the url:
		1. user enter the correct url, start button will be enabled
		2. user enter url thats not supported, invalid warning will popup
	"""
	def url_input_text_box(self):
		self.text_box = QLineEdit(self)
		self.text_box.setPlaceholderText("Enter URL")
		self.text_box.setGeometry(10, 50, 171, 21)
		self.text_box.textChanged.connect(self.text_box_change)
	def text_box_change(self):
		self.look_button.setEnabled(False)
	def check_input_url(self):
		self.check_button = QPushButton("check",self)
		self.check_button.setGeometry(200,50,50,20)
		self.check_button.clicked.connect(self.verify_url)
	def verify_url(self):
		url = self.text_box.text()
		if "youtube.com/watch" in url or "youtube.com/playlist" in url:
			self.look_button.setEnabled(True)
		elif "www.youtube.com/results?search_query" in url:
			self.look_button.setEnabled(True)
			self.url_information()
		else:
			self.look_button.setEnabled(False)
			self.invalid_url_warning()
	def invalid_url_warning(self):
		self.invalid_url_popup = QMessageBox()
		self.invalid_url_popup.setWindowIcon(self.icon)
		self.invalid_url_popup.setIcon(QMessageBox.Warning)
		self.invalid_url_popup.setWindowTitle("Warning")
		self.invalid_url_popup.setText("Invalid URL")
		self.invalid_url_popup.exec()
	def url_information(self):
		self.invalid_url_popup = QMessageBox()
		self.invalid_url_popup.setWindowIcon(self.icon)
		self.invalid_url_popup.setIcon(QMessageBox.Information)
		self.invalid_url_popup.setWindowTitle("FYI")
		self.invalid_url_popup.setText("Base on the url provided, it is a searched page, just FYI, search result is random")
		self.invalid_url_popup.exec()	

	"""
	when the lookup button is enable by valid url, clicking it will bring up another window which will display video list by the url:
		1. it will be single video, displaying the title
		2. it will be playlist displaying all the video from the playlist
		3. it will be mix of single videos scraped from the search query that may or may not contain playlist videos, result will be random
	"""
	def lookup_button(self):
		self.look_button = QPushButton("Lookup", self)
		self.look_button.setGeometry(100, 160, 50, 35)
		self.look_button.setCheckable(True)
		self.look_button.setEnabled(False)
		self.look_button.clicked.connect(self.list_video_widget)

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

	"""
	list video widget that will display the video choseable by the user to download"
		1. it can display single video because user enter single video link
		2. it can display a list of videos by playlist link
		flow:
			lookup button clicked
			thread to lookup by the url and display the video in list, meanwhile display searching in the window
			if the url is not valid, it will display error and not downloadable
			download button will start download the videos and once they are downloaded, there will be checkmark and it cant be select again from the same list
	"""
	def list_video(self):
		self.list_widget = QListWidget(self.widget)
		self.list_widget.setGeometry(0, 0, 300, 320) 
		self.list_widget.setSelectionMode(2)
		list_widget_thread = Thread(target=self.load_video,daemon=True)
		self.list_widget.addItem("Searching Video....")
		item = self.list_widget.item(0)
		item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
		self.download_button.setEnabled(False)
		list_widget_thread.start()

	def load_video(self):
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

	def download_video_button(self):
		self.download_button = QPushButton("Download",self.widget)
		self.download_button.setGeometry(220, 330, 70, 50)
		self.download_button.setCheckable(True)
		self.download_button.clicked.connect(self.make_download_thread)

	def make_download_thread(self):
		download_thread = Thread(target=self.download_action,daemon=True)
		download_thread.start()

	def download_action(self):
		for item in self.list_widget.selectedItems():
			item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
			title = item.text()
			link = self.hashmap[title]["video_object"]
			try:
				item.setText(f"Downloading   {title}")
				self.video_object.get_video(link,title)
				item.setText(f"{self.check_mark}   {title}")
			except Exception as e:
				item.setText(f"{e}   {title}")

	def list_video_widget(self):
		self.make_widget_window()
		self.download_video_button()
		self.list_video()
		self.widget.show()

	# def searchLink(self):
	# 	self.button2 = QPushButton("Search", self)
	# 	self.button2.setGeometry(190,50,51,21)
	# 	# self.button2.clicked.connect(self.listWindow)
	# 	self.button2.setCheckable(True)
	# 	self.button2.setEnabled(False)



	# def singleVideo(self):
	# 	video = Video(self.textbox.text(),self.path)
	# 	if self.drop.currentText() == "Video":
	# 		print('at video')
	# 		video.downloadSingleVideo()
	# 	elif self.drop.currentText() == "Music":
	# 		print('at music')
	# 		video.downloadSingleMusic()


	# def start(self):
	# 	if "youtube.com/watch" in self.textbox.text():
	# 		self.singleVideo()

def main():
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
	app = QApplication(sys.argv)
	software = App()
	software.initUI()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()

