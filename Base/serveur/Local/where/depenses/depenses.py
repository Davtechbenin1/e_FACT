#Coding:utf-8
"""
	Gestion des depenses de l'entreprise
"""
depense_fic = "depenses"
def get_depenses_format(self,date,heure):
	#id = self.get_ident_of(self.depense_fic,True,date)
	dic = {
		#"N°":id,
		"date":date,
		'heure':heure,
		"opérateur":str(),
		"bénéficiaire":str(),
		"comptes":str,
		"motif":str(),
		"montant":float(),
	}
	return dic

def save_depenses(self,where,depenses_dic,date,heure):
	depenses_d = self.get_depenses_format(date,heure)
	ident = depenses_dic.get('N°')
	depenses_d.update(depenses_dic)
	depenses_d["N°"] = ident
	
	info = depenses_d.get("montant")
	self._save_ident_to(where, ident, info, date)
	
	self.save_depenses_to(where,depenses_d.get('comptes'),
		ident,depenses_d.get('montant'),date)
	return self.save_data(where, depenses_d, ident)

def get_depenses(self,where,ident:str=None):
	return self.get_data(where, ident)

def delete_depenses(self,where,ident):
	return self.delete_data(where,ident)
