# Méthode de gestion des identifiants
def Get_th_ident(self,key,info,date = None):
	if not date:
		date = self.sc.get_today()
	this_all_ind = self.Get_gen_data(self.Les_ind,key)
	if not this_all_ind:
		this_all_ind = dict()
	today = this_all_ind.get(date,int())
	today += 1
	this_all_ind[date] = today
	self.Save_gen_data(self.Les_ind,key,this_all_ind)
	ind = self.Get_ind_format(today)
	if date == self.sc.get_today():
		id_cmd = f"{info}N°{date}_{ind}"
	else:
		id_cmd = f"{info}N°{ind}"
	return id_cmd

def Get_article_ident(self):
	return self.Get_th_ident(self.article_fic,"ART","ARTICLE")

def Get_type_article_ident(self):
	return self.Get_th_ident(self.type_article_fic,"TYART","TYPE_D_ARTICLE")

def Get_magasin_ident(self):
	return self.Get_th_ident(self.magasin_fic,"MAG","MAGASIN")

def Get_categorie_ident(self):
	return self.Get_th_ident(self.categorie_fic,"CAT","CATEGORIE")

def Get_client_ident(self):
	return self.Get_th_ident(self.client_fic,"CLT","CLIENTS")

def Get_cmd_ident(self):
	return self.Get_th_ident(self.commande_fic,"CMD")

def Get_original_cmd_ident(self):
	return self.Get_th_ident(self.commande_fic+"original","CMDORG")

def Get_cmd_paie_ident(self):
	return self.Get_th_ident(self.cmd_paie_fic,"PAIE")

def Get_liveur_ident(self):
	return self.Get_th_ident(self.livreur_fic,"AGN")

def Get_conditionement_ident(self):
	return self.Get_th_ident(self.autres_par,"COND","CONDITIONEMENT")

def Get_grille_ident(self):
	return self.Get_th_ident(self.autres_par,"GRIL","GRILLE_TARIFAIRE")

def Get_candidat_ident(self):
	return self.Get_th_ident(self.candidat_fic,"CAND")