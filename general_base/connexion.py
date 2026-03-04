#Coding:utf-8
import time,socket,os,sys
from datetime import datetime
import requests,json,time
from threading import Thread,Lock


from PIL import Image
from io import BytesIO

from kivy.core.window import Window
from lib.davbuild import (Save_local_json,Get_local_json)

# Méthode de sortie
def est_valide_json(self, data):
	try:
		if isinstance(data, str):
			return json.loads(data)
		elif isinstance(data, dict):
			json.dumps(data)  # teste si serialisable
			return data
		else:
			return None
	except Exception as e:
		lis = (int,float,str,dict,tuple,list)
		for k,v in data.items():
			if type(k) not in lis:
				print(k,v,sep = "->")
				self.ident_prob(k,v)
		print(data)
		print(str(e))
		return None

def ident_prob(self,th_k,v):
	lis = (int,float,str,dict,tuple,list,set)
	if type(v) == dict:
		for k,th_v in v.items():
			if type(k) not in lis:
				print(k,th_v,sep = "->")
			self.ident_prob(k,th_v)
	if type(v) not in lis:
		print(th_k,v)
	elif type(v) in (list,tuple,set):
		for th_v in v:
			self.ident_prob(th_k,v)

def Save_general_data(self,ident,th_data):
	fichier = "general"
	Window.set_system_cursor("wait")
	data = self.est_valide_json(th_data)
	if data != None:
		self.insert_data(fichier,ident,data)
	else:
		print(th_data)
		self.sc.add_refused_error('Erreur de sérérialisation donnée JSON')
	Window.set_system_cursor("arrow")

def Save_multiple_data(self,fichier,th_data):
	self.insert_data(fichier,None,th_data)
	
def Get_general_data(self,fichier):
	part = "general"
	#"""
	th_d = self.All_data_Table.get(part)
	if th_d == None:
		self.get_data(part)
		th_d = self.All_data_Table.get(part,dict())
	if fichier:
		my_ident = self.redo_ident(fichier)
		if my_ident in th_d:
			return th_d.get(my_ident)
		else:
			return self.get_data(part,my_ident)
	else:
		return th_d

def Save_details_data(self,fichier,th_data):
	fichier = self.redo_ident(fichier)
	if fichier == self.redo_ident(self.commande_fic):
		ident = th_data.get("id")
		mois = self.sc.Get_mois_of(self.sc.Get_date_of(ident))
		if mois:
			new_fic = self.commande_fic+mois
			self._Save_details_data(new_fic,th_data)
		else:
			self.sc.add_refused_error(f"identifiant non correcte '{ident}'. Informer David Systématiquement. cela est une source d'erreur grave.!")
	else:
		self._Save_details_data(fichier,th_data)

def _Save_details_data(self,fichier,th_data):
	fichier = self.redo_ident(fichier)
	Window.set_system_cursor("wait")
	data = self.est_valide_json(th_data)
	if data:
		ident = data.get('id')
		self.insert_data(fichier,ident,data)
	else:
		print(th_data)
		self.sc.add_refused_error('Erreur de sérérialisation donnée JSON')
	Window.set_system_cursor("arrow")
	
def Get_details_data(self,fichier,ident = None):
	fichier = self.redo_ident(fichier)
	dic = dict()
	if fichier == self.redo_ident(self.commande_fic):
		if ident:
			mois = self.sc.Get_mois_of(self.sc.Get_date_of(ident))
			if mois:
				new_fic = self.commande_fic+mois
				dic = self._Get_details_data(new_fic,ident)
				if not dic:
					dic = self._Get_details_data(self.commande_fic,ident)
					if dic:
						dic['Nom du client'] = self.Get_this_clt_name(dic.get('client'))
						self.Save_details_data(new_fic,dic)
			else:
				self.sc.add_refused_error(f"identifiant non correcte '{ident}'. Informer David Systématiquement. cela est une source d'erreur grave.!")
				dic = dict()
	else:
		dic = self._Get_details_data(fichier,ident)
	return dic

def _Get_details_data(self,fichier,ident):
	fichier = self.redo_ident(fichier)
	th_d = self.All_data_Table.get(fichier)
	if th_d == None:
		self.get_data(fichier)
		th_d = self.All_data_Table.get(fichier,dict())
	if ident:
		my_ident = self.redo_ident(ident)
		if my_ident in th_d:
			return th_d.get(my_ident)
		else:
			return self.get_data(fichier,my_ident)
	else:
		return th_d

# -----------------------------------------
def SUP_infos(self,ident,infos):
	T = Thread(target = self.Save_sup,
		args = (ident,infos))
	T.start()

def Save_sup(self,ident,infos):
	key = 'SUPPRESSION'
	sup_infos = Get_local_json(key)
	sup_infos[ident] = infos
	Save_local_json(key,sup_infos)

# Gestion des images
def Save_image(self, path_img):
	Window.set_system_cursor('wait')
	url = self.th_url + f'upload/{self.th_entreprise}'

	# Fichier par défaut si vide
	if not path_img:
		path_img = "media/zoemarket.jpg"
	if "http"in path_img:
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
			self.sc.add_refused_error(f"Erreur lors du traitement de l'image : {e}")
			Window.set_system_cursor('arrow')
			return path_img

	# Sinon, fichier brut (PDF, doc, etc.)
	else:
		try:
			with open(path_img, "rb") as fic:
				files = {"file": (os.path.basename(path_img), fic, "application/octet-stream")}
		except Exception as e:
			self.sc.add_refused_error(f"Erreur d'ouverture de fichier : {e}")
			Window.set_system_cursor('arrow')
			return path_img

	# Envoi vers le serveur
	try:
		response = requests.post(url, files=files, timeout=30)
	except Exception as e:
		print(e)
		self.sc.add_refused_error(f"Erreur Réseau : {e}")
		Window.set_system_cursor('arrow')
		return path_img

	# Réponse serveur
	if response.status_code == 200:
		try:
			obj = response.json()
			filename = obj.get('filename')
			if filename:
				path_img = f"{self.th_url}download/{filename}"
			else:
				self.sc.add_refused_error("Réponse invalide du serveur (pas de nom de fichier)")
		except Exception as e:
			self.sc.add_refused_error(f"Erreur de décodage JSON : {e}")
	else:
		self.sc.add_refused_error(f"Erreur lors de l'envoi du fichier : {response.status_code}")

	Window.set_system_cursor('arrow')
	return path_img


