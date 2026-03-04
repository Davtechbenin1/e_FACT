#Coding:utf-8
client_fic = 'clients'
import sys
def get_client_format(self,date):
	dic_particulier = {
		#'N°':self.get_ident_of(self.client_fic,False),
		'img':"media/logo.png",
		"nom":str(),
		"prénom":str(),
		"genre":str(),
		"type":'particulier',
		"catégorie":"standart",
		"association appartenue":str(),
		"tel":str(),
		"email":str(),
		"whatsapp":str(),
		"IFU":str(),
		"status":"Ordinaire",
		"solde":float(),
		'fin remboursement en cour':str(),
		"type de contrat":str(),
		"solde à la création":float(),
		"dernier visite":str(),
		"listes visites":list(),
		"notes":list(),
		"type de remboursement":str(),
		"chargé d'affaire":str(),
		"articles préférés":dict(),
		"familles d'articles préférées":str(),
		"pays":str(),
		"ville":str(),
		"quartier":str(),
		"maison":str(),
		"profession":str(),
		"date d'enregistrement":date,
		"commandes":list(),
		"paiements":list(),
		"vente à crédit":'Oui',
		"username":str(),
		"mot de pass":str(),
		"infos_document":dict(),
		"infos_avaliseur":dict(),
		"infos_compt_demande":dict(),
		"finance_infos":dict(),
		"historique du solde":dict()#format: date{solde de départ:,achats:,paiements:,solde final}
	}
	return dic_particulier

def save_client(self,where,data,date = None):
	if not date:
		date = self.get_today()
	th_data = self.get_client_format(date)
	info = f"""{data.get("nom")} {data.get("prénom",str())}""".strip()
	ident = data.get('N°')
	th_data.update(data)
	th_data["N°"] = ident
	img = data.get('img')
	if img:
		img = self.Save_image(img)
	data["img"] = img

	self._save_ident_to(where, ident, info,
		where)
	return self.save_data(where, th_data, ident)

def delete_client(self,where,ident):
	return self.delete_data(where,ident)

def update_client(self,where,data):
	info = f"""{data.get("nom")} {data.get("prénom",str())}""".strip()
	ident = data.get('N°')

	img = data.get('img')
	if img:
		img = self.Save_image(img)
	data["img"] = img

	self._save_ident_to(where, ident, info,
		where)
	return self.update_data(where, data, ident)

def get_client(self,where,ident: str = None):
	return self.get_data(where, ident)


# Gestion des actions spécifiques
def save_cmd_of_this_client(self,where,cmd_dic,retourn = False,date = None):
	if not date:
		date = self.get_today()
	"""
		ici, l'ancienne commande est écrasé par
		sa version modifiée
	"""
	where = self.get_my_where(where,"clients")
	clt_id = cmd_dic.get("client").strip()
	clt_dic = self.get_client(where,clt_id).get("data")
	
	clt_cmd_liste = clt_dic.get('commandes',list())
	clt_paie_liste = clt_dic.get('paiements',list())

	ident = cmd_dic.get('id de la commande')
	ident_mere = cmd_dic.get('commande mère')
	last_paie = cmd_dic.get('paiement actuel')
	status_cmd = cmd_dic.get('status de la commande')

	if ident_mere:
		if ident_mere in clt_cmd_liste:
			ind = clt_cmd_liste.index(ident_mere)
			del clt_cmd_liste[ind]
	
	#La gestion de paiement est gérée avec la base des paiements
	if status_cmd != "Livrée":
		return False
	if ident not in clt_cmd_liste or retourn:
		if not retourn:
			clt_cmd_liste.append(ident)

		mont = cmd_dic.get('montant TTC')
		asso = clt_dic.get('association appartenue')
		char = clt_dic.get("chargé d'affaire")
		if asso:
			self.Up_asso_solde(asso,mont)
		sold = clt_dic.get('solde',int())
		sold_dic = clt_dic.get('historique du solde',dict()).get(date)
		if not sold_dic:
			sold_dic = {
				"solde de départ":sold,
				"achats":float(),
				"paiements":float(),
				"solde final":float()
			}
		
		sold_dic = self.up_histo_cmd(sold_dic,cmd_dic)
		h_dic = clt_dic.get('historique du solde',dict())
		h_dic[date] = sold_dic
		clt_dic['historique du solde'] = h_dic
		if not sold:
			sold = int()
		sold += mont
		clt_dic["solde"] = sold

		article_l = cmd_dic.get("articles")
		art_di = clt_dic.get('articles préférés')
		if not art_di:
			art_di = dict()
		for art_d in article_l.values():
			nom = art_d.get('Désignation')
			art_di[art_d.get('N°')] = nom
		clt_dic['articles préférés'] = art_di
		if self.get_today() not in clt_dic.setdefault('listes visites',list()):
			clt_dic['listes visites'].append(date)

		self.update_client(where,clt_dic)
		return True
	else:
		return False

def save_paie_of_this_client(self,where,paie_dic,date = None):
	if not date:
		date = self.get_today()
	where = self.get_my_where(where,"clients")
	clt_id = paie_dic.get('client')
	clt_dic = self.get_client(where,clt_id).get('data')
	montant = paie_dic.get('montant')
	asso = clt_dic.get('association appartenue')
	if asso:
		self.Up_asso_solde(asso,-montant)
	ident = paie_dic.get('id du paiement')
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
	sold_dic = self.up_histo_pay(sold_dic,paie_dic)
	h_dic = clt_dic.get('historique du solde',dict())
	h_dic[date] = sold_dic
	clt_dic['historique du solde'] = h_dic

	solde -= float(montant)
	clt_dic['solde'] = solde
	clt_dic['paiements'].append(ident)
	
	self.update_client(where,clt_dic)

def up_histo_cmd(self,solde_dic,cmd_dic):
	mont = cmd_dic.get("montant TTC")
	solde_dic['achats'] += mont
	sold_dep = solde_dic.get('solde de départ',int())
	if not sold_dep:
		sold_dep = int()
	sold_acht = solde_dic.get('achats')
	paie = solde_dic.get('paiements')
	solde_dic["solde final"] = (sold_acht+sold_dep-paie)
	return solde_dic

def up_histo_pay(self,solde_dic,pay_dic):
	mont = pay_dic.get('montant')
	solde_dic['paiements'] += mont
	sold_dep = solde_dic.get('solde de départ',int())
	if not sold_dep:
		sold_dep = int()
	sold_acht = solde_dic.get('achats')
	paie = solde_dic.get('paiements')
	solde_dic["solde final"] = (sold_acht+sold_dep-paie)
	return solde_dic

