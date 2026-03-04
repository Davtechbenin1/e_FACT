#Coding:utf-8
"""
	Module de définition de la base de données
	de l'arrivage.

	la gestion d'alerte se fera de façon automatique
	avec une définition stricte d'une période par défaut 
	d'alerte.
"""
import sys

def Save_arrivage(self,arriv_dict):
	return self.save_arrivage(**arriv_dict)

def Get_all_arrivage_id(self):
	return self.get_arrivage()

def Get_this_arrivage(self,num):
	dic = self.get_arrivage(num)
	if dic:
		dic['nom fournisseur'] = self.Get_this_fournisseur(dic.get('fournisseur')).get('nom')
		dic["nombre d'articles"] = len(dic.get('articles'))
	else:
		dic = dict()
	return dic

def get_arrivage_of(self,date):
	return self.get_arrivage_history(date)

def get_arrivages_ofs(self,date_liste):
	all_hist = self.get_arrivage_of(None)
	all_d = dict()
	for date in date_liste:
		d = all_hist.get(date,dict())
		all_d.update(d)
	return all_d.keys()
