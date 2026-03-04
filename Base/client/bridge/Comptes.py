#Coding:utf-8
import sys
def Default_caisse(self):
	dic = {
		"N°":"CMPN°000001",
		"libellé":"CAISSE PRINCIPALE",
		"type de compte":"espèces",
		"institutions":"INTERNE",
		"N° de compte":"5701",
		"devise":"FCFA",
		"solde initial":float(),
		"responsable de la création":"Défault",
		"actif":True,
		"solde actuel":float(),
		"historique du solde":dict(),
		"mouvement":dict(),#Liste des ids de mouvement
		'dernier rapprochement':dict(),
		"rapprochement":dict(),
	}
	return dic

def Save_compte(self,cmpt_dic):
	self.save_comptes(**cmpt_dic)

def Get_comptes_dict(self,ident = None):
	dic = self.get_comptes()
	if not dic:
		self.Save_compte(self.Default_caisse())
		return self.Get_comptes_dict(ident)
	if ident:
		return dic.get(ident,dict())
	else:
		return dic

def Update_this_compte(self,cmpt_dic):
	self.update_comptes(cmpt_dic.get('N°'),**cmpt_dic)

def Get_this_compte(self,ident):
	return self.get_comptes(ident)

# Gestion des mouvements
def Get_mouve_of(self,ident,date:str=None):
	cmp_dic = self.get_comptes(ident)
	mouv = cmp_dic.get('mouvement',dict())
	if date:
		return mouv.get(date,dict())
	else:
		return mouv

def Get_hist_solde_of(self,ident,date : str=None):
	cmp_dic = self.get_comptes(ident)
	mouv = cmp_dic.get('historique du solde',dict())
	if date:
		return mouv.get(date,dict())
	else:
		return mouv

def Get_mouvs_of(self,ident,datelist):
	mouv_list = list()
	all_mouv = self.Get_hist_solde_of(ident)

	for date in datelist:
		mouv = all_mouv.get(date,dict())
		if mouv:
			mouv['date'] = date
			mouv_list.append(mouv)

	return mouv_list

