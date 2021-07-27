import sys
import time
import os
import pytube
from ctypes import windll
from YouTube1 import Video
from videoScrap import Tab
from winreg import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import urllib

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.action = ""
		self.path = self.getPath()
		self.dropdownSelection = ""
		self.window = QMainWindow()
		self.widget = QWidget()
		self.font = QFont("Tisa", 15)
		self.icon = QIcon(self.resource_path("./icon/icon.ico"))

	def initUI(self):
		self.makeMain()
		self.comboBox()
		self.spinBox()
		self.folderLabel()
		self.folderButton()
		self.linkInput()
		self.searchLink()
		self.startButton()
		self.tryConnection()
		self.show()


	def resource_path(self, relative_path):
	    try:
	        base_path = sys._MEIPASS
	    except Exception:
	        base_path = os.path.dirname(__file__)
	    return os.path.join(base_path, relative_path)

	def getPath(self):
		with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders') as key:
			Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
		return Downloads

	def browseFolder(self):
		self.dialog = QFileDialog()
		self.dialog.setFileMode(QFileDialog.Directory)
		if self.dialog.exec_():
			folderName = self.dialog.selectedFiles()
			self.path = ""
			self.path += folderName[0]
			self.getUpdatedpath()

	def getUpdatedpath(self):
		self.newPath = self.path
		self.label1.setText(self.newPath)

	def closeEvent(self, event):
		result = QMessageBox.question(self, "Confirm Exit?","Are you sure you want to exit ?",QMessageBox.Yes | QMessageBox.No)
		event.ignore()
		if result == QMessageBox.Yes:
			event.accept()
			self.widget.close()
			self.window.close()

	def popWarning1(self):
		self.popup1 = QMessageBox(QMessageBox.Question, "Connection Issue", "There is no Internet Connection, press Retry to reconnect or Cancel to close the app \n")
		self.popup1.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
		self.popup1.setWindowTitle("Warning")
		self.popup1.setIcon(QMessageBox.Critical)
		self.popup1.setWindowIcon(self.icon)
		result = self.popup1.exec_()
		if result == QMessageBox.Retry:
			self.tryConnection()
		elif result == QMessageBox.Close:
			sys.exit(0)

	def tryConnection(self):
		url = "http://www.youtube.com"
		try:
			urllib.request.urlopen(url)
		except:
			self.popWarning1()

	def makeMain(self):
		self.setWindowTitle("YouTube Downloader")
		self.setGeometry(0,0,270,270)
		self.setFixedSize(270,270)
		self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		self.setStyleSheet("QMainWindow {background-color: rgb(44, 210, 172);}")
		win = self.frameGeometry()
		center = QDesktopWidget().availableGeometry().center()
		win.moveCenter(center)
		self.move(win.topLeft())
		self.setWindowIcon(self.icon)

	def comboBox(self):
		self.drop = QComboBox(self)
		self.drop.setGeometry(10, 10, 111, 21)
		self.drop.addItem("Video")
		self.drop.addItem("Music")
		#self.drop.currentText()

	def spinBox(self):
		self.spinbox = QSpinBox(self)
		self.spinbox.setGeometry(140, 10, 41, 21)
		self.spinbox.setMinimum(1)
		self.spinbox.setMaximum(200)
		self.spinbox.setEnabled(False)

	def folderLabel(self):
		self.label1 = QLabel(self.path, self)
		self.label1.setGeometry(110,90,151,71)
		self.label1.setWordWrap(True)

	def folderButton(self):
		self.button1 = QPushButton("Browse Folder", self)
		self.button1.setGeometry(10,110,81,31)
		self.button1.clicked.connect(self.browseFolder)

	def linkInput(self):
		self.textbox = QLineEdit(self)
		self.textbox.setPlaceholderText("Enter Link")
		self.textbox.setGeometry(10, 50, 171, 21)
		self.textbox.textChanged.connect(self.textboxChange)

	def textboxChange(self):
		text = self.textbox.text()			
		if "youtube.com/watch" in text:
			self.spinbox.setEnabled(False)
			self.button3.setEnabled(True)
		elif "playlist" in text:
			self.spinbox.setEnabled(False)
			self.button3.setEnabled(True)
		elif text == "":
			self.spinbox.setEnabled(False)
			self.button3.setEnabled(False)
		else:
			self.spinbox.setEnabled(True)
			self.button3.setEnabled(True)

	def searchLink(self):
		self.button2 = QPushButton("Search", self)
		self.button2.setGeometry(190,50,51,21)
		# self.button2.clicked.connect(self.listWindow)
		self.button2.setCheckable(True)
		self.button2.setEnabled(False)

	def startButton(self):
		self.button3 = QPushButton("Start", self)
		self.button3.setGeometry(60, 160, 131, 61)
		self.button3.clicked.connect(self.start)
		self.button3.setCheckable(True)
		self.button3.setEnabled(False)

	def singleVideo(self):
		video = Video(self.textbox.text(),self.path)
		if self.drop.currentText() == "Video":
			print('at video')
			video.downloadSingleVideo()
		elif self.drop.currentText() == "Music":
			print('at music')
			video.downloadSingleMusic()


	def start(self):
		if "youtube.com/watch" in self.textbox.text():
			self.singleVideo()

def main():
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
	app = QApplication(sys.argv)
	software = App()
	software.initUI()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()
