#Coding:utf-8
"""
	Module de définition des fournisseurs
"""
import datetime,sys
from operator import itemgetter

def Default_fourn(self):
	fourn_d = dict()
	fourn_d['nom'] = "HABITUEL"
	fourn_d['type de fournisseur'] = 'Commerçant'
	fourn_d["secteur d'activité"] = ["Général"]
	self.Save_fournisseur(fourn_d)

# Sauvegarde des fournisseurs
def Save_fournisseur(self,fourn_dic):
	self.save_fournisseur(**fourn_dic)

def Modif_fournisseur(self,fourn_dic):
	self.update_fournisseur(fourn_dic)

def Get_fournisseur_dict(self):
	dic = self.get_fournisseur()
	if not dic:
		self.Default_fourn()
		return self.Get_fournisseur_dict()
	else:
		self.all_fourn_dic = {th_d.get("nom"):th_d.get('N°')
			for th_d in dic.values()}
		return dic

def Get_this_fournisseur(self,ident):
	return self.get_fournisseur(ident)

def Get_this_fourn_ident(self,name):
	try:
		if name in self.all_fourn_dic.keys():
			return self.all_fourn_dic.get(name)
		else:
			return name
	except AttributeError:
		self.Get_fournisseur_dict()
		return self.Get_this_fourn_ident()

def Get_fourn_by_name(self,name):
	ident = self.Get_this_fourn_ident(name)
	return self.Get_this_fournisseur(ident)

def Get_fournisseur_list(self):
	try:
		return list(self.all_fourn_dic.keys())
	except AttributeError:
		self.Get_fournisseur_dict()
		return self.Get_fournisseur_list()


