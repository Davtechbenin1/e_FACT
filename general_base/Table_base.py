#Coding:utf-8
"""
	Module définissant la table de base de données général
	du logiciel

	Ici, nous avons besoin des informations concernants
	l'emplacement exacte de la donnée
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

from .Bases.clients import clients
from .Bases.cmds import cmds
from .Bases.paiements import paiements
from .Bases.livreurs import livreurs
from .Bases.stocks import stocks
from .Bases.liaison import liaison
from .Bases.publicite import publicite

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .data_ui_handler import hand

class Gen_Base_table(clients,cmds,paiements,livreurs,stocks,liaison,publicite):
# Les méthodes de communication avec la base
	from .connexion import (est_valide_json,ident_prob,Save_general_data,
		Get_general_data,Save_details_data,Get_details_data,Save_multiple_data,
		SUP_infos,Save_sup,_Save_details_data,_Get_details_data,Save_image)

# Méthode de gestion des types de connexion
	from .Local import (local_insert_data,local_get_data,local_delete_data,local_backup,
		on_message,on_open,set_error_mess,get_multiple_data)

	from .conn_type_hand import (Def_Con,Connecte_to,check_update,get_curent_apk)

	from .ident_hand import (Get_th_ident,Get_article_ident,Get_type_article_ident,
		Get_magasin_ident,Get_client_ident,Get_cmd_ident,Get_original_cmd_ident,
		Get_cmd_paie_ident,Get_liveur_ident,Get_categorie_ident,Get_conditionement_ident,
		Get_grille_ident,Get_candidat_ident)

	def __init__(self,app_instance):
		clients.__init__(self)
		cmds.__init__(self)
		paiements.__init__(self)
		livreurs.__init__(self)
		stocks.__init__(self)

		self.insert_data = self.local_insert_data
		self.get_data = self.local_get_data
		self.delete_data = self.local_delete_data
		self.th_conf_info = Get_local_json('CON_INFO')
		self.th_entreprise = "_general_info_"

		self.All_data_Table = dict()

		
		self.this_request = requests.Session()
		self.this_request.headers.update({"User-Agent": "Mozilla/5.0"})
		self.date_format = "%d-%m-%Y"
		self.format_time = "%d-%m-%Y .%H:%M:%S.%f"
		self.date_format_new = "%d-%m-%Y. %H:%M:%S"
		self.last_sync_date = "01-01-1970 .00:00:00.00"

		self.init_session()

		self.sc = app_instance
		self.SCREEN = app_instance
		self.sc.DB = self

		self.UI_hand = hand(app_instance)
		self.my_init()

	def init_session(self):
		self.session = requests.Session()

		# Keep-Alive + retry
		retry = Retry(
			total=3,
			backoff_factor=0.3,
			status_forcelist=[500, 502, 503, 504]
		)
		adapter = HTTPAdapter(
			max_retries=retry,
			pool_connections=50,
			pool_maxsize=50
		)
		self.session.mount("https://", adapter)
		self.session.mount("http://", adapter)
		
		self.session.headers.update({
			"Accept-Encoding": "gzip, deflate",
			"User-Agent": "Mozilla/5.0"
		})
		
	def my_init(self):
		self.curent_access = "all"
		self.th_access = 'all'
		self.sep = '/++/++/'
		self.cache_lock = dict()
		self.last_updated_at = dict()

		self.commande_histo_liste = dict()

		self.article_fic = 'Article'
		self.type_article_fic = "type d'article"
		self.magasin_fic = "Magasins"
		self.categorie_fic = "Catégorie"
		self.autres_par = "Autres parametres"
		self.commande_fic = "Commandes"
		self.commande_org_fic = "Commandes_original"
		self.client_fic = "Clients"
		self.cmd_paie_fic = "Reglement commande"
		self.livreur_fic = 'Liveurs'
		self.zone_livraison_fic = 'Zone de livraion'
		self.liaison_fic = "liaison"
		self.candidat_fic = "Candidat"
		self.pub_fic = "Publicité"
		self.version_fic = "Versionning"

		self.Les_ind = 'INDEXES'

		self.art_dics_redone = dict()

		#"""
		self.all_important_table = ["general","Bénin",]
		self.Def_Con()

	def get_all_tab(self,liste):
		t = time.time()
		for fic in liste:
			self.local_get_data(fic)
		print(t-time.time())

	def excecute(self,fonc,*args):
		#fonc(*args)
		self.sc.executor.submit(fonc,*args)

	def Begin_up_data(self):
		Window.set_system_cursor("wait")

	def End_up_data(self):
		Window.set_system_cursor("arrow")

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

	def get_date_from_ident(self,num):
		return num.split("N°")[-1].split('_')[0]

	def format_part(self,liste,sep = ' -> '):
		return sep.join([y for y in liste if y])

# Donnée générales
	def Get_gen_data(self,fichier,key):
		dic = self.Get_general_data(fichier)
		if not dic:
			dic = dict()
		return dic.get(key)

	def Save_gen_data(self,fichier,key,data):
		dic = self.Get_general_data(fichier)
		if not dic:
			dic = dict()
		dic[key] = data
		self.Save_general_data(fichier,dic)

# Gestion de fichier local
	def Save_local(self,fichier,info):
		path = self.Get_path(fichier)
		with open(path,"w") as fic:
			fic.write(info)

	def Get_local(self,fichier):
		path = self.Get_path(fichier)
		try:
			with open(path,'r') as fic:
				info = fic.read()
		except:
			info = str()
		return info

	def Get_path(self,fichier):
		path = pathlib.Path().cwd()
		if ".dav" not in fichier:
			fichier = fichier + ".dav"
		path = path/fichier
		return path
				
	def Get_ind_format(self,ind):
		ind = str(ind)
		while len(ind)<6:
			ind = "0"+ind
		return ind

	def format_val(self,val):
		val = str(val)
		if val:
			pref = str()
			if val[0] == '-':
				pref = "-"
				val = val[1:]
			V = val.split('.')
			if len(V)==2:
				val = V[0]
				if int(V[-1]):
					V = "."+V[-1]
				else:
					V = str()
			else:
				val = V[0]
				V = str()
			lenf = len(val)
			ind = 3
			fr = []
			part = ['']*3
			for i in range(lenf-1,-1,-1):
				ind -= 1
				part.insert(ind,val[i])
				if ind == 0:
					fr.append(''.join(part))
					part = ['']*3
					ind = 3
			P = get_prt(part)
			if P:
				fr.append(P)
			fr.reverse()
			return pref+" ".join(fr)+V
		return val

def get_prt(part):
	P = str()
	for i in part:
		if i:
			P += i
	return P
