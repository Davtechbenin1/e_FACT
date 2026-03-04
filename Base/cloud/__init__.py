#Coding:utf-8
"""
	Le pont de connexion entre le seveur cloud et 
	le serveur local
"""
import platform
import websocket, json, threading, time
import time, pathlib, requests, os
import json, sys
from kivy.core.window import Window
from threading import Thread

import string
from datetime import datetime

from PIL import Image
from io import BytesIO
from lib.davbuild import *
from .Local import (WSClient)

import concurrent.futures

class Base_table:
	request_id = int()
	from .Local import (TH_CACHE, set_error_mess, 
		on_message,on_open,local_backup,update_sync_inf,
		parse_server_time)
	
	from .conn_type_hand import (Def_Con,Connecte_to,
		check_update,get_curent_apk)

	from .cloud import (get_sync_dir,save_msg_to_sync,
		get_msg_from,send_all_general_cmds,
		get_all_sync_from,relance_conexion,
		send_to_cloud,msg_handler,_msg_handler)

	def __init__(self,app_instance):
		self._ws_client = WSClient
		
		self.this_request = requests.Session()
		self.session = self.this_request
		self._Lock = threading.Lock()
		self.date_format = "%d-%m-%Y"
		self.format_time = "%d-%m-%Y .%H:%M:%S.%f"
		self.base_dir = get_storage_dir("GSmart")
		self.last_sync_date = "01-01-1970 .00:00:00.00"

		self.sc = app_instance
		self.SCREEN = app_instance
		self.Get_path = self.sc.Get_path
		self.Save_local = self.sc.Save_local
		self.Get_local = self.sc.Get_local
		self.get_today = self.sc.get_today
		self.get_hour = self.sc.get_hour
		self.get_now = self.sc.get_now
		self.sc.DB = self


		self.Sync_in_progress = True

		self.requested_set = set()

		self.executor = concurrent.futures.ThreadPoolExecutor(
			max_workers=os.cpu_count() or 4
		)

	def save_request_id(self,request_id):
		self.requested_set.add(request_id)

	def check_request_id(self,request_id):
		return request_id in self.requested_set

	def check_connexion_to_sever(self):
		self.th_entreprise = self.Get_local("Info_gene")
		if self.th_entreprise:
			con = self.Def_Con()
			if con:
				self.sc.connected = True
			else: 
				self.sc.connected = False

	def ask_for_sync(self,*args):
		t = time.time()
		self.get_all_sync_from()
		#sys.exit()
		self.excecute(self.send_all_general_cmds)
		#self.send_all_general_cmds()

# Gestion des images
	def Save_image(self, path_img):
		Window.set_system_cursor('wait')
		url = self.th_url + 'upload/'

		# Fichier par défaut si vide
		if not path_img:
			path_img = "media/logo.png"
			return path_img
		if "http" in path_img:
			return path_img

		# Si c'est une image compressible
		if path_img.lower().endswith((".png", ".jpg", ".jpeg")):
			try:
				with Image.open(path_img) as img:
					img = img.convert("RGB")
					img.thumbnail((400, 400))

					buffer = BytesIO()
					img.save(buffer, format="JPEG", quality=70)
					buffer.seek(0)

				files = {"file": ("img.jpg", buffer, "image/jpeg")}

			except Exception as e:
				self.log(f"Erreur lors du traitement de l'image : {e}")
				Window.set_system_cursor('arrow')
				return path_img

		# Sinon, fichier brut (PDF, doc, etc.)
		else:
			try:
				with open(path_img, "rb") as fic:
					files = {"file": (os.path.basename(path_img), fic, "application/octet-stream")}
			except Exception as e:
				self.log(f"Erreur d'ouverture de fichier : {e}")
				Window.set_system_cursor('arrow')
				return path_img

		# Envoi vers le serveur
		try:
			response = self.session.post(url, files=files, timeout=30)
		except Exception as e:
			print(e)
			self.log(f"Erreur Réseau : {e}")
			Window.set_system_cursor('arrow')
			return path_img

		# Réponse serveur
		if response.status_code == 200:
			try:
				obj = response.json()
				filename = obj.get('filename')
				if filename:
					path_img = f"{self.th_url}download/{filename}"
					print(path_img)
				else:
					self.log("Réponse invalide du serveur (pas de nom de fichier)")
			except Exception as e:
				self.log(f"Erreur de décodage JSON : {e}")
		else:
			self.log(f"Erreur lors de l'envoi du fichier : {response.status_code}")

		Window.set_system_cursor('arrow')
		return path_img

# Gestion des commandes internes
	def delete_this(self,fichier):
		"""
		Supprime un fichier s'il existe
		"""
		try:
			if os.path.exists(fichier):
				os.remove(fichier)
				return True
			else:
				return False
		except Exception as e:
			print(f"[delete_this ERROR] {e}")
			return False

	def replace_this_(self, fichier):
		"""
		Renomme un fichier .gsmart en .sent avec un timestamp en préfixe
		Exemple : 167901234567890_sent.gsmart
		"""
		if not os.path.exists(fichier):
			print(f"[replace_this_] Fichier introuvable : {fichier}")
			return False

		timestamp = int(time.time() * 1_000_000)  # microsecondes pour éviter les collisions
		dossier, nom_fichier = os.path.split(fichier)
		sent_nom = nom_fichier.replace('.gsmart', '.sent')
		nouveau_nom = os.path.join(dossier, f"{timestamp}_{sent_nom}")

		try:
			os.rename(fichier, nouveau_nom)
			return nouveau_nom
		except Exception as e:
			print(f"[replace_this_] Erreur lors du renommage : {e}")
			return False


	def save_to(self, fic_name, data):
		"""
		Sauvegarde des données en JSON dans un fichier
		"""
		#try:
		# Création du dossier si nécessaire
		os.makedirs(os.path.dirname(fic_name), exist_ok=True) if os.path.dirname(fic_name) else None

		with open(fic_name, "w", encoding="utf-8") as fic:
			json.dump(data, fic, ensure_ascii=False, indent=4)
		return True
		#except Exception as e:
		#	print(f"[save_to ERROR] {e}")
		#	return False

	def get_from(self, fichier, default=None):
		"""
		Lecture JSON depuis un fichier
		"""
		if default is None:
			default = {}

		#try:
		if not os.path.exists(fichier):
			return default

		with open(fichier, "r", encoding="utf-8") as fic:
			data = json.load(fic)
		return data
		#except Exception as e:
		#	print(f"[get_from ERROR] {e}")
		#	return default


	def save_today_log(self,fic_name, data):
		os.makedirs(os.path.dirname(fic_name), exist_ok=True) if os.path.dirname(fic_name) else None
		with open(fic_name, "a") as fic:
			fic.write(
				json.dumps({
					"ts":time.time_ns(),
					"msg":data
				})+ '\n'
			)
		return True

	def get_today_log(self,fic_name):
		if not os.path.exists(fic_name):
			return {}
		data = dict()
		iteration = 0
		with open(fic_name, "r",) as fic:
			for line in fic:
				if line.strip():
					data[iteration] = json.loads(line).get('msg')
					iteration += 1
		return data

	def save_sent_todat_log(self,data):
		fic_name = f"{''.join(self.get_today().split('_'))}.sent"
		th_base_name = os.path.join(self.base_dir,'SYNC')
		th_fic_name = os.path.join(th_base_name,fic_name)
		self.save_today_log(th_fic_name,data)


		
	

