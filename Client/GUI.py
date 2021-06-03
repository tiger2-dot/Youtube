from Client import Network
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import sys
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
'''
pip install matplotlib
pip install pyqt5
pip install numpy
'''

class Entry(QMainWindow):
	def __init__(self,network,create_new_acc = False):
		super(Entry,self).__init__()
		self.network = network
		if create_new_acc == False: #just wants to login
			self.login()
		else:
			self.create_new_acc_gui()

	def create_new_acc(self):
		new_acc = Entry(self.network, True)
		widget.addWidget(new_acc)
		widget.setCurrentIndex(widget.currentIndex() + 1)

	def create_new_acc_gui(self):
		background = QLabel(self)
		background.move(0,0)
		background.resize(1820,920)
		background.setStyleSheet("border-image : url(imgs/back2.png);")

		logo = QtWidgets.QPushButton(self)
		logo.setGeometry(500,300,250,180)
		logo.setStyleSheet("border-image : url(imgs/logo.png);")

		userL = QLabel(self)
		userL.setText('NEW USERNAME: ')
		userL.setStyleSheet('font-weight: bold; font: 17pt Times')
		userL.move(730,275)
		userL.resize(180,70)

		self.new_username = QLineEdit(self)
		self.new_username.setGeometry(925,290,230,40)
		font = self.new_username.font()
		font.setPointSize(17)
		self.new_username.setFont(font)

		new_passL = QLabel(self)
		new_passL.setText('NEW PASSWORD: ')
		new_passL.setStyleSheet('font-weight: bold; font: 17pt Times')
		new_passL.move(730,340)
		new_passL.resize(187,50)

		self.new_password = QLineEdit(self)
		self.new_password.setGeometry(925,345,230,40)
		font = self.new_password.font()
		font.setPointSize(17)
		self.new_password.setFont(font)
		self.new_password.setEchoMode(QtWidgets.QLineEdit.Password)

		confirm_new_pass = QLabel(self)
		confirm_new_pass.setText('CONFIRM NEW PASSWORD: ')
		confirm_new_pass.setStyleSheet('font-weight: bold; font: 17pt Times')
		confirm_new_pass.move(730,390)
		confirm_new_pass.resize(290,50)

		self.confirm_new_password = QLineEdit(self)
		self.confirm_new_password.setGeometry(1030,395,230,40)
		font = self.confirm_new_password.font()
		font.setPointSize(17)
		self.confirm_new_password.setFont(font)
		self.confirm_new_password.setEchoMode(QtWidgets.QLineEdit.Password)
		
		enterButt = QtWidgets.QPushButton(self)
		enterButt.setText('BACK')
		enterButt.setGeometry(730,438,170,38)
		enterButt.clicked.connect(self.go_back)

		backButt = QtWidgets.QPushButton(self)
		backButt.setText('CREATE')
		backButt.setGeometry(920,438,170,38)
		backButt.clicked.connect(self.add_user)

	def go_back(self):
		new_acc = Entry(self.network)
		widget.addWidget(new_acc)
		widget.setCurrentIndex(widget.currentIndex() + 1)

	def add_user(self):
		username = self.new_username.text()
		password = self.new_password.text()
		confirmPass = self.confirm_new_password.text()

		if username != '' or password != '':
			if password == confirmPass:
				if self.network.check_user(username) == False:
					
					self.network.add_user(username,password)

					main_window = MainGUI(self.network,username)
					widget.addWidget(main_window)
					widget.setCurrentIndex(widget.currentIndex() + 1)

	def login(self):
		background = QLabel(self)
		background.move(0,0)
		background.resize(1820,920)
		background.setStyleSheet("border-image : url(imgs/back2.png);")

		logo = QtWidgets.QPushButton(self)
		logo.setGeometry(500,300,250,180)
		logo.setStyleSheet("border-image : url(imgs/logo.png);")

		userL = QLabel(self)
		userL.setText('USERNAME: ')
		userL.setStyleSheet('font-weight: bold; font: 17pt Times')
		userL.move(730,290)
		userL.resize(125,50)

		self.user_name = QLineEdit(self)
		self.user_name.setGeometry(870,294,230,40)
		font = self.user_name.font()
		font.setPointSize(17)
		self.user_name.setFont(font)

		passL = QLabel(self)
		passL.setText('PASSWORD: ')
		passL.setStyleSheet('font-weight: bold; font: 17pt Times')
		passL.move(730,350)
		passL.resize(125,50)

		self.password = QLineEdit(self)
		self.password.setGeometry(870,350,230,40)
		font = self.password.font()
		font.setPointSize(17)
		self.password.setFont(font)
		self.password.setEchoMode(QtWidgets.QLineEdit.Password)
		
		enterButt = QtWidgets.QPushButton(self)
		enterButt.setText('LOGIN')
		enterButt.setGeometry(730,412,170,70)
		enterButt.clicked.connect(self.check_user)
		
		newAcc = QtWidgets.QPushButton(self)
		newAcc.setText('REGISTER')
		newAcc.setGeometry(920,412,179,70)
		newAcc.clicked.connect(self.create_new_acc)
		

	def check_user(self):
		username = self.user_name.text()
		password = self.password.text()

		if_user_exist = self.network.check_user(username)

		if if_user_exist:
			main = MainGUI(self.network,username)
			widget.addWidget(main)
			widget.setCurrentIndex(widget.currentIndex() + 1)
		else:
			self.create_new_acc()


