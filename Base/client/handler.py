#Coding:utf-8
"""
	Le main de la gestion des données
"""
from .base_table import *
from ..serveur.main import data_main
from .bridge import bridge
from lib.davbuild import *

class base_handler(bridge):
	def __init__(self,screen):
		self.sc = screen
		data_main.Get_path = self.sc.Get_path
		data_main.Save_local = self.sc.Save_local
		data_main.Get_local = self.sc.Get_local

		data_main.get_today = self.sc.get_today
		data_main.get_hour = self.sc.get_hour
		data_main.get_now = self.sc.get_now

		self._data_main_obj = data_main()

		self._data_main_obj.client_save_fournisseur = self.save_fournisseur
		self._data_main_obj.client_save_compt = self.save_comptes

		self._data_main_obj.DB.excecute = self.sc.excecute
		self._data_main_obj.check_connect = self.check_connect
		self._data_main_obj.redef_menu = self.sc.th_root.add_menu_haut
		self.check_connect()
		bridge.__init__(self)

	def check_connect(self,*args):
		self._data_main_obj.DB.check_connexion_to_sever()
		self.connected = self._data_main_obj.connected

	def get_inprogress(self):
		return self._data_main_obj.DB.Sync_in_progress

	def set_inprogesst(self,val:bool):
		self._data_main_obj.DB.Sync_in_progress = val

# Gestion des clients
	def save_client(self,**kwargs):
		if not kwargs.get('nom'):
			return "Un client sans nom ne peut être enrégistrer"
		else:
			return save_data(self,"clients",kwargs,self.sc.magasin)

	def get_client(self,id:str = None):
		return get_data(self,"clients",id,self.sc.magasin)

	def delete_client(self,id:str):
		return delete_data(self,"clients",id,self.sc.magasin)

	def update_client(self,id,**kwargs):
		return update_data(self,"clients",kwargs,id,self.sc.magasin)

# Gestion des fournisseurs
	def save_fournisseur(self,**kwargs):
		if not kwargs.get('nom'):
			return "Un fournisseur sans nom ne peut être enrégistrer"
		else:
			return save_data(self,"fournisseurs",kwargs,self.sc.magasin)

	def get_fournisseur(self,id:str = None):
		return get_data(self,"fournisseurs",id,self.sc.magasin)

	def delete_fournisseur(self,id:str):
		return delete_data(self,"fournisseurs",id,self.sc.magasin)

	def update_fournisseur(self,id,**kwargs):
		return update_data(self,"fournisseurs",kwargs,id,self.sc.magasin)

# Gestion des articles
	def save_article(self,**kwargs):
		if not kwargs.get('désignation'):
			return "Un article sans nom ne peut être enrégistrer"
		else:
			return save_data(self,"articles",kwargs,self.sc.magasin)

	def get_article(self,id:str = None):
		return get_data(self,"articles",id,self.sc.magasin)

	def delete_article(self,id:str):
		return delete_data(self,"articles",id,self.sc.magasin)

	def update_article(self,id,**kwargs):
		return update_data(self,"articles",kwargs,id,self.sc.magasin)

# Gestion des commandes
	def save_commande(self,**kwargs):
		if not kwargs.get('articles'):
			return "Une commande vide ne peut être enrégistrer"
		else:
			return save_data(self,"commandes",kwargs,self.sc.magasin)

	def get_commande(self,id:str = None):
		return get_data(self,"commandes",id,self.sc.magasin)

	def delete_commande(self,id:str):
		return delete_data(self,"commandes",id,self.sc.magasin)

	def get_commande_history(self,date:str=None):
		return get_history(self,"commandes",date,self.sc.magasin)

	def update_commande(self,id,**kwargs):
		return update_data(self,"commandes",kwargs,id,self.sc.magasin)

# Gestion des depenses
	def save_depense(self,**kwargs):
		if not kwargs.get('montant'):
			return "Une depense null ne peut être enrégistrer"
		else:
			return save_data(self,"depenses",kwargs,self.sc.magasin)

	def get_depense(self,id:str = None):
		return get_data(self,"depenses",id,self.sc.magasin)

	def delete_depense(self,id:str):
		return delete_data(self,"depenses",id,self.sc.magasin)

	def get_depense_history(self,date:str=None):
		return get_history(self,"depenses",date,self.sc.magasin)

