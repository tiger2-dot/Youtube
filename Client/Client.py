import socket
import json

class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
		#self.HOST = '10.100.102.2' 
		self.HOST = socket.gethostname()
		self.PORT = 5520
		self.Connect()

	def Connect(self):
		self.client.connect((self.HOST,self.PORT))

	def GetBigData(self):
		RUN = True
		SIZE_OF_PACKET = 8192

		data = b''
		while RUN:
			packet = self.client.recv(SIZE_OF_PACKET)

			howManyPacketWillBeSent = packet[0:2]
			currentPacketIndex = packet[2:4]
			actualData = packet[4:]

			data += actualData

			if howManyPacketWillBeSent <= currentPacketIndex:
				RUN = False

			self.client.send(str('a').encode()) # just sending something to let the other side know we are ready for another packet

		return data


	def CreatePacketList(self,data):
		AMOUNT_OF_DATE = 8186

		numOfPackets = int(len(data)/AMOUNT_OF_DATE) 
		listOfPackets = []

		for index in range(0,numOfPackets+1):
			packet = b''

			packet += numOfPackets.to_bytes(2, byteorder = 'big') #how many packets will be sent until full image will be done
			packet += index.to_bytes(2, byteorder = 'big') #what is the number of the current packet
			
			packet += data[AMOUNT_OF_DATE*index:AMOUNT_OF_DATE*(index+1)]

			listOfPackets.append(packet)

		return listOfPackets
		
	def GetVideo(self,vid_id,username): 
		self.client.send(str('Video,{},{}'.format(vid_id,username)).encode())

		generalInfo = self.client.recv(2048).decode() #"name,publisher,view,like,dislike,date"

		if generalInfo != 'ERROR':
			generalInfo = generalInfo.split(',')
		else:
			print ('CLIENT ERROR')
			return

		self.client.send(str('video').encode())

		vidData = self.GetBigData()

		generalInfo.append(vidData)

		return generalInfo

	def Upload(self, info): #info suppose to be like: [b'VIDEO DATA', name, publisher, b'IMAGE DATA']
		self.client.send(str('Upload,').encode())

		video = info[0]
		img = info[3]

		if self.client.recv(1024).decode() == 'ready': #READY TO RECIEVE VIDEO NAME AND PUBLISHER
			name, publisher, tag = info[1], info[2], info[4]
			names = f"{name},{publisher},{tag}"
			self.client.send(names.encode())

		if self.client.recv(1024).decode() == 'sendVideo': #READY TO RECIEVE VIDEO
			packets = self.CreatePacketList(video)
			for p in packets:
				self.client.send(p)
				self.client.recv(16)

		if self.client.recv(1024).decode() == 'sendImg': #READY TO RECIEVE IMG
			packets = self.CreatePacketList(img)
			for p in packets:
				self.client.send(p)
				self.client.recv(16)


	def Recommended(self, vidIndex,username): #vidIndex is a number: 0,1,2 and so on
		self.client.send(str("Recommended,{},{}".format(vidIndex,username)).encode())

		info = self.client.recv(2048).decode() #recieveing data at the format of: name,publisher,views,date,vidId

		if info != 'ERROR':
			info = info.split(',')
		else:
			return ('ERROR')

		self.client.send(str("Img").encode())

		img = self.GetBigData()
		info.append(img)
		
		return info #returning: [name,publisher,views,date,vidId,img]

	def Liked(self,vid_index,username,disliked = False):
		if disliked == False:
			self.client.send(str('Liked,{},{}'.format(vid_index,username)).encode())
		else:
			self.client.send(str('Disliked,{},{}'.format(vid_index,username)).encode())

		info = self.client.recv(2048).decode() #recieveing data at the format of: name,publisher,views,date,vidId

		if info != 'ERROR':
			info = info.split(',')
		else:
			return ('ERROR')

		self.client.send(str("Img").encode())

		img = self.GetBigData()
		info.append(img)
		
		return info #returning: [name,publisher,views,date,vidId,img]


	def check_user(self,username):
		self.client.send(str('User,{}'.format(username)).encode())

		is_exist = self.client.recv(32).decode()
		if is_exist == 'True':
			return True
		return False

	def add_user(self, username,password):
		self.client.send(f'Add,{username},{password}'.encode())

	def Disconnect(self): #To Disconnect
		self.client.send(str('disconnect,').encode())

	def addLike(self,vidId,username):
		self.client.send(str("Like,{},{}".format(vidId,username)).encode())

		is_added = self.client.recv(32).decode()
		if is_added == 'True':
			return True
		return False

	def addDislike(self,vidId,username):
		self.client.send(str("Dislike,{},{}".format(vidId,username)).encode())

		is_added = self.client.recv(32).decode()
		if is_added == 'True':
			return True
		return False

	def get_tags_views(self,username):
		self.client.send(str('Tags,{}'.format(username)).encode())
		data = json.loads(self.client.recv(1024).decode())
		return data

	def get_creators_views(self,username):
		self.client.send(str('Creators,{}'.format(username)).encode())
		data = json.loads(self.client.recv(1024).decode())
		return data