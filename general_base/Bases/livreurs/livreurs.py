#Coding:utf-8
"""
	Même principe de gestion que les clients
"""
def liveur_format(self):
	return {
		"id":self.Get_liveur_ident(),
		"date d'ajout":self.sc.get_today(),
		"img":'media/logo.png',
		"identifiant":str(),#Le seul qui est obligatoire.
		"solde":float(),
		"identité":{
			"nom":str(),
			"prénom":str(),
			"date de naissance":str(),
			"lieu de naissance":str(),
			"N° d'identification":str(),
		},
		"contact":{
			"téléphone":str(),
			"whatsapp":str(),
			"email":str(),
			"linkdlin":str(),
		},
		"adresse":{
			"pays":str(),
			"commune":str(),
			"arrondissement":str(),
			"quartier ou village":str(),
			"rue":str(),
			"maison":str(),
		},
		"historique":{
			"général":dict(),
			"de livraison":dict(),
			"des paiements":dict(),
		},
		"informations suplémentaire":dict(),
		"status":"actif",
	}

def add_liveur(self,identifiant):
	liv_format = self.liveur_format()
	liv_format['identifiant'] = identifiant
	self.update_liveur(liv_format)
	return liv_format.get('id')

def update_liveur(self,dic):
	self.Save_details_data(self.livreur_fic,dic)

def get_liveur(self,ident = None):
	dic = self.Get_details_data(self.livreur_fic)
	if ident:
		ident = self.redo_ident(ident)
		return dic.get(ident,dict())
	else:
		return dic

def get_liveur_list(self):
	li_dic = self.get_liveur()
	return [f"""{dic.get('identité').get("nom")} {dic.get('identité').get("prénom")}"""
		for dic in li_dic.values() if dic]
		

# Permet d'enrégistrer les parties d'infos liveurs
def add_liveur_part(self,part,id,dic):
	liv_format = self.get_liveur(id)
	liv_format[part] = dic
	self.update_liveur(liv_format)

# Gestion des historiques liveurs
def save_liveur_vente(self,cmd_dic):
	liv_dict = self.get_liveur(cmd_dic.get("chargé d'affaire"))
	mont = cmd_dic.get('montant TTC')
	ident = cmd_dic.get('id')
	liv_dict = self.add_liv_historique(liv_dict,ident,mont)
	self.update_liveur(liv_dict)

def save_liveur_paiement(self,cmd_dic,mont):
	liv_dict = self.get_liveur(cmd_dic.get("chargé d'affaire"))
	ident = cmd_dic.get('id')
	liv_dict = self.add_liv_historique(liv_dict,ident,mont,False)
	self.update_liveur(liv_dict)

def add_liv_historique(self,liv_dict,ident,mont,livraison = True):
	hist = liv_dict.get('historique')
	gene_hist = hist.get('général')
	hist_date = gene_hist.get(self.sc.get_today())
	if not hist_date:
		hist_date = {
			"solde de départ":liv_dict.get('solde'),
			"livraisons":float(),
			"paiements":float(),
			"solde finale":liv_dict.get('solde'),
		}
	if livraison:
		hist_date['livraisons'] = mont
		hist_date['solde finale'] -= mont
		liv_dict['solde'] -= mont
	else:
		hist_date['paiements'] = mont
		hist_date['solde finale'] += mont
		liv_dict['solde'] += mont

	gene_hist[self.sc.get_today()] = hist_date
	hist['général'] = gene_hist
	part = "de livraison" if livraison else 'des paiements'
	liv_dict['historique'] = self.add_historique_part(
		hist,part,ident,mont)
	return liv_dict


# Gestion des déverss candidas
def candidat_forma(self):
	return {
		"id":self.Get_candidat_ident(),
		"profile":str(),
		"zone":dict(),
		"identité":dict(),
		"infos":dict(),
	}

def add_candidat(self,dic):
	self.Save_details_data(self.candidat_fic,dic)

def get_candidat(self,ident = None):
	all_dic = self.Get_details_data(self.candidat_fic)
	if ident:
		return all_dic.get(ident)
	return all_dic



