#Coding:utf-8
"""
	Gestion de la base Local distant
"""
from kivy.core.window import Window
import os, time, sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
from General_surf import Cache_error
import websocket, json, threading, time, sys, uuid
from kivy.uix.modalview import ModalView
import traceback,string
import functools

from lib.davbuild import *

def TH_CACHE(fonc_origin):
	@functools.wraps(fonc_origin)
	def wrapper(*args,**kwargs):
		self = args[0]
		try:
			return fonc_origin(*args,**kwargs)
		#"""
		except Exception as E:
			error = traceback.format_exc()
			error_log(error)
			Clock.schedule_once(self.set_error_mess,.1)
		#"""
	return wrapper

def set_error_mess(self,*args):
	self.sc.add_refused_error("Erreur Réseau, Opération échoué. Veillez vérifier votre connexion!")

def parse_server_time(self, iso_str: str):
	"""
	Convertit une chaîne ISO en datetime UTC, tolère les variations
	comme les millisecondes ou le 'Z' à la fin.
	"""
	if not iso_str:
		raise ValueError("parse_server_time: iso_str est vide")
	# Retirer le Z final si présent
	if iso_str.endswith('Z'):
		iso_str = iso_str[:-1]
	try:
		dt = datetime.fromisoformat(iso_str)
		# Toujours convertir en UTC
		if dt.tzinfo is None:
			dt = dt.replace(tzinfo=timezone.utc)
		else:
			dt = dt.astimezone(timezone.utc)
		return dt
	except Exception as e:
		print(f"[parse_server_time ERROR] iso_str={iso_str} -> {e}")
		return False

def update_sync_inf(self, date_list):
	"""
	Met à jour la date de dernière synchro côté client en tenant compte 
	de la date et de l'ID pour s'assurer de prendre le dernier élément
	synchronisé.
	date_list : liste de cursor strings "2026-02-19T12:34:56.789000_id_123"
	"""
	if not date_list:
		print("[update_sync_inf WARNING] Liste vide")
		return

	max_dt = None
	max_id = -1

	for cursor_str in date_list:
		iso_ts, serv_id = cursor_str.split('_id_')
		serv_id = int(serv_id)
		iso_ts_obj = self.parse_server_time(iso_ts)
		if iso_ts_obj:
			# Comparer date + id
			if (max_dt is None) or (iso_ts_obj > max_dt) or (iso_ts_obj == max_dt and serv_id > max_id):
				max_dt = iso_ts_obj
				max_id = serv_id

	if max_dt is not None:
		server_cursor = f"{max_dt.astimezone(timezone.utc).isoformat()}_id_{max_id}"
		self.sc.Save_local("Last_synchro", server_cursor)
		print(f"[update_sync_inf] Last_synchro mis à jour : {server_cursor}")
	else:
		print("[update_sync_inf ERROR] Aucune date/id valide trouvée")

def on_message(self, ws, message):
	msg = json.loads(message)
	status = msg.get('status')
	try:
		if status == 'ok':
			action = msg.get('action')
			trafic = msg.get('result')
			sync_info = (msg.get('sync_info') or {})
			sync_info = [f"{ts}_id_{id}" for id,ts in sync_info.items()]
			
			if action == "subscribe":
				self.ask_for_sync()
				return

			if action == "sync":
				if self.check_request_id(msg.get('request_id')):
					if msg.get('status') == 'ok':
						print("[SYNC\t]: Envoyé vers le serveur avec succès")
					if msg.get('status') == 'error':
						print("[SYNC\t]: Erreur coté serveur lors de l'enrégistrement de la SYNC")
						for th_msg in trafic.values():
							self.save_msg_to_sync(th_msg)
					self.update_sync_inf(sync_info)
				else:
					print("[SYNC\t]: Réçu du serveur avec succès")
					for th_msg in trafic.values():
						self.sc._local_msg_hand(th_msg)
					self.update_sync_inf(sync_info)

			elif action == "trafic":
				if self.check_request_id(msg.get('request_id')):
					self.save_sent_todat_log(msg)
					self.update_sync_inf(sync_info)
				else:
					self.sc._local_msg_hand(trafic)
					self.update_sync_inf(sync_info)

			elif action == 'get_sync':
				sync_info = list()
				
				if trafic:
					print("[GET_SYNC\t]: Donnée en cours de synchronisation...")
					for id,dic in trafic.items():
						curs = dic.get('cursor')
						sync_info.append(curs)

						info = self.sc._local_msg_hand(dic)
					print("[GET_SYNC\t]: synchronisation Terminer Base mise à jour...")

					self.update_sync_inf(sync_info)
				self.Sync_in_progress = False
				
		else:
			self.Sync_in_progress = False
			print(msg)
	except:
		format_exc = traceback.format_exc()
		print(format_exc)
		self.Sync_in_progress = False



def on_open(self, ws):
	ws.send(json.dumps({"action":"subscribe", 
		'base_name':self.Get_local("Info_gene")}))

