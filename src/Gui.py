import sys
import time
import os
import threading 
import multiprocessing
import pytube
from ctypes import windll
from YouTube import Video
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
		self.left = 0
		self.top = 0 
		self.width = 600
		self.height = 560
		self.path = self.getPath()
		self.dropdownSelection = ""
		self.title = "YouTube Downloader"
		self.spinValue = 0
		self.count = 0
		self.videoCount = "Total Download Count: " + str(self.count)
		self.currentName = ""
		self.textHistory = []
		self.finishName = []
		self.playlistURL = []
		self.playlistTitle = []
		self.finalUrl = []
		self.finalTitle = []
		self.dict = {}
		self.items = []
		self.innerTitle = "By pizza0201"
		self.text1 = "Enter Single or Playlist Link, or Keyword to Search"
		self.text2 = "Browse Folder"
		self.text3 = "Start"
		self.current = "Currently Downloading: "
		self.finish = "Downloaded: "
		self.window = QMainWindow()
		self.widget = QWidget()
		self.font = QFont("Tisa", 15)
		self.icon = QIcon(self.resource_path("./icon/icon.ico"))
		self.ui = self.resource_path("./icon/help.ui")
		self.stylesheetMainwindow = """
    		QMainWindow {
    			background-color: rgb(44, 210, 172);
    		}
		"""
	def resource_path(self, relative_path):
	    try:
	        base_path = sys._MEIPASS
	    except Exception:
	        base_path = os.path.dirname(__file__)
	    return os.path.join(base_path, relative_path)

	def initUI(self):
		self.makeMain()
		self.tryConnection()
		self.show()

	def reinit(self):
		self.playlistTitle = []
		self.playlistURL = []
		self.finalUrl = []
		self.finalTitle = []
		self.dict = {}
	
	def writeDownloadHistory(self):
		self.file = open("History.txt", "a+", encoding="utf-8")
		for file in self.finishName:
			self.file.write(file + "\n")
		self.file.close()

	def closeEvent(self, event):
		result = QMessageBox.question(self, "Confirm Exit?","Are you sure you want to exit ?",QMessageBox.Yes | QMessageBox.No)
		event.ignore()
		if result == QMessageBox.Yes:
			event.accept()
			self.widget.close()
			self.window.close()
			self.writeDownloadHistory()
	
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
		self.label2.setText(self.newPath)

	def makeMain(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setFixedSize(self.width, self.height)
		self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		self.setStyleSheet(self.stylesheetMainwindow)
		win = self.frameGeometry()
		center = QDesktopWidget().availableGeometry().center()
		win.moveCenter(center)
		self.move(win.topLeft())
		self.setWindowIcon(self.icon)

		self.label1 = QLabel(self.innerTitle, self)
		self.label1.setGeometry(10, 31, 91, 21)

		self.label2 = QLabel(self.path, self)
		self.label2.setGeometry(170, 130, 251, 71)
		self.label2.setWordWrap(True)

		self.label3 = QLabel(self.videoCount, self)
		self.label3.setGeometry(30, 220, 171, 21)

		self.label4 = QLabel(self.current, self)
		self.label4.setGeometry(10, 250, 141, 31)
		self.label4.setWordWrap(True)

		self.label5 = QLabel(self.finish, self)
		self.label5.setGeometry(10, 330, 81, 31)

		self.button1 = QPushButton(self.text2, self)
		self.button1.setGeometry(30, 140, 111, 51)
		self.button1.clicked.connect(self.browseFolder)

		self.button2 = QPushButton(self.text3, self)
		self.button2.setGeometry(480, 200, 111, 71)
		self.button2.clicked.connect(self.getStart)
		self.button2.setCheckable(True)
		self.button2.setEnabled(False)

		self.button3 = QPushButton("Search", self)
		self.button3.setGeometry(380, 80, 61, 31)
		self.button3.clicked.connect(self.listWindow)
		self.button3.setCheckable(True)
		self.button3.setEnabled(False)

		self.textbox = QLineEdit(self)
		self.textbox.setPlaceholderText(self.text1)
		self.textbox.setGeometry(10, 80, 361, 31)
		self.textbox.textChanged.connect(self.textboxChange)

		self.spinbox = QSpinBox(self)
		self.spinbox.setGeometry(330, 40, 42, 22)
		self.spinbox.setMinimum(0)
		self.spinbox.setMaximum(200)
		self.spinbox.setEnabled(False)

		self.checkbox = QCheckBox(self)
		self.checkbox.setText("VPN")
		self.checkbox.setGeometry(270, 40, 52, 22)

		self.drop = QComboBox(self)
		self.drop.setGeometry(450, 40, 141, 31)
		self.drop.addItem("Please Select One: ")
		self.drop.addItem("Video")
		self.drop.addItem("Music")
		self.drop.activated.connect(self.getDropdownValue)

		self.listWidget1 = QListWidget(self)
		self.listWidget1.setGeometry(10, 290, 581, 41)
		self.listWidget2 = QListWidget(self)
		self.listWidget2.setGeometry(10, 360, 581, 151)	

		self.menuBar = self.menuBar()
		self.menu1 = self.menuBar.addMenu("File")
		self.menu2 = self.menuBar.addMenu("Help")
		self.subMenuAction2 = QAction("Manual", self)
		self.subMenuAction2.triggered.connect(self.helpManual)
		self.menu2.addAction(self.subMenuAction2)
		# subMenu1.addAction(subMenuAction1)
		# subMenuAction1.triggered.connect(self.quitApp)
		# self.menu1.addMenu(subMenu1)
		# self.menu2 = self.menuBar.addMenu("Edit")
		# subMenu2 = QMenu("Coming Soon", self)
		# self.menu2.addMenu(subMenu2)
		# self.menu3 = self.menuBar.addMenu("Help")
		# subMenu3 = QMenu("Manual", self)
		# subMenu3.triggered.connect(self.helpManual)
		# self.menu3.addMenu(subMenu3)

	def helpManual(self):
		self.window.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		uic.loadUi(self.ui, self.window)
		self.window.setStyleSheet(self.stylesheetMainwindow)
		self.window.setFixedSize(600, 800)
		self.window.setWindowIcon(self.icon)
		self.window.show()

	def addText(self):
		self.textHistory.append(self.getText())

	def getText(self):
		text = self.textbox.text()
		return text
		
	def getSpinValue(self):
		self.spinValue = self.spinbox.value()
		return self.spinValue

	def getcheckboxValue(self):
		return self.checkbox.isChecked()

	def getDropdownValue(self):
		self.dropdownSelection = self.drop.currentText()
		if self.dropdownSelection == "Video":
			self.button2.setEnabled(True)
		elif self.dropdownSelection == "Music":
			self.button2.setEnabled(True)
		else:
			self.button2.setEnabled(False)

	def makeObj(self):
		video = Video(self.getText(), self.path, self.getSpinValue(), self.getcheckboxValue())
		return video

	def listWindow(self):
		self.widget = QWidget()
		self.widget.setWindowTitle("Video List")
		self.widget.setWindowIcon(self.icon)
		self.widget.setGeometry(0, 0, 300, 380)
		self.widget.setFixedSize(300, 380)
		self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		win = self.widget.frameGeometry()
		center = QDesktopWidget().availableGeometry().center()
		win.moveCenter(center)
		self.widget.move(win.topLeft())

		self.listWidget = QListWidget(self.widget)
		self.listWidget.setGeometry(0, 0, 300, 320) 
		self.listWidget.setSelectionMode(2)
		self.listWidget.addItem("Searching.....")

		self.button4 = QPushButton("Cancel", self.widget)
		self.button4.setGeometry(5, 330, 81, 41)
		self.button4.clicked.connect(self.exitListWidget)
		self.button5 = QPushButton("Ok", self.widget)
		self.button5.setGeometry(210, 330, 81, 41)
		self.button5.clicked.connect(self.getList)

		# self.searchingList()
		thread1 = threading.Thread(target=self.searchingList)
		thread1.start()
		self.widget.show()

	def searchingList(self):
		video = self.makeObj()
		self.getDict(video)
		self.listWidget.clear()
		self.listWidget.addItems(self.playlistTitle)

	def exitListWidget(self):
		self.widget.close()	

	def getList(self):
		self.items = self.listWidget.selectedItems()
		for i in range(len(self.items)):
			tempTitle = str(self.items[i].text())
			for titles in self.playlistTitle:
				if titles == tempTitle:
					index = self.playlistTitle.index(titles)
					self.finalUrl.append(self.playlistURL[index])
					self.finalTitle.append(titles)
		self.widget.close()	
		self.dict = {}
		self.dict = dict(zip(self.finalUrl, self.finalTitle))

	def getDict(self, video):
		self.addText()
		access = 0
		if len(self.textHistory) >= 3:
			access = -2
		if (len(self.textHistory) == 1) or (len(self.textHistory) == 2 and self.getText() != self.textHistory[access]) or (len(self.textHistory) >= 3 and self.getText() != self.textHistory[access]):
			self.reinit()
			self.playlistURL, self.playlistTitle = video.getDict()
			self.dict = {}
			self.dict = dict(zip(self.playlistURL, self.playlistTitle))

	def textboxChange(self):
		text = self.getText()			
		if "youtube.com/watch" in text:
			self.spinbox.setEnabled(False)
			self.button3.setEnabled(False)
		elif "playlist" in text:
			self.spinbox.setEnabled(False)
			self.button3.setEnabled(True)
		elif text == "":
			self.spinbox.setEnabled(False)
			self.button3.setEnabled(False)
		else:
			self.spinbox.setEnabled(True)
			self.button3.setEnabled(True)
		
	def popWarning1(self):
		self.popup1 = QMessageBox()
		self.popup1.setWindowTitle("Warning")
		self.popup1.setText("Text Box Is Empty")
		self.popup1.setWindowIcon(self.icon)
		self.popup1.exec_()

	def popWarning2(self):
		self.popup2 = QMessageBox()
		self.popup2.setWindowTitle("Warning")
		self.popup2.setText("Max Number Of Url Can\'t be Zero")
		self.popup2.setWindowIcon(self.icon)
		self.popup2.exec_()

	def popWarning3(self):
		self.popup3 = QMessageBox(QMessageBox.Question, "Connection Issue", "There is no Internet Connection, press Retry to reconnect or Cancel to close the app \n")
		self.popup3.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
		self.popup3.setWindowTitle("Warning")
		self.popup3.setIcon(QMessageBox.Critical)
		self.popup3.setWindowIcon(self.icon)
		result = self.popup3.exec_()
		if result == QMessageBox.Retry:
			self.tryConnection()
		elif result == QMessageBox.Close:
			sys.exit(0)

	def tryConnection(self):
		url = "http://www.youtube.com"
		try:
			urllib.request.urlopen(url)
		except:
			self.popWarning3()

	def checkInternet(self):
		if self.tryConnection() == False:
			self.popWarning3()

	def cleanTextbox(self):
		self.textbox.clear()

	def cleanListWidget1(self):
		self.listWidget1.clear()

	def cleanListWidget2(self):
		self.listWidget2.clear()

	def disableButton(self):
		self.button1.setEnabled(False)
		self.button2.setEnabled(False)
		self.button3.setEnabled(False)
		self.drop.setEnabled(False)
		self.checkbox.setEnabled(False)
		self.textbox.setEnabled(False)
		self.spinbox.setEnabled(False)

	def enableButton(self):
		self.button1.setEnabled(True)
		self.button2.setEnabled(True)
		self.drop.setEnabled(True)
		self.checkbox.setEnabled(True)
		self.textbox.setEnabled(True)

	def changeLabel(self):
		self.newVideoCount = "Total Download Count: " + str(self.count)
		self.label3.setText(self.newVideoCount)
		QCoreApplication.processEvents()	

	def getCurrentList(self):
		self.listWidget1.addItem(self.currentName)
		QCoreApplication.processEvents()
	
	def getFinishedList(self):
		self.listWidget2.addItems(reversed(self.finishName))
		QCoreApplication.processEvents()

	def downloadVideo(self):
		video = self.makeObj()
		self.count += 1
		title = video.getSingleTitle()
		self.currentName = title
		self.cleanListWidget2()
		self.changeLabel()
		self.getCurrentList()
		self.getFinishedList()
		video.downloadSingleVideo()
		self.count -= 1
		self.finishName.append(title)
		self.cleanListWidget1()
		self.cleanListWidget2()
		self.downloadAfter()

	def downloadListVideo(self):
		video = self.makeObj()
		if not self.finalUrl:
			self.getDict(video)
			self.count += len(self.playlistURL)
			for url,title in self.dict.items():
				self.cleanListWidget2()
				self.currentName = title
				self.changeLabel()
				self.getCurrentList()
				self.getFinishedList()
				video.downloadMultVideo(url, title)
				self.count -= 1
				self.finishName.append(title)
				self.cleanListWidget1()
				self.cleanListWidget2()
			self.downloadAfter()
		elif self.finalUrl:
			self.count += len(self.finalUrl)
			for url,title in self.dict.items():
				self.cleanListWidget2()
				self.currentName = title
				self.changeLabel()
				self.getCurrentList()
				self.getFinishedList()
				video.downloadMultVideo(url, title)
				self.count -= 1
				self.finishName.append(title)
				self.cleanListWidget1()
				self.cleanListWidget2()
			self.downloadAfter()
			self.finalUrl = []
			self.finalTitle = []

	def downloadMusic(self):
		music = self.makeObj()
		self.count += 1
		title = music.getSingleTitle()
		self.currentName = title
		self.cleanListWidget2()
		self.changeLabel()
		self.getCurrentList()
		self.getFinishedList()
		music.downloadSingleMusic()
		self.count -= 1
		self.finishName.append(title)
		self.cleanListWidget1()
		self.cleanListWidget2()
		self.downloadAfter()

	def downloadListMusic(self):
		music = self.makeObj()
		if not self.finalUrl:
			self.getDict(music)
			self.count += len(self.playlistURL)
			for url,title in self.dict.items():
				self.cleanListWidget2()
				self.currentName = title
				self.changeLabel()
				self.getCurrentList()
				self.getFinishedList()
				music.downloadMultMusic(url, title)
				self.count -= 1
				self.finishName.append(title)
				self.cleanListWidget1()
				self.cleanListWidget2()
			self.downloadAfter()
		elif self.finalUrl:
			self.count += len(self.finalUrl)
			for url,title in self.dict.items():
				self.cleanListWidget2()
				self.currentName = title
				self.changeLabel()
				self.getCurrentList()
				self.getFinishedList()
				music.downloadMultMusic(url, title)
				self.count -= 1
				self.finishName.append(title)
				self.cleanListWidget1()
				self.cleanListWidget2()
			self.downloadAfter()
			self.finalUrl = []
			self.finalTitle = []
	
	def downloadAfter(self):
		self.changeLabel()
		self.getFinishedList()
		self.cleanTextbox()
		self.cleanListWidget1()
		self.enableButton()

	def getStart(self):
		if not self.getText():
			self.popWarning1()
		else:
			if self.dropdownSelection == "Video":
				if "youtube.com/watch" in self.getText():
					self.disableButton()
					thread2 = threading.Thread(target=self.downloadVideo)
					thread2.start()	
				elif "youtube.com/playlist" in self.getText():
					self.disableButton()
					thread3 = threading.Thread(target=self.downloadListVideo) 
					thread3.start()
				else:
					if self.getSpinValue() == 0:
						self.popWarning2()
					else:
						self.disableButton()
						thread4 = threading.Thread(target=self.downloadListVideo)
						thread4.start()
			elif self.dropdownSelection == "Music":
				if "youtube.com/watch" in self.getText():
					self.disableButton()
					thread5 = threading.Thread(target=self.downloadMusic) 
					thread5.start()
				elif "youtube.com/playlist" in self.getText():
					self.disableButton()
					thread6 = threading.Thread(target=self.downloadListMusic) 
					thread6.start()	
				else:
					if self.getSpinValue() == 0:
						self.popWarning2()
					else:
						self.disableButton()
						thread7 = threading.Thread(target=self.downloadListMusic)
						thread7.start()

def main():
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
	app = QApplication(sys.argv)
	software = App()
	software.initUI()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()