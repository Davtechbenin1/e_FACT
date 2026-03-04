#Coding:utf-8
"""
	Pont de gestion des données liés aux articles
"""
import pathlib, os, sys, time
from operator import itemgetter
from plyer import notification
import threading

def Save_new_art(self,art_dic):
	return self.Save_article(art_dic)

def Save_article(self,art_dic):
	return self.save_article(**art_dic)

def Get_this_art_num(self,nom):
	mon_dict = self.get_article()
	try:
		key = next(k for k, v in mon_dict.items() 
			if v.get('désignation').lower() == nom.lower().strip())
	except:
		key = nom
	return key

def Get_article_list(self):
	dic = self.get_article()
	return [art_d.get('désignation') for art_d in dic.values()]

def Get_article_list_dict(self):
	all_info = self.get_article()
	return all_info

def Get_this_article(self,nom):
	num = self.Get_this_art_num(nom)
	dic = self.get_article(num)
	return dic

def Get_famille_dict(self):
	all_family = self.get_famille()
	
	return all_family

def Set_family_dict(self,famille):
	all_family = self.Get_famille_dict()
	if famille not in all_family.values():
		self.save_famille(nom = famille)

def add_to_family_dict(self,art_dic):
	famille = art_dic.get('famille')
	if not famille:
		return
	ident = art_dic.get('N°')
	name = art_dic.get('Désignation')
	
	all_family = self.Get_famille_dict()
	th_family = all_family.setdefault(famille,dict())
	th_family[ident] = name
	all_family[famille] = th_family
	self.Save_general_data(self.family_fic, all_family)

def Update_article(self,dic):
	id = dic.get('N°')
	return self.update_article(id,**dic)

def acurate_stock(self,stocks,conditionement):
	all_stks = dict()
	th_all_stks = dict()
	if len(conditionement) == 1:
		val = int()
		for v in stocks.values():
			val += v
		return val
	for key,tup in conditionement.items():
		val,cond = tup
		if cond == None:
			stockage_pr = key
		else:
			all_stks[cond] = [val,key]
	
	new_all_stks = {stockage_pr:1}

	for key,tup in all_stks.items():
		val,cond = tup
		if key == stockage_pr:
			ref_to_stk_pr = cond
			val_to_stk_pr = val
			continue
	all_stks.pop(stockage_pr)
	lenf = len(all_stks)
	new_all_stks[ref_to_stk_pr] = val_to_stk_pr
	while lenf:
		for key,tup in all_stks.items():
			val,cond = tup
			if key == ref_to_stk_pr:
				val_to_stk_pr *= val
				stockage_pr = key
				ref_to_stk_pr = cond
				new_all_stks[ref_to_stk_pr] = val_to_stk_pr
				continue
		all_stks.pop(stockage_pr)
		lenf = len(all_stks)

	return val_to_stk_pr