# Obtenir le backup
#@TH_CACHE
def local_backup(self):
	if self.th_entreprise:
		headers = {"Accept":"application/zip"}
		
		with self.session.post(self.th_url+f'backup/{self.th_entreprise}',
			headers = headers,stream = True, timeout = 300) as r:
			r.raise_for_status()
			now = self.sc.get_hour()
			now = now.replace(":","_")
			file_name = 'Last_Backup'+now+'.zip'
			ppp = Path(f"backup/{self.sc.real_date()}")
			os.makedirs(ppp, exist_ok=True)
			out_put = os.path.join(ppp,file_name)
			with open(out_put,"wb") as f:
				for chunk in r.iter_content(chunk_size = 1024*1024):
					if chunk:
						f.write(chunk)

class WSClient:
	connected = False
	def __init__(self,mother , ws, entreprise):
		"""
		ws : instance websocket (ex: websocket-client)
		entreprise : nom de l'entreprise pour base_name
		"""
		self.ws = ws
		self.th_entreprise = entreprise

		# Cache local
		self.mother = mother
		self.All_data_Table = dict()

		# Dict pour stocker les réponses en attente
		self._responses = {}  # request_id -> data
		self._responses_lock = threading.Lock()
		self._lock = threading.Lock()
		self._lock_bases = dict()
		self._pending = {}        # request_id -> Event
		self._pending_lock = threading.Lock()

		# Start listener WS
		#self._listener_thread = threading.Thread(target=self._listen, daemon=True)
		#self._listener_thread.start()

	# -------------------------
	# Utilitaires
	# -------------------------
	def uuid(self):
		return str(uuid.uuid4())

	def redo_ident(self, ident):
		"""Méthode pour standardiser les identifiants"""
		if ident:
			p = "1234567890_"+string.ascii_lowercase
			th_txt = str()
			for i in ident.lower():
				if i not in p:
					i = "xx"
				th_txt += i
			return th_txt
		return None

	# -------------------------
	# Listener WebSocket
	# -------------------------
	def _listen(self):
		"""Thread qui écoute en permanence les messages du serveur"""
		while True:
			try:
				msg = self.ws.recv()
				if not msg:
					continue
				data = json.loads(msg)
				request_id = data.get("request_id")
				with self._pending_lock:
					event = self._pending.pop(request_id, None)

				if event:
					with self._responses_lock:
						self._responses[request_id] = data
					event.set()
			except Exception as e:
				print("WS listen error:", e)
				break

	# -------------------------
	# Méthode send + wait réponse
	# -------------------------
	def _send_and_wait(self, payload, timeout=10):
		request_id = payload["request_id"]
		event = threading.Event()

		with self._pending_lock:
			self._pending[request_id] = event

		# Envoi WS
		self.ws.send(json.dumps(payload))

		# Attente propre
		t = time.time()
		if not event.wait(timeout):
			with self._pending_lock:
				self._pending.pop(request_id, None)
			raise TimeoutError(f"WebSocket response timeout for {request_id}")

		with self._responses_lock:
			response = self._responses.pop(request_id, None)

		#print(response)
		#sys.exit()
		if not response:
			raise ValueError("No response received")
		if response.get("status") != "ok":
			raise ValueError(response.get("error"))

		return response.get("result", {})


	# -------------------------
	# Méthodes CRUD WebSocket
	# -------------------------
	def insert_data(self, payload):
		payload['base_name'] = self.Get_local("Info_gene")
		
		#self.ws.send(json.dumps(payload))
		result = self._send_and_wait(payload,10)

		with self._lock_bases.setdefault(th_tab_n,threading.Lock()):
			all_d = self.All_data_Table.setdefault(th_tab_n, {})
			if th_ident:
				all_d[th_ident] = data
			else:
				all_d.update(data)
			self.All_data_Table[th_tab_n] = all_d

	def get_data(self, table_name, ident=None):
		th_tab_n = self.redo_ident(table_name)
		th_ident = self.redo_ident(ident) if ident else None
		all_d = self.All_data_Table.setdefault(th_tab_n, {})
		payload = {
				"action": "get",
				"base_name": self.Get_local("Info_gene"),
				"table": th_tab_n,
				"data_ident": th_ident,
				"request_id": th_tab_n +' '+ self.uuid()
			}

		if all_d:
			if th_ident:
				inf = all_d.get(th_ident,dict())
				if inf:
					return inf
			else:
				return all_d
			
		result = self._send_and_wait(payload)

		# Mise à jour cache local
		with self._lock_bases.setdefault(th_tab_n,threading.Lock()):
			if th_ident:
				all_d[th_ident] = result
				self.All_data_Table[th_tab_n] = all_d
			else:
				self.All_data_Table[th_tab_n] = result

		return result

	def delete_data(self, payload):
		payload['base_name'] = self.Get_local("Info_gene")
		with self._lock_bases.setdefault(th_tab_n,threading.Lock()):
			if th_tab_n in self.All_data_Table:
				if isinstance(th_ident,(list,tuple)):
					for id in th_ident:
						self.All_data_Table[th_tab_n].pop(id, None)
				elif isinstance(th_ident,str):
					self.All_data_Table[th_tab_n].pop(th_ident, None)

		self.ws.send(json.dumps(payload))
