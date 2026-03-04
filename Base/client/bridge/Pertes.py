#Coding:utf-8
"""
	Module de définition de la base de données
	des pertes.

	la gestion d'alerte se fera de façon automatique
	avec une définition stricte d'une période par défaut 
	d'alerte.
"""
import sys

def Save_perte(self,arriv_dict):
	return self.save_perte(**arriv_dict)

def Get_all_perte_id(self):
	return self.get_perte()

def Get_this_perte(self,num):
	dic = self.get_perte(num)
	if dic:
		dic["nombre d'articles"] = len(dic.get('articles'))
	else:
		dic = dict()
	return dic

def get_perte_of(self,date):
	return self.get_perte_history(date)

def get_pertes_ofs(self,date_liste):
	all_hist = self.get_perte_of(None)
	all_d = dict()
	for date in date_liste:
		d = all_hist.get(date,dict())
		all_d.update(d)
	return all_d.keys()