class MainGUI(QMainWindow):
	def __init__(self,network,username,videoCounter = 0):
		super(MainGUI,self).__init__()
		self.network = network
		self.username = username
		self.videoCounter = videoCounter
		self.MainUI()
		self.SideBarUI()


	def SideBarUI(self):
		borderLabel = QLabel(self)
		borderLabel.move(1600,0)
		borderLabel.resize(220,920)
		borderLabel.setStyleSheet("border-image : url(imgs/back3.png);")

		logoButt = QtWidgets.QPushButton(self)
		logoButt.setGeometry(1595,10,220,150)
		logoButt.setStyleSheet("border-image : url(imgs/logo.png);")

		uploadButt = QtWidgets.QPushButton(self)
		uploadButt.setText("     Upload a Video")
		uploadButt.clicked.connect(lambda: self.ClickSideButt('upload'))
		uploadButt.setGeometry(1600,425,220,50)
		uploadButt.setFont(QFont('Times',12))
		uploadButt.setStyleSheet("background-color : white") 
		uploadButt.setIcon(QIcon('imgs/icon.png'))
		uploadButt.setIconSize(QtCore.QSize(50,50))

		ManageButt = QtWidgets.QPushButton(self)
		ManageButt.setText("    Manage Account")
		ManageButt.clicked.connect(lambda: self.ClickSideButt('manageAcc'))
		ManageButt.setGeometry(1600,350,220,50)
		ManageButt.setFont(QFont('Times',12))
		ManageButt.setStyleSheet("background-color : white") 
		ManageButt.setIcon(QIcon('imgs/mngAcc.png'))
		ManageButt.setIconSize(QtCore.QSize(50,50))

		DisLiked = QtWidgets.QPushButton(self)
		DisLiked.setText("   Disliked Videos")
		DisLiked.clicked.connect(lambda: self.ClickSideButt('disliked'))
		DisLiked.setGeometry(1600,275,220,50)
		DisLiked.setFont(QFont('Times',12))
		DisLiked.setStyleSheet("background-color : white") 
		DisLiked.setIcon(QIcon('imgs/dislike.png'))
		DisLiked.setIconSize(QtCore.QSize(50,50))

		liked = QtWidgets.QPushButton(self)
		liked.setText("   Liked Videos")
		liked.clicked.connect(lambda: self.ClickSideButt('liked'))
		liked.setGeometry(1600,200,220,50)
		liked.setFont(QFont('Times',12))
		liked.setStyleSheet("background-color : white") 
		liked.setIcon(QIcon('imgs/like.png'))
		liked.setIconSize(QtCore.QSize(50,50))

		logout = QtWidgets.QPushButton(self)
		logout.setText('Log out')
		logout.setGeometry(1600,800,220,50)
		logout.setFont(QFont("Times",12, weight = QtGui.QFont.Bold))
		logout.setStyleSheet("background-color : red")
		logout.clicked.connect(self.logout)


	def logout(self):
		new_acc = Entry(self.network)
		widget.addWidget(new_acc)
		widget.setCurrentIndex(widget.currentIndex() + 1)

	def MainUI(self):
		self.IDs = []

		back = QLabel(self)
		back.setStyleSheet("border: 1px solid black;") 
		back.move(0,0)
		back.resize(1600,920)
		back.setStyleSheet("border-image : url(imgs/back2.png);")

		for y in range(0,2):
			for x in range(0,5):
				data = self.network.Recommended(self.videoCounter,self.username)
				self.videoCounter += 1

				if data == 'ERROR':
					break

				name,publisher,views,date,vidId,img = data[0],data[1],data[2],data[3],data[4],data[5]

				self.IDs.append(vidId)

				date = str(date).split('-')
				date = "{}/{}/{}".format(date[2],date[1],date[0])

				newImg = open('GuiCache/{}.png'.format(self.videoCounter),'wb') #saving the image in order to show it latter
				newImg.write(img)
				newImg.close()

				self.vid = QLabel(self) #Showing the preview img
				self.vid.setGeometry(45 + (290 * x),115 + (320 * y),210,170)
				self.vid.setStyleSheet("border-image : url(GuiCache/{}.png);".format(self.videoCounter))

				self.name = QLabel(self) #The name of the video
				self.name.setText(name)
				self.name.setGeometry(45 + (290 * x),297 + (320 * y),210,50)
				self.name.setFont(QFont("Times",11,weight = QtGui.QFont.Bold))
				self.name.setWordWrap(True)

				self.publisher = QLabel(self) #The name of the publisher
				self.publisher.setText(publisher)
				self.publisher.setGeometry(45 + (290 * x),339 + (320 * y),180,20)
				self.publisher.setFont(QFont("Times",11))

				self.viewsNdate = QLabel(self) #The number of views and the publish date
				self.viewsNdate.setText("{} views ~ {}".format(views,date))
				self.viewsNdate.setGeometry(45 + (290 * x),375 + (320 * y),180,20)


		nextButt = QtWidgets.QPushButton(self)
		nextButt.setText('->')
		nextButt.setFont(QFont('Times',12))
		nextButt.setGeometry(800,850,70,50)
		nextButt.clicked.connect(self.next_page)

		prevButt = QtWidgets.QPushButton(self)
		prevButt.setText('<-')
		prevButt.setFont(QFont('Times',12))
		prevButt.setGeometry(690,850,70,50)
		prevButt.clicked.connect(self.prev_page)

	def prev_page(self):
		if self.videoCounter >= 10: #just if in the next page than able to go back
			newPage = MainGUI(self.network,self.username)
			widget.addWidget(newPage)
			widget.setCurrentIndex(widget.currentIndex() + 1)
		else:
			return

	def next_page(self):
		newPage = MainGUI(self.network,self.username,self.videoCounter)
		widget.addWidget(newPage)
		widget.setCurrentIndex(widget.currentIndex() + 1)

	def mousePressEvent(self,event): #when presing the vid than understanding what is the id of the current vid and calling it
		xPos = event.x()
		yPos = event.y()
		counter = 0

		if xPos >= 45 and xPos <=1360 and yPos >= 115 and yPos <= 720: #checking if clicking in the button areas
			X = int((xPos - 45)/290)
			Y = int((yPos - 115)/320)
			isBrake = False
			for y in range(0,2):
				for x in range(0,5):
					if x >= X and y >= Y:
						isBrake = True
						break
					else:
						counter += 1
				if isBrake == True:
					break

			try:
				self.vidId = self.IDs[counter]
			except:
				return
				
			moreGui = MoreGUI("show,{}".format(self.vidId), self.network, self.username)
			widget.addWidget(moreGui)
			widget.setCurrentIndex(widget.currentIndex() + 1)


	def ClickSideButt(self,arg):
		moreGui = MoreGUI(arg,self.network, self.username)
		widget.addWidget(moreGui)
		widget.setCurrentIndex(widget.currentIndex() + 1)


