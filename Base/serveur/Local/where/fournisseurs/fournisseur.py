#Coding:utf-8
forun_fic = 'fournisseurs'
def get_fournisseur_format(self,date):
	dic = {
		#'N°':self.get_ident_of(self.forun_fic,False),
		"nom":str(),
		"IFU":str(),
		'RCCM':str(),
		"type de fournisseur":str(),
		"secteur d'activité":list(),
		"addresse":str(),
		"solde":float(),
		"email":str(),
		"téléphone":str(),
		"whatsapp":str(),
		"personnes à contacter":dict(),
		"info paiement":{},
		"délais de paiement":str(),
		"remises négociées":{},
		"fréquence des commandes":str(),
		"condition de livraison":str(),
		'historique du solde':dict(),
		"fiabilité":int(),# En pourcentage
		"réclamation":{},
		"nom directeur":str(),
		"tél directeur":str(),
		"articles":dict(),
		"commandes":list(),
		"paiements":list()
	}
	return dic

def save_fournisseur(self,where,data,date):
	info = f"""{data.get("nom")}""".strip()
	th_data = self.get_fournisseur_format(date)
	ident = data.get('N°')
	th_data.update(data)
	th_data['N°'] = ident

	self._save_ident_to(where, ident, info,
		where)
	return self.save_data(where, th_data, ident)

def delete_fournisseur(self,where,ident):
	return self.delete_data(where,ident)

def update_fournisseur(self,where,clt_dic):
	info = f"""{clt_dic.get("nom")}""".strip()
	ident = clt_dic.get('N°')

	self._save_ident_to(where, ident, info,
		where)
	return self.update_data(where, clt_dic, ident)

def get_fournisseur(self,where,ident: str = None):
	return self.get_data(where, ident)

# Gestion des actions spécifiques
def save_cmd_of_this_fournisseur(self,where,cmd_dic,retourn = False, date = None):
	if not date:
		date = self.sc.get_today()
	"""
		ici, l'ancienne commande est écrasé par
		sa version modifiée
	"""
	where = self.get_my_where(where,"fournisseurs")
	clt_id = cmd_dic.get("fournisseur").strip()
	clt_dic = self.get_fournisseur(where,clt_id).get('data')
	
	clt_cmd_liste = clt_dic.get('commandes',list())
	clt_paie_liste = clt_dic.get('paiements',list())

	ident = cmd_dic.get('N°')
	status_cmd = cmd_dic.get('status')
	
	#La gestion de paiement est gérée avec la base des paiements
	if status_cmd != "Livrée":
		return False
	if ident not in clt_cmd_liste or retourn:
		if not retourn:
			clt_cmd_liste.append(ident)

		mont = cmd_dic.get('montant TTC')
		sold = clt_dic.get('solde',int())
		sold_dic = clt_dic.get('historique du solde',dict()).get(date)
		if not sold_dic:
			sold_dic = {
				"solde de départ":sold,
				"achats":float(),
				"paiements":float(),
				"solde final":float()
			}
		
		sold_dic = self.up_fourn_histo_cmd(sold_dic,cmd_dic)
		h_dic = clt_dic.get('historique du solde',dict())
		h_dic[date] = sold_dic
		clt_dic['historique du solde'] = h_dic
		if not sold:
			sold = int()
		sold += mont
		clt_dic["solde"] = sold

		self.update_fournisseur(where,clt_dic)
		return True
	else:
		return False

def save_paie_of_this_fournisseur(self,where,paie_dic,date = None):
	if not date:
		date = self.sc.get_today()
	where = self.get_my_where(where,"fournisseurs")
	clt_id = paie_dic.get('fournisseur')
	clt_dic = self.get_fournisseur(where,clt_id).get('data')
	montant = paie_dic.get('montant')
	ident = paie_dic.get('N°')
	solde = clt_dic["solde"]
	if not solde:
		solde = float()
	sold_dic = clt_dic.get('historique du solde',dict()).get(date)
	if not sold_dic:
		sold_dic = {
			"solde de départ":solde,
			"achats":float(),
			"paiements":float(),
			"solde final":float()
		}
	sold_dic = self.up_fourn_histo_pay(sold_dic,paie_dic)
	h_dic = clt_dic.get('historique du solde',dict())
	h_dic[date] = sold_dic
	clt_dic['historique du solde'] = h_dic

	solde -= float(montant)
	clt_dic['solde'] = solde
	clt_dic['paiements'].append(ident)
	
	self.update_fournisseur(clt_dic)

def up_fourn_histo_cmd(self,solde_dic,cmd_dic):
	mont = cmd_dic.get("montant TTC")
	solde_dic['achats'] += mont
	sold_dep = solde_dic.get('solde de départ',int())
	if not sold_dep:
		sold_dep = int()
	sold_acht = solde_dic.get('achats')
	paie = solde_dic.get('paiements')
	solde_dic["solde final"] = (sold_acht+sold_dep-paie)
	return solde_dic

def up_fourn_histo_pay(self,solde_dic,pay_dic):
	mont = pay_dic.get('montant payé')
	solde_dic['paiements'] += mont
	sold_dep = solde_dic.get('solde de départ',int())
	if not sold_dep:
		sold_dep = int()
	sold_acht = solde_dic.get('achats')
	paie = solde_dic.get('paiements')
	solde_dic["solde final"] = (sold_acht+sold_dep-paie)
	return solde_dic

