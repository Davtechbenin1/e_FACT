#Coding:utf-8
from Desktop.Prog.IMPR.Impression import *
from lib.davbuild import *
def get_curent_perso(self):
	try:
		nom = f"{self.root.This_user.get('nom')} {self.root.This_user.get('prénom')}"
	except AttributeError:
		nom = 'Aziabou David'
	return nom

def get_profile_perso(self):
	nom = f"{self.root.This_user.get('nom')} {self.root.This_user.get('prénom')}"
	return nom

def Get_User_info(self):
	#try:
	dic = self.root.This_user.get('accès')
	#except AttributeError:
	#	dic = dict()
	return dic

def Get_User_menu_of(self,part,inf_dic):
	all_d = self.Get_User_info()
	if isinstance(all_d,(str,)) and all_d.lower() == "all":
		return inf_dic
	part_d = all_d.get(part,dict())
	th_inf = dict()
	for menu,surf in inf_dic.items():
		if menu in part_d:
			th_inf[menu] = surf
	
	return th_inf

def Get_liste_type_perso(self):
	perso_info = self.sc.DB.Get_all_perso_perso()
	this_liste = list()
	for i in perso_info:
		dic = self.sc.DB.Get_this_perso(i)
		dic['NOM'] = i
		this_liste.append(dic)
	
	return this_liste

def get_devers_perso(self):
	"""
		EN principe, toutes personnels administratifs
		peut faire un déversement. Lors de l'ajout de 
		personnel, on doit identifier les personels
		lambda des personnels administratifs. 
		Le déversement des commerciaux est considéré comme
		un recouvrement et gérer au niveau de la partie
		Confirmation
	"""
	liste = self.sc.DB.Get_all_perso_list()
	th_l = list()

	for ident in liste:
		obj = self.DB.Get_this_perso(ident)
		NOM = obj.get('nom') + ' ' + obj.get('prénom')
		self.Persoo_ident_dict[NOM] = ident
		th_l.append(NOM)
	return th_l

def Up_Perso_dict(self):
	all_info = self.sc.DB.Get_details_data(self.sc.DB.personnels_fic)
	for ident,dic in all_info.items():
		NOM = dic.get('nom') + ' ' + dic.get('prénom')
		self.Persoo_ident_dict[NOM] = ident
		
def Get_this_perso_ident(self,nom):
	ident = self.Persoo_ident_dict.get(nom)
	if ident:
		return ident
	return nom

def get_all_perso(self):
	return self.get_devers_perso()

def get_all_charger(self):
	liste = self.sc.DB.Get_par_post("d'affaire")
	th_l = list()
	for ident in liste:
		obj = self.DB.Get_this_perso(ident)
		NOM = obj.get('nom') + ' ' + obj.get('prénom')
		self.Persoo_ident_dict[NOM] = ident
		th_l.append(NOM)
	return th_l
