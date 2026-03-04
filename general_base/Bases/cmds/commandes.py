#Coding:utf-8
"""
	Gestion des commandes clients
	'''
		Principe de modification:
			Si une commande est modifié, il faut 
			garder la trace de l'originale avant de passer
			à la modification
	'''
"""
import sys
def cmd_format(self):
	return {
		"id":self.Get_cmd_ident(),
		"client id":str(),
		"montant TTC":float(),
		"montant HT":float(),
		"montant payé":float(),
		"montant restant":float(),
		"autres montants":dict(),
		"articles":dict(),
		"originale":True,
		"dernière modification":self.sc.get_today(),
		"status":{
			"de la commande":"en cours",#"en traitement","traité"
			"de la livraison":"non livrée",#"en cours de livraison", "livrée"
			"du paiement":"non soldée",#"avancée","soldée"
		},
		"chargé d'affaire":str(),
		"dates":{
			"d'émission":self.sc.get_now(),
			"de traitement":str(),
			"de départ de la livraison":str(),
			"de la livraison":str(),
			"du premier paiements":str(),
			"du dernier paiements":str(),
		},
		'zone de livraions':dict(),
		"numéro à contacter":str(),
		"historique":{
			"de modification":dict(),
			"de paiements":dict(),
		},
		"annuler":dict(),
		"date de livraions prévue":{"date":str(),
			'heure':str()},
	}

def add_cmd(self,cmd):
	self.excecute(self._add_cmd,cmd)

def _add_cmd(self,cmd):
	self.up_all_cmd_base(cmd)
	if cmd.get('originale'):
		self.add_type_of_cmd(cmd,self.commande_org_fic)
	self.add_type_of_cmd(cmd,self.commande_fic)

def update_cmd(self,cmd):
	self.add_cmd(cmd)

def get_cmd(self,date = "",ident = None):
	return self.get_type_of_cmd(self.commande_fic,
		date,ident)

def get_original_cmd(self,date = "", ident = None):
	return self.get_type_of_cmd(self.commande_org_fic,
		date,ident)

def get_type_of_cmd(self,fichier,date,ident):
	if not date:
		date = self.sc.get_today()
	mois = self.sc.Get_mois_of(date)
	all_dic = self.Get_details_data(fichier+mois)
	if not all_dic:
		all_dic = dict()
	if ident:
		ident = self.redo_ident(ident)
		return all_dic.get(ident,dict())
	else:
		return all_dic

def add_type_of_cmd(self,cmd,fichier):
	ident = cmd.get('id')
	
	mois = self.sc.Get_mois_of(self.sc.Get_date_of(ident))

	self.Save_details_data(fichier+mois,cmd)

def up_all_cmd_base(self,cmd):
	date = cmd.get('dernière modification')
	cmd_general = self.get_all_cmd_base()
	cmd_general[cmd.get('id')] = date
	clt_dic = self.get_client(cmd.get('client id'))
	dic = clt_dic.get('commandes',dict())
	dic[cmd.get('id')] = cmd.get('montant TTC')
	clt_dic['commandes'] = dic
	self.update_client(clt_dic)
	self.Save_general_data(self.commande_fic,cmd_general)

def get_all_cmd_base(self):
	dic = self.Get_general_data(self.commande_fic)
	if not dic:
		dic = dict()
	return dic

def get_all_cmd_base_of(self,date):
	cmd_general = self.get_all_cmd_base()
	ident_l = list()
	for key,th_date in cmd_general.items():
		if th_date == date:
			ident_l.append(key)
	return ident_l

def update_type_of_cmd(self,cmd,fichier):
	self.add_type_of_cmd(cmd,fichier)
