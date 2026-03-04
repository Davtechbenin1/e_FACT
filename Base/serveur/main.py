#Coding:utf-8
from .connexion import local
import uuid, datetime, sys

from lib.serveur.DAV_BASE.MyData import date_obj

from .Local.where.arrivages import arrivages
from .Local.where.articles import articles
from .Local.where.clients import clients
from .Local.where.commandes import commandes
from .Local.where.fournisseurs import fournisseurs

from .Local.where.comptes import comptes
from .Local.where.depenses import depenses
from .Local.where.general import general
from .Local.where.pertes import pertes
from .Local.where.recettes import recettes

from lib.davbuild import get_storage_dir,os

from ..cloud import (Base_table)

class data_main(articles, clients, commandes, local,
	arrivages, fournisseurs, comptes, depenses, general, 
	recettes,pertes):
	def __init__(self):
		self.date_format = "%d-%m-%Y"
		
		local.__init__(self)
		articles.__init__(self)
		clients.__init__(self)
		commandes.__init__(self)
		general.__init__(self)
		arrivages.__init__(self)
		fournisseurs.__init__(self)
		comptes.__init__(self)
		depenses.__init__(self)
		general.__init__(self)
		recettes.__init__(self)
		pertes.__init__(self)

		self.DB = Base_table(self)
		self.base_dir = get_storage_dir("GSmart")
		self.db_path = os.path.join(self.base_dir, "gsmart.db")

		self._local_cache = dict()
		self._lock_dict = dict()
		self.created_table = set()
		self.connected = False
		self.sc = self

		self.open_local_connexion()

		self.handler_dic = {
			"clients":self.clients_handler,
			"fournisseurs":self.fournisseur_handler,
			"articles":self.articles_handler,
			'comptes':self.comptes_handler,
			
			"arrivages":self.arrivages_handler,
			"pertes":self.pertes_handler,
			"commandes":self.cmd_handler,
			"historiquecmd":self.cmd_hist_handler,

			
			"famille":self.famille_handler,
			"conditionnement":self.conditionement_handler,
			
			"recettes":self.recettes_handler,
			"depenses":self.depenses_handler,

			"entreprise":self.entreprise_handler,
		}

	def message_handler(self,msg):
		self.DB.msg_handler(msg)
		return self._local_msg_hand(msg)


	def _local_msg_hand(self,msg):
		where = msg.get('where').lower()
		where_inf = where.split("_z_o_e_")[0]
		fonc = self.handler_dic.get(where_inf)
		action = msg.get('action')
		#print(where)
		if action.lower() == "history":
			inf = self._get_ident_from(where,msg.get('id'),
				)
			return self.success_response(
				inf,where,msg.get('id'),action)

		elif fonc:
			return fonc(msg)

		else:
			return self.failed_response(
				msg.get('data'),msg.get('where'),
				msg.get('id'),msg.get('action'),
				f"Aucune action reconnue pour {where} {action}")

	def get_my_where(self,past_wh,base_name):
		th,part = past_wh.split('_z_o_e_')
		where = f'{base_name}_z_o_e_{part}'
		return where

	def Save_image(self,img):
		return img