class Canvas(FigureCanvas):
	def __init__(self,parent,graph,network,username,x = 6, y = 8):
		fig, self.ax = plt.subplots(figsize = (x,y),dpi = 100)
		super().__init__(fig)
		self.setParent(parent) 

		self.network = network
		self.username = username

		if graph == 'tags_views':
			self.tags_views_graph()
		elif graph == 'pie_creators':
			self.creators_pie()
		elif graph == 'dates_views':
			self.dates_views()

	def dates_views(self):
		data = self.network.get_dates_views(self.username) #FROMAT OF: DATE:VIEWS,DATE:VIEWS

		dates = list(data.keys())
		dates = self.sort_dates(dates)
		views = list(data.values())

		self.ax.plot(dates,views)

	def creators_pie(self):
		data = self.network.get_creators_views(self.username) #FORMAT OF: {CREATOR: HOW MANY TIMES WATCHED, CREATOR: AND SO ON}
		creators = list(data.keys())
		values = list(data.values())

		self.ax.pie(values,labels = creators)
		self.ax.set(title = 'What Publisher You Watched The Most')

	def tags_views_graph(self):
		data = self.network.get_tags_views(self.username) #FORMAT OF: {TAG:VIEWS, TAG:VIEWS}
		tags = list(data.keys()) #Xaxis

		tags = self.sort_tags(tags)

		values = list(data.values()) #Yaxis

		xLen = np.arange(len(tags))

		self.ax.bar(tags,values,0.35)
		self.ax.set(xlabel = 'tags',ylabel = 'views',title = 'Tags To Views')

	def sort_dates(self,dates):
		new_dates = []
		for date in dates:
			date = date.split('-')
			new_date = "{}/{}".format(date[2],date[1])
			new_dates.append(new_date)

		return new_dates

	def sort_tags(self,tags):
		new_tags = []
		for tag in tags:
			tag = tag.split('-')
			if tag[0] == 'Music':
				new_tags.append(tag[1])
			else:
				new_tags.append(tag[0])

		return new_tags





