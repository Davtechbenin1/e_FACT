#Coding:utf-8
from datetime import datetime
import sys
cmd_fic = "factures"
def get_cmd_format(self,date):
	#id = self.get_ident_of(self.cmd_fic,True,date)
	dic = {
		#"id de la commande":id,
		#"N°":id,
		"client":str(),
		"montant TTC":float(),
		"autre montant":dict(),
		"montant payé":float(),
		"montant restant":float(),
		"paiements":list(),#[id paiement]
		"paiement actuel":str(),# id du dernier paiement
		"articles":list(),
		"status de la commande":str(),
		"status du paiement":"Non soldée",
		
		"date d'émission":date,
		"date de traitement":str(),
		"date de livraison":str(),
		"date d'origine":date,
		"nature d'encaissement":"Non encaissé",
		"status de la facture":"Crédit",
		"date d'encaissement":str(),

		"type de facture":str(),

		"type de contrat":str(),
		"plan de remboursement":str(),
		"date de fin contrat":str(),
		"durée du contrat":int(),#En jours
		"associations":str(),

		"commande mère":str(),
		"commande modifiée":str(),
		"date et heur de modification":str(),
		"provenance":str(),
		"auteur":str(),
		"provenance d'origine":str(),
		"auteur d'origine":str(),
		"date de traitement prévu":str(),
		"pénalité":float(),
		"options pénalité":float(),
		"plan de paiements":dict(),#Cet dictionnaire permet de définir les dates et montant à payer pour finire l'échance
	}
	return dic

def save_cmd(self,where,cmd_dic,date = None):
	if not date:
		date = self.get_today()
	cmd_d = self.get_cmd_format(date)
	ident = cmd_dic.get('N°')
	cmd_d.update(cmd_dic)
	cmd_d["N°"] = ident
	cmd_d["id de la commande"] = ident
	
	info = cmd_dic.get("montant TTC")
	self._save_ident_to(where, ident, info,date)
	
	if cmd_d.get('status de la commande').lower() == "Livrée".lower():
		self.livre_cmd(where,cmd_d,date)
		if cmd_d.get('montant TTC')<=0:
			self.save_cmd_solder(where,ident)
		else:
			self.save_cmd_non_solder(where,ident)
	return self.save_data(where, cmd_d, ident)

def update_cmd(self,where,cmd_dic):
	ident = cmd_dic.get('N°')
	info = cmd_dic.get("montant TTC")
	date = cmd_dic.get("date d'émission")
	self._save_ident_to(where, ident, info, date)
	if cmd_dic.get('status de la commande').lower() == "Livrée".lower():
		if cmd_dic.get("montant TTC") < 0:
			self.retourn_cmd(where,cmd_dic,date)
			self.save_cmd_solder(where,ident)
		elif cmd_dic.get("montant restant",float()) <= 0:
			self.save_cmd_solder(where,ident)
		else:
			self.save_cmd_non_solder(where,ident)
			self.livre_cmd(where,cmd_dic,date)
	return self.update_data(where, cmd_dic, ident)

def get_cmd(self,where,ident:str=None):
	return self.get_data(where, ident)

def delete_cmd(self,where,ident):
	cmd_dic = self.get_cmd(where,ident).get('data')
	if cmd_dic.get('status de la commande').lower() == "livrée":
		self.delete_cmd_non_solder(where,ident)
	date = cmd_dic.get("date d'émission")
	self._delete_ident_from(where,date,ident)
	return self.delete_data(where,ident)

# Gestion des actions spécifiques
def livre_cmd(self,where,cmd_dic,date):
	mont_ttc = cmd_dic.get('montant TTC')
	articles = cmd_dic.get('articles')
	cmd_iden = cmd_dic.get('N°')
	mag = cmd_dic.get('magasin')
	ret = self.save_cmd_of_this_client(where,cmd_dic, False,date)
	if ret:
		for art_dic in articles.values():
			arr,part = where.split("_z_o_e_")
			WH = f"articles_z_o_e_{part}"
			self.save_vent(WH,art_dic, mag)

def retourn_cmd(self,where,cmd_dic,date):
	mont_ttc = cmd_dic.get('montant TTC')
	articles = cmd_dic.get('articles')
	cmd_iden = cmd_dic.get('N°')
	mag = cmd_dic.get('magasin')
	ret = self.save_cmd_of_this_client(where,cmd_dic, True, date)
	if ret:
		for art_dic in articles.values():
			arr,part = where.split("_z_o_e_")
			WH = f"articles_z_o_e_{part}"
			self.save_retour(WH,art_dic, mag)