# Gestion des recettes
	def save_recette(self,**kwargs):
		if not kwargs.get('montant'):
			return "Un recette null ne peut être enrégistrer"
		else:
			return save_data(self,"recettes",kwargs,self.sc.magasin)

	def get_recette(self,id:str = None):
		return get_data(self,"recettes",id,self.sc.magasin)

	def delete_recette(self,id:str):
		return delete_data(self,"recettes",id,self.sc.magasin)

	def get_recette_history(self,date:str=None):
		return get_history(self,"recettes",date,self.sc.magasin)

# Gestion des entreprise
	def save_entreprise(self,kwargs):
		if not kwargs.get('sigle'):
			return "Un entreprise sans nom ne peut être enrégistrer"
		else:
			return save_data(self,"entreprise",kwargs)

	def get_entreprise(self,id:str = None):
		return get_data(self,"entreprise",id)

	def delete_entreprise(self,id:str):
		return delete_data(self,"entreprise",id)

	def update_entreprise(self,kwargs):
		return update_data(self,"entreprise",kwargs,str())
	
# Gestion des familles
	def save_famille(self,**kwargs):
		return save_data(self,"famille",kwargs)

	def get_famille(self,id:str = None):
		return get_data(self,"famille",id)

	def delete_famille(self,id:str):
		return delete_data(self,"famille",id)

	def update_famille(self,id,**kwargs):
		return update_data(self,"famille",kwargs,id)

# Gestion des conditionements
	def save_conditionnement(self,**kwargs):
		return save_data(self,"conditionnement",kwargs)

	def get_conditionnement(self,id:str = None):
		return get_data(self,"conditionnement",id)

	def delete_conditionnement(self,id:str):
		return delete_data(self,"conditionnement",id)

	def update_conditionnement(self,id,**kwargs):
		return update_data(self,"conditionnement",kwargs,id)

# Gestion des arrivages
	def save_arrivage(self,**kwargs):
		if not kwargs.get('articles'):
			return "Un arrivage vide ne peut être enrégistrer"
		else:
			return save_data(self,"arrivages",kwargs,self.sc.magasin)

	def get_arrivage(self,id:str = None):
		return get_data(self,"arrivages",id,self.sc.magasin)

	def delete_arrivage(self,id:str):
		return delete_data(self,"arrivages",id,self.sc.magasin)

	def get_arrivage_history(self,date:str=None):
		return get_history(self,"arrivages",date,self.sc.magasin)

	def update_arrivage(self,id,**kwargs):
		return update_data(self,"arrivages",kwargs,id,self.sc.magasin)

# Gestion des pertes
	def save_perte(self,**kwargs):
		if not kwargs.get('articles'):
			return "Une perte vide ne peut être enrégistrer"
		else:
			return save_data(self,"pertes",kwargs,self.sc.magasin)

	def get_perte(self,id:str = None):
		return get_data(self,"pertes",id,self.sc.magasin)

	def delete_perte(self,id:str):
		return delete_data(self,"pertes",id,self.sc.magasin)

	def get_perte_history(self,date:str=None):
		return get_history(self,"pertes",date,self.sc.magasin)

	def update_perte(self,id,**kwargs):
		return update_data(self,"pertes",kwargs,id,self.sc.magasin)

# Gestion des comptes de paiements
	def save_comptes(self,**kwargs):
		return save_data(self,"comptes",kwargs,self.sc.magasin)

	def get_comptes(self,id:str = None):
		return get_data(self,"comptes",id,self.sc.magasin)

	def delete_comptes(self,id:str):
		return delete_data(self,"comptes",id,self.sc.magasin)

	def update_comptes(self,id,**kwargs):
		return update_data(self,"comptes",kwargs,id,self.sc.magasin)

# Gestion des historiques de paiement des commandes:
	def get_cmd_non_solder(self):
		dic = get_data(self,"historiquecmd","non_solder",self.sc.magasin)
		return dic.get('data')

	def get_cmd_solder(self):
		dic = get_data(self,"historiquecmd","solder",self.sc.magasin)
		return dic.get('data')

# Gestion des backups système:
	def local_backup(self):
		...
