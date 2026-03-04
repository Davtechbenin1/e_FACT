#Coding:utf-8
"""
	Gestionnaire de stocks. c'est ici que les données à
	manipuler de la base de données du stocks sera gérer
	et mise à niveau de façon constant
"""
from Desktop.Prog.IMPR.Impression import *
from lib.davbuild import *
def Repartition_stk(self):
	self.arts_dict = self.DB.Get_all_articles()

def set_stk_compt_dic(self):
	for k,liste in self.class_par_magasin.items():
		self.cmpt_par_magasin[k] = len(liste)

	for k,liste in self.class_par_famille.items():
		self.cmpt_par_famille[k] = len(liste)

	for k,liste in self.class_par_fournisseur.items():
		self.cmpt_par_fournisseur[k] = len(liste)

def stk_of_this_magasin(self,f):
	if not f:
		return self.arts_dict
	else:
		return self.class_par_magasin.get(f,dict())

def stk_of_this_famille(self,fam):
	if not fam:
		return self.arts_dict
	else:
		return self.class_par_famille.get(fam,dict())

def stk_of_this_fournisseur(self,four):
	if  not four:
		return self.arts_dict
	else:
		return self.class_par_fournisseur.get(four,dict())

def get_magasin(self):
	return [i for i in self.DB.Get_magasin_list() if i]

def Trie_stk(self,magasin,famille,fournisseur):
	mag_dic = self.stk_of_this_magasin(magasin)
	if mag_dic:
		fam_dic = self.stk_of_this_famille(famille)
		tr_d = {i:j for i,j in mag_dic.items() if i in fam_dic}
		if tr_d:
			four_dic = self.stk_of_this_fournisseur(fournisseur)
			fil_d = {i:j for i,j in tr_d.items() if i in four_dic}
			return fil_d
		else:
			return dict()
	else:
		return dict()

def get_stk_set(self,stk,art_d):
	qte = art_d.get('qté')
	uni = art_d.get('unité')
	stk_sp = stk.split('_')
	if len(stk_sp) == 2:
		q,u = stk_sp
		return f"{q} {qte}, {u} {uni}"
	else:
		q = stk_sp
		#print(q)
		return f"{q} {qte}"

def get_art_name(self,nom):
	try:
		nom,nat = nom.split('_')
		return f"{nom} {nat}"
	except:
		nom,nat = nom.split(' ')
		return f"{nom} {nat}"

# Gestion des arrivages

def Get_arrivage_from(self,date_liste):
	liste = list()
	for date in date_liste:
		if date not in self.Arrivage_predefine:
			li = self.DB.Get_arrivage_of(date)
			self.Arrivage_predefine[date] = li
		else:
			li = self.Arrivage_predefine[date]
		liste.extend(li)
	return liste

# Gestion des pertes
def Get_perte_from(self,date_liste):
	liste = list()
	for date in date_liste:
		if date not in self.perte_predefine:
			li = self.DB.Get_perte_of(date)
			self.perte_predefine[date] = li
		else:
			li = self.perte_predefine[date]
		liste.extend(li)
	return liste

# Gestion des Inventaires
def Get_invent_from(self,date_liste):
	liste = list()
	for date in date_liste:
		if date not in self.invent_predefine:
			li = self.DB.Get_invent_of(date)
			self.invent_predefine[date] = li
		else:
			li = self.invent_predefine[date]
		liste.extend(li)
	return liste

# Gestion des Consommations internes
def Get_conso_interne_from(self,date_liste):
	liste = list()
	for date in date_liste:
		if date not in self.conso_predefine:
			li = self.DB.Get_conso_interne_of(date)
			self.conso_predefine[date] = li
		else:
			li = self.conso_predefine[date]
		liste.extend(li)
	return liste

# Gestion des transferts entres Magasins
def Get_transfert_mag_form(self,date_liste):
	liste = list()
	for date in date_liste:
		if date not in self.transfert_predefine:
			li = self.DB.Get_transfert_mag_of(date)
			self.transfert_predefine[date] = li
		else:
			li = self.transfert_predefine[date]
		liste.extend(li)
	return liste


# Mise à jour des données prédéfinie
def Up_predefinie(self):
	self.Arrivage_predefine = self.Up_this_predef(
		self.Arrivage_predefine,self.DB.Get_arrivage_of)

	self.perte_predefine = self.Up_this_predef(
		self.perte_predefine,self.DB.Get_perte_of)

	self.invent_predefine = self.Up_this_predef(
		self.invent_predefine,self.DB.Get_invent_of)

	self.conso_predefine = self.Up_this_predef(
		self.conso_predefine,self.DB.Get_conso_interne_of)

	self.transfert_predefine = self.Up_this_predef(
		self.transfert_predefine,self.DB.Get_transfert_mag_of)

def Up_this_predef(self,predef_dict,predef_fonc):
	pref = dict()
	for date,data in predef_dict.items():
		pref[date] = predef_fonc(date)
	return pref

