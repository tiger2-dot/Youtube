import sqlite3
from datetime import date

class Database:
	def __init__(self):
		self.Connect()
		self.create_video_table()
		self.create_user_table()
		self.create_actions_table()
		self.create_recommendation_table()
		self.conn.commit()
		self.conn.close()

	def create_recommendation_table(self):
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'recommendations'")

		tables = len(self.cursor.fetchall())

		if tables == 0:
			self.cursor.execute("""CREATE TABLE recommendations(
				user text,
				recommendation text) """)

	def create_actions_table(self):
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'actions'")

		tables = len(self.cursor.fetchall())

		if tables == 0:
			self.cursor.execute("""CREATE TABLE actions (
				user_id integer,
				vid_id integer,
				action text)""") #like/dislike/watched

	def create_user_table(self):
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'users'")

		tables = len(self.cursor.fetchall())

		if tables == 0:
			self.cursor.execute("""CREATE TABLE users (
				user_id integer,
				username text,
				password text)""")

	def create_video_table(self):
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'video'")

		tables = len(self.cursor.fetchall())

		if tables == 0: #if table not exist, create one
			self.cursor.execute("""CREATE TABLE video(
				vid_id integer,
				Video text,
				name text,
				publisher text,
				view int,
				likee int,  
				dislike int, 
				datee text,
				image text,
				tag text)""")

	def Connect(self):
		self.conn = sqlite3.connect('DB/DataBase.db')
		self.cursor = self.conn.cursor()
	

	def add_video(self,data):
		self.Connect()
		self.cursor.executemany("INSERT INTO video VALUES (?,?,?,?,?,?,?,?,?,?)",data)
		self.conn.commit()
		self.conn.close()

	def add_user(self,data):
		self.Connect()
		self.cursor.executemany("INSERT INTO users VALUES (?,?,?)",data)
		self.conn.commit()
		self.conn.close()

	def add_action(self,user_id,vid_id,action): #action can only be : 'Like' 'Dislike' 'Watched'
		self.cursor.executemany("INSERT INTO actions VALUES (?,?,?)",[(user_id,vid_id,action)]) 
		self.conn.commit()

	def add_recommendation(self,username,rec_list):
		self.Connect()
		self.cursor.executemany("INSERT INTO recommendations VALUES (?,?)",[(username,rec_list)]) #[1,0,1,2,5]
		self.conn.commit()
		self.conn.close()

	def update_recommendation(self,username,new_rec):
		self.Connect()

		self.cursor.execute("UPDATE recommendations SET recommendation = ? WHERE user = ?",(new_rec,username))
		self.conn.commit()
		self.conn.close()

	def is_actions_done(self,user_id,action,vid_id):
		act = "'"+action+"'"

		self.cursor.execute(f"SELECT vid_id FROM actions WHERE action = ? AND user_id = ?",(act,user_id))
		values = self.cursor.fetchall()

		for value in values:
			if int(value[0]) == int(vid_id):
				return True
		return False

	def check_rec_exist(self,username):
		self.Connect()

		self.cursor.execute("SELECT recommendation FROM recommendations WHERE user = ?",(username,))
		results = self.cursor.fetchall()

		self.conn.close()

		if len(results) == 0:
			return False

		return True


	def Like(self,vidId,username):
		self.Connect()	
		userId = self.name_to_id(username)

		is_done = self.is_actions_done(userId,'Like',vidId)

		if is_done == False:
			self.cursor.execute(f"UPDATE video SET likee = {self.GetLike(vidId)[0]+1} WHERE vid_id = {vidId}")
			self.add_action(userId,vidId,'Like')
			self.conn.commit()	

		self.conn.close()

		if is_done == False: #IF LIKE WAS ADDED THEN RETURN TRUE
			return True
		return False

	def Dislike(self,vidId,username):
		self.Connect()
		userId = self.name_to_id(username)

		is_done = self.is_actions_done(userId,'Dislike',vidId)

		if is_done == False:
			self.cursor.execute(f"UPDATE video SET dislike = {self.GetDislikes(vidId)[0]+1} WHERE vid_id = {vidId}")
			self.add_action(userId,vidId,'Dislike')
			self.conn.commit()
			
		self.conn.close()

		if is_done == False: #IF LIKE WAS ADDED THEN RETURN TRUE
			return True
		return False 

	def is_user_exist(self,username):
		self.Connect()

		#NEED THE USERNAME BE LIKE 'USERNAME'
		username = "'" + username + "'" 

		self.cursor.execute("SELECT user_id FROM users WHERE username = {}".format(username))
		results = self.cursor.fetchall()

		self.conn.close()

		if len(results) != 0:
			return True
		return False

	def name_to_id(self,username):
		username = "'"+str(username)+"'"
		self.cursor.execute(f"SELECT user_id FROM users WHERE username = {username}")
		return self.cursor.fetchone()[0]

	def GetVideo(self,vidId,username,addView = True): #add one to the watched before sending data
		self.Connect()

		if addView == True:
			userId = self.name_to_id(username)

			self.cursor.execute(f"UPDATE video SET view = {self.GetViews(vidId)[0]+1} WHERE vid_id = {vidId}")
			self.add_action(userId,int(vidId),'Watched')
			self.conn.commit()

		try:
			self.cursor.execute(f"SELECT * FROM video WHERE vid_id == {vidId}")
		except:
			print ('DATABASE ERROR')
			return 'ERROR'

		returnValue = self.cursor.fetchone()
		self.conn.close()
		return returnValue


	def GetCurrVideoId(self):
		self.Connect()

		self.cursor.execute("SELECT vid_id FROM video")

		results = self.cursor.fetchall()

		self.conn.close()

		if len(results) > 0:
			return results[len(results)-1][0]
		else:
			return 0

	def get_users_curr_id(self):
		self.Connect()
		self.cursor.execute("SELECT user_id from users")
		values = self.cursor.fetchall()
		self.conn.close()
		try:
			return values[len(values)-1]
		except:
			return 0

	def get_liked_video(self,username,dislikes = False): #return a list of video id
		self.Connect()

		user_id = self.name_to_id(username)

		if dislikes == False:
			self.cursor.execute(f"SELECT vid_id FROM actions WHERE user_id = {user_id} AND action = 'Like'")
		else:
			self.cursor.execute(f"SELECT vid_id FROM actions WHERE user_id = {user_id} AND action = 'Dislike'")

		videos = self.cursor.fetchall()
		vid = []

		for video in videos:
			vid.append(video[0])

		self.conn.close()
		return vid

	def get_watched_videos(self,username):
		self.Connect()

		user_id = self.name_to_id(username)

		self.cursor.execute("SELECT vid_id FROM actions WHERE user_id = {}".format(user_id))
		values = self.cursor.fetchall()

		self.conn.close()
		return values

	def get_sorted_by_views_likes(self):
		self.Connect()

		self.cursor.execute("SELECT vid_id FROM video ORDER BY (likee/view) DESC")
		results = self.cursor.fetchall()

		self.conn.close()
		return results


	def GetLike(self,vidId):
		self.cursor.execute("SELECT likee FROM video WHERE vid_id == {}".format(vidId))
		return self.cursor.fetchone()

	def GetDislikes(self,vidId):
		self.cursor.execute("SELECT dislike FROM video WHERE vid_id == {}".format(vidId))
		return self.cursor.fetchone()

	def GetViews(self,VideoId):
		self.cursor.execute("SELECT view FROM video WHERE vid_id == {}".format(VideoId))
		return self.cursor.fetchone()

	def get_tag(self,vid_id):
		self.Connect()

		self.cursor.execute("SELECT tag FROM video WHERE vid_id = {}".format(vid_id))
		result = self.cursor.fetchone()

		self.conn.close()

		return result

	def get_user(self,vid_id):
		self.Connect()

		self.cursor.execute("SELECT publisher FROM video WHERE vid_id = {}".format(vid_id))
		result = self.cursor.fetchone()

		self.conn.close()

		return result

	def get_user_acts(self,username):
		self.Connect()

		user_id = self.name_to_id(username)

		self.cursor.execute("SELECT vid_id,action FROM actions WHERE user_id == {}".format(user_id))
		results = self.cursor.fetchall()

		self.conn.close()
		return results

	def Get_id_by_tag_creator(self,tag,creator):
		self.Connect()

		self.cursor.execute("SELECT vid_id FROM video WHERE publisher = ? AND tag = ?",(creator,tag,))
		results = self.cursor.fetchall()

		self.conn.close()
		return results

	def get_all_vids(self):
		self.Connect()

		self.cursor.execute("SELECT vid_id FROM video")
		results = self.cursor.fetchall()

		self.conn.close()
		return results

	def get_watch_list(self,username):
		self.Connect()

		self.cursor.execute("SELECT recommendation FROM recommendations WHERE user = ?",(username,))
		results = self.cursor.fetchall()

		self.conn.close()
		return results[0][0]



'''
d = Database()
a = d.get_all_vids()
print (a)
'''