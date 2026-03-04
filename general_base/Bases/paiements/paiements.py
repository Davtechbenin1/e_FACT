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
def cmd_paie_format(self):
	return {
		"id":self.Get_cmd_paie_ident(),
		"client id":str(),
		"solde départ client":float(),
		"montant":float(),
		"compte id":str(),
		"date d'émission":self.sc.get_today(),
		"heure d'émission":self.sc.get_hour(),
		"état de confirmation":"non confirmé",
		"annuler":dict(),
		"commande id":str(),
	}

def add_cmd_paie(self,paie_dic):
	self.up_all_cmd_paie_base(paie_dic)
	self.add_cmd_paie_to(paie_dic,self.cmd_paie_fic)

def valide_cmd_paie(self,paie_dic):
	paie_dic['état de confirmation'] = "confirmé"
	cmd_ass = self.get_cmd(paie_dic.get('id'))
	self.paie_this_cmd(cmd_ass,paie_dic)
	self.update_cmd_paie(paie_dic)

def update_cmd_paie(self,paie_dic):
	self.add_cmd_paie(paie_dic)

def up_all_cmd_paie_base(self,paie_dic):
	date = paie_dic.get("date d'émission")
	cmd_general = self.get_all_cmd_paie_base()
	cmd_general[paie_dic.get('id')] = date
	self.Save_general_data(self.cmd_paie_fic,cmd_general)

def get_cmd_paie(self,date = "",ident = None):
	if ident:
		mois = self.sc.Get_mois_of(self.sc.Get_date_of(ident))
	else:
		if not date:
			date = self.sc.get_today()
		mois = self.sc.Get_mois_of(date)
	all_dic = self.Get_details_data(self.cmd_paie_fic+mois)
	if ident:
		ident = self.redo_ident(ident)
		return all_dic.get(ident,dict())
	else:
		return all_dic

def add_cmd_paie_to(self,paie_dic):
	mois = self.sc.Get_mois_of(paie_dic.get('id'))
	self.Save_details_data(self.cmd_paie_fic+mois,paie_dic)

def get_all_cmd_paie_base(self):
	dic = self.Get_general_data(self.cmd_paie_fic)
	if not dic:
		dic = dict()
	return dic

def get_all_cmd_paie_base_of(self,date):
	cmd_general = self.get_all_cmd_paie_base()
	ident_l = list()
	for key,th_date in cmd_general.items():
		if th_date == date:
			ident_l.append(key)
	return ident_l

