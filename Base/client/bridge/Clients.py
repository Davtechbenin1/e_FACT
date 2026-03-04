#Coding:utf-8
import sys
import datetime

def Save_client(self,clt_dic):
	return self.save_client(**clt_dic)

def Supp_client(self,ident):
	self.delete_client(ident)

def Update_client(self,clt_dic):
	if clt_dic:
		return self.update_client(clt_dic)

def Get_this_clt(self,ident):
	if ident in self.Get_clt_list():
		ident = self.trie_client.get(ident)
	dic = self.get_client(ident)
	#print(dic)
	return dic

def Get_this_clt_solde(self,ident):
	return self.Get_this_clt(ident).get('solde',float())

def Get_clt_list(self):
	all_dic = self.get_client()
	self.trie_client = {f"{dic.get('nom')} {dic.get('prénom') or str()}".strip():dic.get('N°')
	for dic in all_dic.values()}
	return self.trie_client.keys()

def Get_this_clt_num(self,clt_name):
	dic = self.Get_this_clt(clt_name)
	return dic.get('N°')

