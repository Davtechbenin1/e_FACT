#Coding:utf-8
"""
	Gestion des identifiants
"""
import sys
def _ident_hand(self,where,date):
	self.Ident_fic = "_identifiants_"
	id_dic = self.get_general_data(self.Ident_fic).get("data")

	curent = id_dic.setdefault(where,dict()).setdefault(date,1)
	id_dic[where][date] = curent+1
	self.save_general_data(id_dic,self.Ident_fic)
	return curent

def get_ident_of(self,where,apply_date = True,date = None):
	if not date:
		date = self.get_today()
	ident = f"{where[:3].upper()}{self.get_now()}"
	return ident

def _get_real_ident_to(self,where,date):
	id = self._ident_hand(where,date)
	id_str = str(id)
	while len(id_str) < 5:
		id_str = f'0{id_str}'
	return id_str

# Gestion des sauvegardes d'identifiants
def _save_ident_to(self,where,ident,info,date : str = None):
	if not date:
		date = self.get_today()
	self.Ident_save = "_save_ident_"
	id_dic = self.get_general_data(self.Ident_save).get("data")
	id_dic.setdefault(where,dict()).setdefault(date,dict())
	id_dic[where][date][ident] = info
	self.save_general_data(id_dic,self.Ident_save)

def _get_ident_from(self,where,date : str = None):
	self.Ident_save = "_save_ident_"
	id_dic = self.get_general_data(self.Ident_save).get("data")
	#print()
	#print(id_dic)
	if date:
		return id_dic.get(where,dict()).get(date,dict())
	else:
		return id_dic.get(where,dict())

def _delete_ident_from(self,where,date,ident):
	if not date:
		date = self.get_today()
	self.Ident_save = "_save_ident_"
	id_dic = self.get_general_data(self.Ident_save).get("data")
	id_dic.setdefault(where,dict()).setdefault(date,dict())
	id_dic[where][date].pop(ident,None)
	self.save_general_data(id_dic,self.Ident_save)

# Gestion des sauvegardes direct dans le général
def _save_data_to(self,where,ident,info):
	self.Data_save = "_save_data_"
	id_dic = self.get_general_data(self.Data_save).get("data")
	id_dic.setdefault(where,dict())
	id_dic[where][ident] = info
	self.save_general_data(id_dic,self.Data_save)

def _get_data_from(self,where):
	self.Data_save = "_save_data_"
	id_dic = self.get_general_data(self.Data_save).get("data")
	return id_dic.get(where,dict())

def _delete_data_from(self,where,ident):
	self.Data_save = "_save_data_"
	id_dic = self.get_general_data(self.Data_save).get("data")
	id_dic.setdefault(where,dict())
	id_dic[where].pop(ident,None)
	self.save_general_data(id_dic,self.Data_save)

