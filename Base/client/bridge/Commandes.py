#Coding:utf-8
from threading import Thread
import sys,os
from operator import itemgetter
from datetime import datetime
# Sauvegarde des commandes
def Save_cmd(self,cmd_dic):
	return self.save_commande(**cmd_dic)

def Get_all_commandes(self,date : str = None):
	return self.get_commande_history(date)

def Modif_this_cmd(self,cmd_dic):
	id = cmd_dic.get('N°')
	return self.update_commande(id,**cmd_dic)

def Sup_this_cmd(self,ident):
	return self.delete_commande(ident)

def Get_this_cmd(self,ident):
	dic = self.get_commande(ident)
	if dic:
		clt_dict = self.Get_this_clt(dic.get('client').strip())
		if clt_dict:
			nom = f"{clt_dict.get('nom')} {clt_dict.get('prénom')}".strip()
			dic['Nom du client'] = nom 
			try:
				dic["montant restant"] = (dic['montant TTC'] - 
					dic['montant payé'])
			except:
				...
		else:
			print(dic)

	return dic

# Gestion des historiques de paiements des commandes
def Partage_hist(self):
	dic = self.get_cmd_non_solder()
	cmds_list = dic.keys()
	self.cmd_impayer = dict()
	self.cmd_encoure = dict()
	for ident in cmds_list:
		cmd = self.Get_this_cmd(ident)
		date_end = cmd.get('date de fin contrat')
		if not date_end:
			date_end = self.sc.get_today()
		date_fin_cont = datetime.strptime(
			date_end,
			self.sc.date_format)
		to_day = datetime.strptime(
			self.sc.get_today(),
			self.sc.date_format)
		if (date_fin_cont - to_day).days < 0:
			self.cmd_impayer[cmd.get('N°')] = cmd
		else:
			self.cmd_encoure[cmd.get("N°")] = cmd

def Get_cmd_impayer(self):
	try:
		return self.cmd_impayer
	except AttributeError:
		self.Partage_hist()
		return self.cmd_impayer

def Get_cmd_encours(self):
	try:
		return self.cmd_encoure
	except AttributeError:
		self.Partage_hist()
		return self.cmd_encoure

def Get_cmd_non_sold(self):
	cmds_list = self.get_cmd_non_solder().keys()
	return {ident:self.Get_this_cmd(ident) 
		for ident in cmds_list}

# Gestion des historiques des commandes en fonctions du jours
def get_cmds_of(self,date):
	dic = self.get_commande_history()
	return dic.get(date,dict())

def get_cmds_ofs(self,date_list):
	all_dict = dict()
	cmd_all_dic = self.get_commande_history()
	for date in date_list:
		dic = cmd_all_dic.get(date,dict())
		all_dict.update(dic)
	return all_dict

def get_fact_of(self,date_list):
	all_dic = self.get_cmds_ofs(date_list)
	fact_dic = dict()
	for ident,mont in all_dic.items():
		if mont >= 0:
			fact_dic[ident] = self.Get_this_cmd(ident)
	return fact_dic

def get_fact_retour_of(self,date_list):
	all_dic = self.get_cmds_ofs(date_list)
	fact_ret_dic = dict()
	for ident,mont in all_dic.items():
		if mont < 0:
			fact_ret_dic[ident] = self.Get_this_cmd(ident)
	return fact_ret_dic



	


		