class MoreGUI(QWidget):
	def __init__(self,func,network,username):
		super(MoreGUI,self).__init__()
		self.network = network
		self.username = username
		self.HHoleBox = QHBoxLayout()
		self.VSideBar = QVBoxLayout()

		self.func = func.split(',')

		if self.func[0] == "upload":
			self.Upload()
		elif self.func[0] == 'liked':
			self.Like()
		elif self.func[0] == 'disliked':
			self.Like(True)
		elif self.func[0] == 'manageAcc':
			self.Acc()

		if self.func[0] == 'show':
			self.ShowVid(self.func[1])

		self.SideBarUI()

		self.setLayout(self.HHoleBox)
		

	def ShowVid(self, vidId): #BUILD THE WINDOW THAT SHOWS VIDEO
		data = self.network.GetVideo(vidId,self.username) #[name,publisher,view,like,dislike,date,vidData]
		video = data[6]

		newVid = open('GuiCache/{}.mp4'.format(vidId),'wb')
		newVid.write(video)
		newVid.close()

		#CREATE MEDIA PLAYER AND VIDEO WIDGETS
		self.mediaPlayer = QMediaPlayer(None,QMediaPlayer.StreamPlayback)

		self.videoWidget = QVideoWidget()

		self.playButt = QtWidgets.QPushButton(self)
		self.playButt.setEnabled(True)
		self.playButt.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay)) #CHANGE ICON WHEN PLAY AND STOP, AND DIRECTORY
		self.playButt.clicked.connect(self.play)

		self.slider = QtWidgets.QSlider(Qt.Horizontal)
		self.slider.setRange(0,0)
		self.slider.sliderMoved.connect(self.setPosition)

		self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile('GuiCache/{}.mp4'.format(vidId))))
		self.mediaPlayer.setVideoOutput(self.videoWidget)

		#CREATING INFO LABELS
		nameL = QLabel(self)
		nameL.setText(data[0])
		nameL.setFont(QFont('Times',15))

		self.like = QtWidgets.QPushButton(self)
		self.like.setText(data[3])
		self.like.clicked.connect(lambda: self.addLike(vidId))
		self.like.setIcon(QIcon('imgs/like.png'))
		self.like.setIconSize(QtCore.QSize(50,50))

		self.dislike = QtWidgets.QPushButton(self)
		self.dislike.setText(data[4])
		self.dislike.clicked.connect(lambda: self.addDislike(vidId))
		self.dislike.setIcon(QIcon('imgs/dislike.png'))
		self.dislike.setIconSize(QtCore.QSize(50,50))

		self.date = QLabel(self)
		self.date.setText(f"Date of upload: {data[5]}")
		self.date.setFont(QFont('Times',15))

		self.publisher = QLabel(self)
		self.publisher.setText(f"Uploaded by: {data[1]}")
		self.publisher.setFont(QFont('Times',15))

		self.views = QLabel(self)
		self.views.setText(f"{data[2]} views")
		self.views.setFont(QFont('Times',15))


		#CREATING LAYOUTS AND PLACING EVERYTHING
		hboxLayout = QHBoxLayout()
		hboxLayout.addWidget(self.playButt)
		hboxLayout.addWidget(self.slider)

		nameBoxLayout = QHBoxLayout()
		nameBoxLayout.addWidget(nameL) 

		infoBoxLayout = QHBoxLayout()
		infoBoxLayout.addWidget(self.like) 
		infoBoxLayout.addWidget(self.dislike) 
		infoBoxLayout.addSpacing(950)
		infoBoxLayout.addWidget(self.date) 
		infoBoxLayout.addSpacing(50)
		infoBoxLayout.addWidget(self.views) 

		publisherBox = QHBoxLayout()
		publisherBox.addStretch(1)
		publisherBox.addWidget(self.publisher)

		vboxLayout = QVBoxLayout()
		vboxLayout.addWidget(self.videoWidget,17)
		vboxLayout.addLayout(hboxLayout,1)
		vboxLayout.addLayout(nameBoxLayout,1)
		vboxLayout.addLayout(infoBoxLayout,1)
		vboxLayout.addLayout(publisherBox,1)

		self.HHoleBox.addLayout(vboxLayout)
		self.HHoleBox.addSpacing(235)

		self.mediaPlayer.positionChanged.connect(self.positionChanged)
		self.mediaPlayer.durationChanged.connect(self.durationChanged)


	def positionChanged(self,position):
		self.slider.setValue(position)

	def durationChanged(self,duration):
		self.slider.setRange(0, duration)

	def setPosition(self,position):
		self.mediaPlayer.setPosition(position)

	def play(self):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.mediaPlayer.pause()
		else:
			self.mediaPlayer.play()


	def addLike(self,vidId):
		is_added = self.network.addLike(vidId,self.username)

		if is_added == True:
			self.like.setText(str(int(self.like.text()) + 1))

	def addDislike(self,vidId):
		is_added = self.network.addDislike(vidId,self.username)

		if is_added == True:
			self.dislike.setText(str(int(self.dislike.text()) + 1))

	def Logo(self):
		try:
			if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
				self.mediaPlayer.pause()
		except:
			pass

		mainWindow = MainGUI(self.network,self.username)
		widget.addWidget(mainWindow)
		widget.setCurrentIndex(widget.currentIndex() + 1)

	def Upload(self):
		background = QLabel(self)
		background.move(0,0)
		background.resize(1820,920)
		background.setStyleSheet("border-image : url(imgs/back2.png);")

		nameL = QLabel(self)
		nameL.setText('Please enter the name of the video: ')
		nameL.setStyleSheet('font-weight: bold; font: 17pt Times')
		nameL.move(100,50)
		nameL.resize(400,50)

		self.enterName = QLineEdit(self)
		self.enterName.setGeometry(480,55,450,40)
		font = self.enterName.font()
		font.setPointSize(17)
		self.enterName.setFont(font)

		self.vidData = b''
		self.uplVid = QtWidgets.QPushButton(self)
		self.uplVid.setGeometry(100,120,250,60)
		self.uplVid.setText('UPLOAD THE VIDEO')
		self.uplVid.setStyleSheet('font-weight: bold; font: 13pt Times; background-color :  blue; color : white')
		self.uplVid.clicked.connect(self.uploadVid)

		self.imgData = b''
		self.uplImg = QtWidgets.QPushButton(self)
		self.uplImg.setGeometry(100,200,250,60) 
		self.uplImg.setText('UPLOAD THE PREVIEW IMAGE')
		self.uplImg.setStyleSheet('font-weight: bold; font: 12pt Times; background-color : blue; color : white')
		self.uplImg.clicked.connect(self.uploadImg)

		self.sendData = QtWidgets.QPushButton(self)
		self.sendData.setGeometry(250,280,250,60)
		self.sendData.setText('UPLOAD THE VIDEO')
		self.sendData.setStyleSheet('font-weight: bold; font: 16pt Times; background-color : gray; color : white')
		self.sendData.clicked.connect(self.upload_video)

		tagsL = QLabel(self)
		tagsL.setText('CHOOSE A TAG:')
		tagsL.setStyleSheet('font-weight: bold; font: 15pt Times')
		tagsL.move(400,120)
		tagsL.resize(150,50)

		self.tags = QComboBox(self)
		self.tags.addItem('Choose a tag')
		self.tags.addItem('Music-Pop')
		self.tags.addItem('Music-Rap')
		self.tags.addItem('Music-Hip hop')
		self.tags.addItem('Music-Jazz')
		self.tags.addItem('Music-Rock')
		self.tags.addItem('Music-Classical')
		self.tags.addItem('Comedy')
		self.tags.addItem('Cars')
		self.tags.addItem('Podcast')
		self.tags.addItem('Teaching')

		self.tags.move(580,120)
		self.tags.resize(120,50)
		self.tags.setStyleSheet("font : 11pt Times; background-color : gray; color : white")
		self.tags.activated[str].connect(self.choose_banner) 

		self.inform_client = QLabel(self)
		self.inform_client.setText('')
		self.inform_client.setStyleSheet('font-weight: bold; font: 15pt Times')
		self.inform_client.move(250,400)
		self.inform_client.resize(600,120)



	def choose_banner(self,text):
		self.tag = text

	def upload_video(self):
		name = self.enterName.text()
		vid = self.vidData
		img = self.imgData
		tag = self.tag

		self.inform_client.setText('Uploading the video, please dont touch the window and wait for the upload to finish...')

		if name != '' or vid != b'' or img != b'':
			self.network.Upload([vid,name,self.username,img,tag])
			self.inform_client.setText('Upload done')


	def uploadImg(self):
		filePath, K = QFileDialog.getOpenFileName(self, 'Open Video File', 'C:\\Users\\natal\\Desktop\\Daniel\\SchooldProjects\\py\\YTproject', 'Video files (*.png)')
		try:
			file = open(filePath, 'rb')
		except:
			return
		self.imgData = file.read()

	def uploadVid(self):
		filePath, K = QFileDialog.getOpenFileName(self, 'Open Video File', 'C:\\Users\\natal\\Desktop\\Daniel\\SchooldProjects\\py\\YTproject', 'Video files (*.mp4)')
		try:
			file = open(filePath, 'rb')
		except:
			return
		self.vidData = file.read()

	def Like(self,disliked = False):
		background = QLabel(self)
		background.move(0,0)
		background.resize(1600,920)
		background.setStyleSheet("border-image : url(imgs/back2.png);")

		title = QLabel(self)

		if disliked == False:
			title.setText('Your Liked Videos: ')
		else:
			title.setText('Your Disliked Videos: ')
		title.move(650,30)
		title.resize(400,50)
		title.setStyleSheet('font-weight: bold; font: 24pt Times')

		self.Ids = []

		videoCounter = 0

		for y in range(0,2):
			for x in range(0,5):
				data = self.network.Liked(videoCounter,self.username,disliked)

				videoCounter += 1

				if data == 'ERROR':
					break

				name,publisher,views,date,vidId,img = data[0],data[1],data[2],data[3],data[4],data[5]

				self.Ids.append(vidId)

				date = str(date).split('-')
				date = "{}/{}/{}".format(date[2],date[1],date[0])

				newImg = open('GuiCache/{}.png'.format(videoCounter),'wb') #saving the image in order to show it latter
				newImg.write(img)
				newImg.close()

				self.vid = QLabel(self) #Showing the preview img
				self.vid.setGeometry(45 + (290 * x),115 + (320 * y),210,170)
				self.vid.setStyleSheet("border-image : url(GuiCache/{}.png);".format(videoCounter))

				self.name = QLabel(self) #The name of the video
				self.name.setText(name)
				self.name.setGeometry(45 + (290 * x),297 + (320 * y),210,50)
				self.name.setFont(QFont("Times",11,weight = QtGui.QFont.Bold))
				self.name.setWordWrap(True)

				self.publisher = QLabel(self) #The name of the publisher
				self.publisher.setText(publisher)
				self.publisher.setGeometry(45 + (290 * x),339 + (320 * y),180,20)
				self.publisher.setFont(QFont("Times",11))

				self.viewsNdate = QLabel(self) #The number of views and the publish date
				self.viewsNdate.setText("{} views ~ {}".format(views,date))
				self.viewsNdate.setGeometry(45 + (290 * x),375 + (320 * y),180,20)

	def mousePressEvent(self,event): #when presing the vid than understanding what is the id of the current vid and calling it
		xPos = event.x()
		yPos = event.y()
		counter = 0

		if xPos >= 45 and xPos <=1360 and yPos >= 115 and yPos <= 720: #checking if clicking in the button areas
			X = int((xPos - 45)/290)
			Y = int((yPos - 115)/320)
			isBrake = False
			for y in range(0,2):
				for x in range(0,5):
					if x >= X and y >= Y:
						isBrake = True
						break
					else:
						counter += 1
				if isBrake == True:
					break

			try:
				self.vidId = self.Ids[counter]

				moreGui = MoreGUI("show,{}".format(self.vidId), self.network, self.username)
				widget.addWidget(moreGui)
				widget.setCurrentIndex(widget.currentIndex() + 1)
			except:
				return

	def Acc(self):
		background = QLabel(self)
		background.move(0,0)
		background.resize(1600,920)
		background.setStyleSheet("border-image : url(imgs/back2.png);")

		graph1 = Canvas(self,'tags_views',self.network,self.username)
		graph1.move(10,20)

		graph2 = Canvas(self,'pie_creators',self.network,self.username,x = 8, y = 4)
		graph2.move(750,20)



	def SideBarUI(self):
		borderLabel = QLabel(self)
		borderLabel.move(1600,0)
		borderLabel.resize(220,920)
		borderLabel.setStyleSheet("border-image : url(imgs/back3.png);")
		
		logoButt = QtWidgets.QPushButton(self)
		logoButt.clicked.connect(self.Logo)
		logoButt.setGeometry(1595,10,220,150)
		logoButt.setStyleSheet("border-image : url(imgs/logo.png);")

		uploadButt = QtWidgets.QPushButton(self)
		uploadButt.setText("     Upload a Video")
		uploadButt.clicked.connect(lambda: self.ClickSideButt('upload'))
		uploadButt.setGeometry(1600,425,220,50)
		uploadButt.setFont(QFont('Times',12))
		uploadButt.setStyleSheet("background-color : white") 
		uploadButt.setIcon(QIcon('imgs/icon.png'))
		uploadButt.setIconSize(QtCore.QSize(50,50))

		ManageButt = QtWidgets.QPushButton(self)
		ManageButt.setText("    Manage Account")
		ManageButt.clicked.connect(lambda: self.ClickSideButt('manageAcc'))
		ManageButt.setGeometry(1600,350,220,50)
		ManageButt.setFont(QFont('Times',12))
		ManageButt.setStyleSheet("background-color : white") 
		ManageButt.setIcon(QIcon('imgs/mngAcc.png'))
		ManageButt.setIconSize(QtCore.QSize(50,50))

		DisLiked = QtWidgets.QPushButton(self)
		DisLiked.setText("   Disliked Videos")
		DisLiked.clicked.connect(lambda: self.ClickSideButt('disliked'))
		DisLiked.setGeometry(1600,275,220,50)
		DisLiked.setFont(QFont('Times',12))
		DisLiked.setStyleSheet("background-color : white") 
		DisLiked.setIcon(QIcon('imgs/dislike.png'))
		DisLiked.setIconSize(QtCore.QSize(50,50))

		liked = QtWidgets.QPushButton(self)
		liked.setText("   Liked Videos")
		liked.clicked.connect(lambda: self.ClickSideButt('liked'))
		liked.setGeometry(1600,200,220,50)
		liked.setFont(QFont('Times',12))
		liked.setStyleSheet("background-color : white") 
		liked.setIcon(QIcon('imgs/like.png'))
		liked.setIconSize(QtCore.QSize(50,50))

		logout = QtWidgets.QPushButton(self)
		logout.setText('Log out')
		logout.setGeometry(1600,800,220,50)
		logout.setFont(QFont("Times",12, weight = QtGui.QFont.Bold))
		logout.setStyleSheet("background-color : red")
		logout.clicked.connect(self.logout)

	def ClickSideButt(self,args):
		moreGui = MoreGUI(args,self.network, self.username)
		widget.addWidget(moreGui)
		widget.setCurrentIndex(widget.currentIndex() + 1)

	def logout(self):
		new_acc = Entry(self.network)
		widget.addWidget(new_acc)
		widget.setCurrentIndex(widget.currentIndex() + 1)


def clean_chache():
	files = os.listdir('GuiCache')
	for file in files:
		try:
			os.remove(f'GuiCache/{file}')
		except:
			pass

clean_chache()

network = Network()
app = QApplication(sys.argv)
maing = Entry(network)

widget = QtWidgets.QStackedWidget()
widget.addWidget(maing)
widget.setFixedWidth(1820)
widget.setFixedHeight(920)
widget.show()

app.exec_()

network.Disconnect()

clean_chache()
