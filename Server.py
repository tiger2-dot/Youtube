import socket
import threading
import sqlite3
import json
from datetime import date
from Database import Database

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname()
PORT = 5520

server.bind((HOST,PORT))
server.listen()
print ('Server activated, waiting for connection...')

db = Database()
print ('Connected to database succesfully...')

videoCounter = db.GetCurrVideoId()

def CreatePacketList(data):
	AMOUNT_OF_DATA = 8186

	numOfPackets = int(len(data)/AMOUNT_OF_DATA) 
	listOfPackets = []

	for index in range(0,numOfPackets+1):
		packet = b''

		packet += numOfPackets.to_bytes(2, byteorder = 'big') #how many packets will be sent until full frame will be done
		packet += index.to_bytes(2, byteorder = 'big') #what is the number of the current packet
		
		packet += data[AMOUNT_OF_DATA*index:AMOUNT_OF_DATA*(index+1)]

		listOfPackets.append(packet)

	return listOfPackets


def RecieveData(client):
	RUN = True

	data = b''
	while RUN:
		packet = client.recv(8192)

		howManyPacketWillBeSent = packet[0:2]
		currentPacketIndex = packet[2:4]
		actualData = packet[4:]

		data += actualData

		if howManyPacketWillBeSent <= currentPacketIndex:
			RUN = False

		client.send(str('a').encode()) # just sending something to let the other side know we are ready for another packet

	return data

def send_packet_list(client,packet_list):
	for p in packet_list:
		client.send(p)
		client.recv(16)


def upload_video(client):
	global db
	global videoCounter

	client.send(str('ready').encode())
	data = client.recv(1024).decode().split(',') #expect to recieve: "name,publisher,tag"
	name,publisher,tag = data[0],data[1],data[2]
	client.send(str('sendVideo').encode())
	video = RecieveData(client)
	client.send(str('sendImg').encode())
	img = RecieveData(client)
	db.add_video([(videoCounter,video,name,publisher,0,0,0,date.today(),img,tag)]) #DEFYING VIEW,LIKE AND DISLIKE AS 0, DATE AS UPLOAD TIME
	print ('Succesfully added video to database with id: {}'.format(videoCounter))
	videoCounter += 1


def choose_video(client, VidId,username):
	global db
	try:
		data = db.GetVideo(VidId,username) #format of (id,b'video',name,publisher, view,like,dislike,date,b'img')
	except:
		client.send('ERROR'.encode())
		return

	generalInfo = "{},{},{},{},{},{}".format(data[2],data[3],data[4],data[5],data[6],data[7],) #name,publisher,view,like,dislike,date
	client.send(str(generalInfo).encode())

	if client.recv(16).decode() == 'video':
		video = data[1]
		send_packet_list(client,CreatePacketList(video))
		
 
def find_recommended_video(client, vid_id,username): #FUNCTION NEED TO BE CHANGED
	global db

	data = db.GetVideo(vid_id,username,False) #NEED TO CHANGE

	try:
		info = "{},{},{},{},{}".format(data[2],data[3],data[4],data[7],data[0]) #name,publisher,views,date,id
		client.send(str(info).encode())

		if client.recv(1024).decode() == 'Img': #sending the preview img
			img = data[8]
			send_packet_list(client,CreatePacketList(img))
	except:
		client.send(str('ERROR').encode())
		return
		

def add_like(client,vidId,username):
	global db
	is_added = db.Like(vidId,username)
	client.send(str(is_added).encode())

def add_dislike(client,vidId,username):
	global db
	is_added = db.Dislike(vidId,username)
	client.send(str(is_added).encode())


def check_users(client,username):
	global db

	returnValue = db.is_user_exist(username) #TRUE OR FALSE

	client.send(str(returnValue).encode())

def add_user(username,password):
	global db

	db.add_user([(db.get_users_curr_id()[0]+1,username,password)])

	print (f'User {db.get_users_curr_id()[0]+1} was added to the database succesfully')


def get_liked_videos(client,index,username,dislikes = False):
	global db

	#FIRSTLY GET A LIST OF ALL LIKED VIDEO, THAT RETURN THE ONE WE NEED
	try:
		liked_video = db.get_liked_video(username,dislikes)[int(index)]
	except:
		print ('ERROR1')
		client.send(str('ERROR').encode())
		return

	video = db.GetVideo(liked_video,username,False)

	try:
		info = "{},{},{},{},{}".format(video[2],video[3],video[4],video[7],video[0]) #name,publisher,views,date,id
		client.send(str(info).encode())

		if client.recv(1024).decode() == 'Img': #sending the preview img
			img = video[8]
			send_packet_list(client,CreatePacketList(img))
	except:
		print ('ERROR2')
		client.send(str('ERROR').encode())
		pass

def get_tags_views(client,username):
	global db

	videos_watched = db.get_watched_videos(username)

	tags_views = {}
	for vid in videos_watched:
		tag = db.get_tag(vid[0])

		if tag[0] in tags_views: #IF TAG ALREADY EXIST, ADDING THE NUMBER OF HOW MANY TIMES WATHCED BY ONE
			value = tags_views[tag[0]]
			value += 1
			tags_views[tag[0]] = value
		else: #IF TAG IS NEW THAT ADDING IT TO DICT AND ADDING ONE VIEW
			tags_views[tag[0]] = 1

	data = json.dumps(tags_views)
	client.send(data.encode())

			
def get_creators_views(client,username):
	global db

	videos_watched = db.get_watched_videos(username)

	creators_views = {}
	for vid in videos_watched:
		user = db.get_user(vid[0])

		if user[0] in creators_views: #IF TAG ALREADY EXIST, ADDING THE NUMBER OF HOW MANY TIMES WATHCED BY ONE
			value = creators_views[user[0]]
			value += 1
			creators_views[user[0]] = value
		else: #IF TAG IS NEW THAT ADDING IT TO DICT AND ADDING ONE VIEW
			creators_views[user[0]] = 1

	data = json.dumps(creators_views)
	client.send(data.encode())



def Client(client,addr):
	while True:
		data = client.recv(1024).decode().split(',') #recieveing data at the format of "COMMAND,{NUMBER OF VIDEO}/NOTHING IF NOT ASKED FOR VIDEO"

		if data[0] == 'disconnect':
			break

		elif data[0] == 'Upload':
			upload_video(client)

		elif data[0] == 'Video':
			choose_video(client, data[1],data[2])

		elif data[0] == 'Recommended':
			find_recommended_video(client,data[1],data[2])

		elif data[0] == 'Like':
			add_like(client,data[1],data[2])

		elif data[0] == 'Dislike':
			add_dislike(client,data[1],data[2])

		elif data[0] == 'User':
			check_users(client,data[1])

		elif data[0] == 'Add':
			add_user(data[1],data[2])

		elif data[0] == 'Liked':
			get_liked_videos(client, data[1],data[2])

		elif data[0] == 'Disliked':
			get_liked_videos(client,data[1],data[2],True)

		elif data[0] == 'Tags':
			get_tags_views(client,data[1])

		elif data[0] == 'Creators':
			get_creators_views(client,data[1])

	print (f"{addr[0]} disconnected")
	client.close()


def main():
	global server

	while True:

		client, addr = server.accept()
		print ("{} connected to server".format(addr[0]))

		thread = threading.Thread(target = Client,args = (client,addr,))
		thread.start()


main()
