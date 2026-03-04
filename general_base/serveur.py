#Coding:utf-8
from kivy.uix.modalview import ModalView
import traceback,functools,string

from lib.davbuild import *

def redo_ident(self,ident):
	if ident:
		p = "1234567890_"+string.ascii_lowercase
		th_txt = str()
		for i in ident.lower():
			if i not in p:
				i = "xx"
			th_txt += i
		return th_txt
	return str()

def TH_CACHE(fonc_origin):
	@functools.wraps(fonc_origin)
	def wrapper(*args,**kwargs):
		try:
			return fonc_origin(*args,**kwargs)
		#"""
		except Exception as E:
			self = args[0]
			error = traceback.format_exc()
			error_log(error)
			Clock.schedule_once(self.sc.show_conn_erreur)
		#"""
	return wrapper
# Ajout de donnée
@TH_CACHE
def first_insert_data(self,part,table_name,ident,data):
	my_ident = self.redo_ident(ident)
	th_tab_n = self.redo_ident(table_name)
	if ident:
		th_data = {
			"keys":my_ident,
			"data":data
		}
	else:
		th_data = {
			"keys":None,
			"data":data
		}
	response = self.session.put(self.cloud_url+f'insert/{part}/{th_tab_n}',
		json = th_data)
	if response.status_code == 200:
		ret = response.json()
	else:
		raise ValueError (f"Erreur: {response.status_code}->{response.text}")
	
# Obtenir des données
@TH_CACHE
def first_get_data(self,part,table_name,ident = None):
	# Cette méthode met a jour directement la Table base
	th_tab_n = self.redo_ident(table_name)
	my_ident = str()
	ident_list = list()
	if ident:
		my_ident = self.redo_ident(ident)
	th_data = {
		"keys":my_ident,
	}
	response = self.session.put(self.cloud_url+f'select/{part}/{th_tab_n}',
		json = th_data)
	if response.status_code == 200:
		ret = response.json()
		return ret.get("data")
	else:
		raise ValueError (f"Erreur: {response.status_code}->{response.text}")
	
# Suppression de données
@TH_CACHE
def first_delete_data(self,part,table_name,ident):
	th_tab_n = self.redo_ident(table_name)
	my_ident = str()
	ident_list = list()
	if ident:
		my_ident = self.redo_ident(ident)
	th_data = {
		"keys":my_ident,
	}
	response = self.session.put(self.cloud_url+f'delete/{part}/{th_tab_n}',
		json = th_data)
	if response.status_code == 200:
		ret = response.json()
	else:
		raise ValueError (f"Erreur: {response.status_code}->{response.text}")
	
