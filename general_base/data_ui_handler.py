#Coding:utf-8
"""
	Cet module permet de définir des méthodes de gestion
	des données via le websocket et l'interface utilisateur.
"""
from lib.davbuild import *
from General_surf import *
class hand:
	def __init__(self,sc):
		self.sc = sc

	def notify_if(self,table):
		Clock.schedule_once(partial(self.__notify_if,table
				))

	def __notify_if(self,table,dt):
		if self.sc.plateform == "desktop":
			if self.sc.DB.commande_fic.lower() in table.lower():
				if self.sc.throot.Aff_surf.menu_in_action != "Commandes":
					self.sc.add_refused_error("Il y a du nouveau au niveau des commandes")
				else:
					self.sc.throot.Aff_surf.menu_in_action = "Commandes"
					self.sc.throot.Aff_surf.add_all()
				