def paiement_commande(self,where,cmd_ident,paie_id,montant,date):
	where = self.get_my_where(where,"commandes")
	th_cmd = self.get_cmd(where,cmd_ident).get('data')
	th_cmd['montant payé']+= montant
	th_cmd['montant restant'] = float(th_cmd.get('montant TTC'))-float(th_cmd.get('montant payé'))
	th_cmd['paiement actuel'] = paie_id
	th_cmd['paiements'].append(paie_id)
	plan_paie = th_cmd.get('plan de paiements')

	if not plan_paie:
		plan_paie = {
			self.get_today():{
				"montant dû":th_cmd.get('montant TTC'),
				"montant payé":th_cmd.get('montant payé'),
				"date":date,
				"montant restant":th_cmd.get('montant restant'),
				'paiement associé':list()
			}
		}
	else:
		plan_paie = self.update_plan_paie(plan_paie,montant,paie_id,date)
	th_cmd['plan de paiements'] = plan_paie
	if th_cmd['montant restant'] <=0:
		th_cmd['status du paiement'] = 'Soldée'
	else:
		th_cmd["status du paiement"] = 'Non soldée'
	self.update_cmd(where,th_cmd)

def update_plan_paie(self,plan_paie,mont_paie,paie_id,date):
	dates = [datetime.strptime(date,self.date_format)
		for date in plan_paie.keys()]
	dates.sort()
	date_ind = 0
	while mont_paie > 0:
		th_date = dates[date_ind].strftime(self.date_format)
		date_dic = plan_paie.get(th_date)
		if not date_dic:
			raise ValueError(f"{th_date} n'est pas dans le plan de paie")
		mont_restant = date_dic.get('montant restant')
		if mont_restant:
			date_dic['montant payé'] += mont_paie if mont_paie <= mont_restant else mont_restant
			date_dic['montant restant'] = date_dic["montant dû"] - date_dic['montant payé']
			date_dic['date'] = date
			date_dic['paiement associé'].append(paie_id)
			mont_paie -= mont_restant
		else:
			date_ind += 1
	return plan_paie


{'id de la commande': 'FAC01-02-2026N°00001', 
'N°': 'FAC01-02-2026N°00001', 
'client': 'CLIN°00001', 
'montant TTC': 10000.0, 
'autre montant': {}, 
'montant payé': 2000.0, 
'paiements': ['REC01-02-2026N°00006'], 
'paiement actuel': 'REC01-02-2026N°00006', 
'articles': {'ARTN°00001': 
	{'conditionnement': {'Sac': [1, None], 
	'Démi Sac': [2.0, 'Sac']}, 
	'Désignation': 'Charbon', 
	'N°': 'ARTN°00001', 
	'img': 'media/logo.png', 
	'ventes': {'Sac': 1.0, 'Démi Sac': 1.0}, 
	'prix de vente': {'Sac': 6500.0, 'Démi Sac': 3500.0}, 
	'Qté': ' [b]1[/b] [i]Sac[/i] [b]1[/b] [i]Démi Sac[/i]', 
	'PVU': ' [b]6 500[/b] [i]Sac[/i] [b]3 500[/b] [i]Démi Sac[/i]', 
	'Montant HT': 10000.0, 'Taxes': 0, 
	'Montant TTC': 10000.0, 'Mont': 10000.0, 
	'Montant': 10000.0, 'No': '1'}}, 
'status de la commande': 'Livrée', 
'status du paiement': 'Non soldée', 
"date d'émission": '01-02-2026', 
'date de traitement': '01-02-2026', 
'date de livraison': '01-02-2026. 11:53:0', 
"date d'origine": '01-02-2026 .11:53:0', 
"nature d'encaissement": 'Non encaissé', 
'status de la facture': 'Crédit', 
"date d'encaissement": '', 
'type de facture': 'Facture', 
'type de contrat': '', 
'plan de remboursement': '', 
'date de fin contrat': '', 
'durée du contrat': 0, 
'associations': '', 
'commande mère': '', 
'commande modifiée': '', 
'date et heur de modification': '', 
'provenance': 'Bureau', 
'auteur': 'ZoeCorpUser', 
"provenance d'origine": 'Bureau', 
"auteur d'origine": 'ZoeCorpUser', 
'date de traitement prévu': '', 
'pénalité': 0.0, 'options pénalité': 0.0, 
'plan de paiements': {'01-02-2026': 
	{'montant dû': 10000.0, 
	'montant payé': 10000.0, 
	'date': '', 
	'montant restant': 0.0, 
	'paiement associé': []}}, 
'magasin': 'Général', 
'Nom du client': 'Aziabou', 
'montant restant': 8000.0, 
'nom client': 'Aziabou David', 
'Code client': 'CLIN°00001', 
'N° à contacter': '0168793580', 
"date d'achat": '01-02-2026. 11:53:0', 
'catégorie': '', 
'date premier échéance': '01-02-2026', 
'th_sort': 0, 'nombre de jour restant': 0, 
"N° d'ordre": 1, 'No': '1'}


