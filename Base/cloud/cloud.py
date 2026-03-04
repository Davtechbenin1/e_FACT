#Coding:utf-8
"""
	Gestion de la connexion à distance vers le serveur
	cloud.

	Deux architecture possible:
		- Une en streaming
		- Une en sauvegarde synchroniser.
"""
import os,os.path,json,uuid,traceback,websocket
from lib.davbuild import Clock

def get_sync_dir(self):
	th_base_name = os.path.join(self.base_dir,'SYNC')
	os.makedirs(th_base_name, exist_ok=True)
	return th_base_name



def save_msg_to_sync(self,msg):
	date = self.get_today().replace("-",'')
	sync_dir = self.get_sync_dir()
	general_fic_name = os.path.join(sync_dir,'general.json')
	general_fic_dic = self.get_from(general_fic_name)
	if date not in general_fic_dic:
		general_fic_dic[date]=date
		self.save_to(general_fic_name,general_fic_dic)

	date_fic = os.path.join(sync_dir,f'{date}.gsmart')
	with self._Lock:
		self.save_today_log(date_fic,msg)

def get_msg_from(self,date):
	date = date.replace("-",'')
	sync_dir = self.get_sync_dir()
	date_fic = os.path.join(sync_dir,f'{date}.gsmart')
	return self.get_today_log(date_fic)

def send_all_general_cmds(self,*args):
	sync_dir = self.get_sync_dir()
	general_fic_name = os.path.join(sync_dir,'general.json')
	general_fic_dic = self.get_from(general_fic_name)
	#print(general_fic_dic)
	keys = list(general_fic_dic.keys())

	for date in keys:
		date = date.replace("-",'')
		#print(date)
		sync_dir = self.get_sync_dir()
		date_fic = os.path.join(sync_dir,f'{date}.gsmart')
		
		date_dic = self.get_msg_from(date)
		#print(date_dic)
		request_id = f"{uuid.uuid4()}"
		sync_info = {
			"data":date_dic,
			"date_fic": date_fic,
			"date":date,
			"action":'sync',
			"base_name":self.Get_local("Info_gene"),
			"request_id":request_id
		}
		self.save_request_id(request_id)
		#self.request_id += 1
		
		ret = self.send_to_cloud(sync_info)
		if ret:
			#print(date_fic)
			self.replace_this_(date_fic)
			general_fic_dic.pop(date)
	self.save_to(general_fic_name,general_fic_dic)

def get_all_sync_from(self,*args):
	last_sync = self.sc.Get_local("Last_synchro")
	sync_info = {
		"request_id":f"{uuid.uuid4()}",
		"action":'get_sync',
		"base_name":self.Get_local("Info_gene"),
		"last_sync":last_sync
	}
	self.Sync_in_progress = True
	self.send_to_cloud(sync_info)

def send_to_cloud(self,msg):
	try:
		self.ws_client.ws.send(json.dumps(msg))
		return True
	except:
		print(traceback.format_exc())
		return False

# Gestionnaires des instruction de sauvegarde
def msg_handler(self,msg):
	msg['request_id'] = f"{uuid.uuid4()}"
	#self.excecute(self._msg_handler,msg)
	self._msg_handler(msg)

def _msg_handler(self,msg):
	action = msg.get('action').lower()
	if action in ("save","delete",'update'):
		#print(msg)
		self.last_connected_info = self.sc.connected
		if self.sc.connected:
			th_msg = {
				"request_id":f"{uuid.uuid4()}",
				"base_name":self.Get_local("Info_gene"),
				'action':"trafic",
				'data':msg
			}
			self.save_request_id(th_msg.get('request_id'))
			try:
				self.ws_client.ws.send(json.dumps(th_msg))
			except websocket._exceptions.WebSocketConnectionClosedException:
				self.save_msg_to_sync(msg)
				self.excecute(self.relance_conexion)
				#self.relance_conexion()
		else:
			#print(msg)
			self.save_msg_to_sync(msg)
			self.excecute(self.relance_conexion)
			#self.relance_conexion()

def relance_conexion(self,*args):
	self.sc.check_connect()
	if self.last_connected_info != self.sc.connected:
		self.last_connected_info = self.sc.connected
		Clock.schedule_once(self.sc.redef_menu,.01)
	
