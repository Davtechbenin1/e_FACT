#Coding:utf-8

def modif_this_cmd(self,cmd):
	cmd['originale'] = False
	cmd['historique']["de modification"][self.sc.get_now()
	] = cmd.get('montant TTC')
	cmd['dernière modification'] = self.sc.get_now()
	self.update_cmd(cmd)

def paie_this_cmd(self,cmd,paie_dict):
	mont = paie_dict.get('montant')
	date = self.sc.get_now()
	date_dict = cmd.get('dates')
	if not date["du premier paiements"]:
		date["du premier paiements"] = date
	date["du dernier paiements"] = date
	cmd['historique']["de paiements"][paie_dict.get('id')] = mont
	cmd["montant payé"] += mont
	if cmd['montant payé'] >= cmd['montant TTC']:
		cmd['status']['du paiement'] = "soldée"
	else:
		cmd['status']['du paiement'] = "avancée"
	self.update_cmd(cmd)
	self.save_liveur_paiement(cmd,mont)
	self.save_client_paiement(paie_dict)

def livre_this_cmd(self,cmd,live_ident):
	cmd['status']['de livraison'] = "livrée"
	cmd["chargé d'affaire"] = live_ident
	cmd['status']['de la commande'] = "traité"
	cmd['dates']["de la livraison"] = self.sc.get_now()
	self.save_liveur_vente(cmd)
	self.save_client_vente(cmd)
	self.update_cmd(cmd)

def set_live_to(self,cmd,live_ident):
	cmd['status']['de livraison'] = "en cours de livraison"
	cmd["chargé d'affaire"] = live_ident
	cmd['dates']["de départ de la livraison"] = self.sc.get_now()
	self.update_cmd(cmd)

def confirmer_cmd(self,cmd):
	cmd['status']['de la commande'] = "en traitement"
	cmd["dates"]["de traitement"] = self.sc.get_now()
	self.update_cmd(cmd)

def anuler_this_cmd(self,cmd,motif):
	cmd['annuler'] = {
		self.sc.get_today():motif
	}
	if cmd.get('originale'):
		...
	else:
		date = cmd.get("")
	self.update_cmd(cmd)

def get_all_cmd_type_of(self,fichier,date_liste = list(), 
	delete = False, all_type = False):
	if not date_liste:
		date_liste = [self.sc.get_today(),]
	all_cmd = dict()
	for date in date_liste:
		all_cmd_ident = self.get_all_cmd_base_of(date)
		for ident in all_cmd_ident:
			th_date = self.get_date_from_ident(ident)
			cmd_d = self.get_type_of_cmd(fichier,th_date,ident)
			if all_type:
				pass
			elif delete:
				cmd_d = cmd_d if cmd_d.get('annuler') else dict()
			else:
				cmd_d = cmd_d if not cmd_d.get('annuler') else dict()
			if cmd_d:
				all_cmd[ident] = cmd_d
	return all_cmd

def get_all_cmd_of(self,date_liste = list(),delete = False, all_type = False):
	return self.get_all_cmd_type_of(self.commande_fic,date_liste,
		delete,all_type)

def get_all_cmd_orig_of(self,date_liste = list(),delete = False, all_type = False):
	return self.get_all_cmd_type_of(self.commande_org_fic,date_liste,
		delete,all_type)



