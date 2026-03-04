#Coding:utf-8
"""
	On doit laisser la mains à l'utilisateur de renseigner
	certainne information suplémentaire qu'il veux recolter
	sur ces clients.
"""

def client_format(self):
	return {
		"id":self.Get_client_ident(),
		"date d'ajout":self.sc.get_today(),
		"email":str()
	}

def format_clt_part(self,dic,part):
	part_dic = dic.get(part,dict())
	return self.format_part(part_dic.values())

def add_client(self,email):
	dics = self.Get_details_data(self.client_fic)
	email_l = [dic.get('email') for dic in dics.values()]
	if email not in email_l:
		clt_format = self.client_format()
		clt_format['email'] = email
		self.update_client(clt_format)
		return clt_format.get('id'),clt_format

def update_client(self,dic):
	self.Save_details_data(self.client_fic,dic)

def get_client(self,ident = None):
	dic = self.Get_details_data(self.client_fic)
	if ident:
		ident = self.redo_ident(ident)
		return dic.get(ident,dict())
	else:
		return dic

def get_client_by_ident(self,identifiant):
	clients = self.get_client().values()
	th_clt = [clt_dic for clt_dic in clients
		if clt_dic.get('identifiant').lower() 
			== identifiant.lower()]
	if th_clt:
		return th_clt[0]
	else:
		return dict()

def associate_clt_with_ident(self):
	all_d = self.get_client().values()
	th_dics = dict()
	for dic in all_d:
		th_dics[self.format_part(
			(dic.get('identité').get('nom'),
			dic.get('identité').get('prénom')))] = dic.get('id')
	return th_dics

# Permet d'enrégistrer les parties d'infos clients
def add_client_part(self,part,id,dic):
	clt_format = self.get_client(id)
	clt_format[part] = dic
	self.update_client(clt_format)

# Gestion des historiques clients
def save_client_vente(self,cmd_dic):
	clt_dict = self.get_client(cmd_dic.get('client id'))
	mont = cmd_dic.get('montant TTC')
	ident = cmd_dic.get('id')
	clt_dict = self.add_clt_historique(clt_dict,ident,mont)
	self.update_client(clt_dict)

def save_client_paiement(self,cmd_dic):
	clt_dict = self.get_client(cmd_dic.get('client id'))
	mont = cmd_dic.get('montant')
	ident = cmd_dic.get('id')
	clt_dict = self.add_clt_historique(clt_dict,ident,mont,False)
	self.update_client(clt_dict)

def add_clt_historique(self,clt_dict,ident,mont,achat = True):
	hist = clt_dict.get('historique')
	gene_hist = hist.get('général')
	hist_date = gene_hist.get(self.sc.get_today())
	if not hist_date:
		hist_date = {
			"solde de départ":clt_dict.get('solde'),
			"achats":float(),
			"paiements":float(),
			"solde finale":clt_dict.get('solde'),
		}
	if achat:
		hist_date['achats'] = mont
		hist_date['solde finale'] -= mont
		clt_dict['solde'] -= mont
	else:
		hist_date['paiements'] = mont
		hist_date['solde finale'] += mont
		clt_dict['solde'] += mont

	gene_hist[self.sc.get_today()] = hist_date
	hist['général'] = gene_hist
	part = "d'achat" if achat else 'des paiements'
	clt_dict['historique'] = self.add_historique_part(
		hist,part,ident,mont)
	return clt_dict

def add_historique_part(self,hist,part,ident,mont):
	part_hist = hist.get(part)
	date_hist = hist.get(self.sc.get_today())
	if not date_hist:
		date_hist = dict()
	date_hist[ident] = mont
	part_hist[self.sc.get_today()] = date_hist
	hist[part] = part_hist
	return hist

