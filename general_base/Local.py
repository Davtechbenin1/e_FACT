#Coding:utf-8
"""
	Gestion de la base Local distant
"""
from kivy.core.window import Window
import os
from pathlib import Path
from datetime import datetime,timedelta
from General_surf import Cache_error
import websocket, json, threading, time, sys
from kivy.uix.modalview import ModalView
import traceback
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
			Clock.schedule_once(self.set_error_mess)
		#"""
	return wrapper

def set_error_mess(self,*args):
	self.sc.add_refused_error("Erreur Réseau, Opération échoué. Veillez vérifier votre connexion!")

def on_message(self, ws, message):
	mes = json.loads(message)
	table = mes.get("table")
	keys = mes.get('keys',None)
	data = mes.get('data')
	
	if not data:
		return
	if "org.kivy.android" in sys.modules or "android" in sys.modules:
		...
	else:
		try:
			self.UI_hand.notify_if(table)
		except:
			...

	if keys:
		with threading.Lock():
			th_d = self.All_data_Table.get(table, {})
			th_d[keys] = data
			self.All_data_Table[table] = th_d
	else:
		with threading.Lock():
			th_d = self.All_data_Table.get(table, {})
			for key,th_dat in data.items():
				th_d[key] = th_dat
			self.All_data_Table[table] = th_d

def on_open(self, ws):
	ws.send(json.dumps({"action":"subscribe", "table":self.th_entreprise}))

# Obtenir le backup
@TH_CACHE
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

# Ajout de donnée
@TH_CACHE
def local_insert_data(self,table_name,ident,data):
	my_ident = self.redo_ident(ident)
	th_tab_n = self.redo_ident(table_name)
	if ident:
		th_data = {
			"keys":my_ident,
			"data":data
		} #session.put(th_url+f'insert/david/
	else:
		th_data = {
			"keys":None,
			"data":data
		}
	try:
		response = self.session.put(self.th_url+f'insert/{self.th_entreprise}/{th_tab_n}',
			json = th_data, timeout = 10)
		if response.status_code == 200:
			"""
			ret = response.json()
			data = ret.get("data")
			t_dic = self.All_data_Table.get(th_tab_n,dict())
			t_dic[my_ident] = data

			self.All_data_Table[th_tab_n] = t_dic
			"""
		else:
			self.sc.add_refused_error("Erreur d'envoie")

			
	except Exception as E:
		print(E)
		self.sc.add_refused_error('Erreur Réseau')

# Obtenir des données
@TH_CACHE
def local_get_data(self,table_name,ident = None):
	# Cette méthode met a jour directement la Table base
	th_tab_n = self.redo_ident(table_name)
	my_ident = str()
	ident_list = list()
	if ident:
		my_ident = self.redo_ident(ident)
	th_data = {
		"keys":my_ident,
	}
	response = self.session.put(self.th_url+f'select/{self.th_entreprise}/{th_tab_n}',
		json = th_data, timeout = 10)
	if response.status_code == 200:
		ret = response.json()
		if ident:
			fic = th_tab_n+'((_))'+my_ident
			data = ret.get('data')
			
			all_d = self.All_data_Table.get(th_tab_n,dict())
			all_d[my_ident] = data
			self.All_data_Table[th_tab_n] = all_d

			return data 
		elif table_name == "general":
			gen_data = ret.get('data')
			for ident,val in gen_data.items():
				my_ident = self.redo_ident(ident)
				all_d = self.All_data_Table.get("general",dict())
				all_d[my_ident] = val
				self.All_data_Table['general'] = all_d
				
		else:
			gen_data = ret.get("data")
			G_data = dict()
			for ident,val in gen_data.items():
				my_ident = self.redo_ident(ident)
				fic = th_tab_n+'((_))'+ my_ident
				G_data[my_ident] = val

			self.All_data_Table[th_tab_n] = G_data
			
			return self.All_data_Table.get(th_tab_n)
	else:
		raise ValueError (f"Erreur: {response.status_code}->{response.text}")
	
@TH_CACHE
def get_multiple_data(self,table_liste):
	# Cette méthode met a jour directement la Table base
	th_tab_n = [self.redo_ident(table_name) for table_name in table_liste]
	
	th_data = {
		"table liste":th_tab_n
	}
	response = self.session.put(self.th_url+f'select/{self.th_entreprise}',
		json = th_data, timeout = 10)
	if response.status_code == 200:
		ret = response.json()
		for table,data in ret.get('data').items():
			self.All_data_Table[table] = data
		return response

	else:
		raise ValueError (f"Erreur: {response.status_code}->{response.text}")
	
# Suppression de données
@TH_CACHE
def local_delete_data(self,table_name,ident):
	th_tab_n = self.redo_ident(table_name)
	my_ident = str()
	ident_list = list()
	if ident:
		my_ident = self.redo_ident(ident)
	th_data = {
		"keys":my_ident,
	}
	response = self.session.put(self.th_url+f'delete/{self.th_entreprise}/{th_tab_n}',
		json = th_data, timeout = 10)
	if response.status_code == 200:
		ret = response.json()
		if ident:
			th_d = self.All_data_Table.get(th_tab_n,dict())
			if th_d:
				th_d[my_ident] = dict()
			self.All_data_Table[th_tab_n] = th_d
		else:
			gen_data = ret.get("data")
			G_data = dict()
			self.All_data_Table[th_tab_n] = G_data
			return self.All_data_Table.get(th_tab_n)
	else:
		raise ValueError (f"Erreur: {response.status_code}->{response.text}")
	