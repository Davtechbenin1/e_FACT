#Coding:utf-8
compt_fic = "comptes"
def get_compte_format(self,date):
	#id = self.get_ident_of(self.compt_fic,False)
	dic = {
		#"N°":id,
		"libellé":str(),
		"type de compte":str(),
		"institutions":str(),
		"N° de compte":str(),
		"devise":str(),
		"solde initial":float(),
		"date de création":date,
		"responsable de la création":str(),
		"actif":True,
		"solde actuel":float(),
		"historique du solde":dict(),
		"mouvement":dict(),#Liste des ids de mouvement
		'dernier rapprochement':dict(),
		"rapprochement":dict(),
	}
	return dic
	

def save_compte(self,where,cmd_dic,date):
	th_cmd = self.get_compte_format(date)
	id = cmd_dic.get('N°')
	th_cmd.update(cmd_dic)
	th_cmd["N°"] = id
	return self.save_data(where, th_cmd, id)

def update_compte(self,where,cmd_dic):
	ident = cmd_dic.get('N°')
	return self.update_data(where, cmd_dic, ident)

def get_compte(self,where,ident:str=None):
	dic = self.get_data(where,ident)
	return dic

def delete_compte(self,where,ident):
	return self.delete_data(where,ident)

# Gestion des actions spécifiques
def save_recettes_to(self,where,ident,recettes_ident,montant,date):
	where = self.get_my_where(where,"comptes")
	compt_dic = self.get_compte(where,ident).get('data')
	mouv_ = compt_dic.get('mouvement',dict())
	mouv_.setdefault(date,dict())
	mouv_[date][recettes_ident] = montant
	compt_dic["mouvement"] = mouv_
	compt_dic = self.update_cmpt_solde(compt_dic, montant,True,date)
	self.update_compte(where,compt_dic)

def save_depenses_to(self,where,ident,depenses_ident,montant,date):
	where = self.get_my_where(where,"comptes")
	compt_dic = self.get_compte(where,ident).get('data')
	mouv_ = compt_dic.get('mouvement',dict())
	mouv_.setdefault(date,dict())
	mouv_[date][depenses_ident] = -montant
	compt_dic["mouvement"] = mouv_
	compt_dic = self.update_cmpt_solde(compt_dic, montant,False,date)
	self.update_compte(where,compt_dic)

def update_cmpt_solde(self,cmpt_dic,montant,recette :bool = False,date = None):
	if not date:
		date = self.get_today()
	histo_part = cmpt_dic.get("historique du solde",dict())
	date_part = histo_part.setdefault(date,dict())
	if not date_part:
		date_part = {
			"solde de départ":float(cmpt_dic.get('solde actuel')),
			"recettes":float(),
			"dépenses":float(),
			"solde final":float(cmpt_dic.get('solde actuel'))
		}
	if recette:
		date_part['recettes'] += montant
		date_part['solde final'] += montant

		cmpt_dic['solde actuel'] += montant
	else:
		date_part['dépenses'] += montant
		date_part['solde final'] -= montant

		cmpt_dic['solde actuel'] -= montant
	histo_part[date] = date_part
	cmpt_dic['historique du solde'] = histo_part
	return cmpt_dic
