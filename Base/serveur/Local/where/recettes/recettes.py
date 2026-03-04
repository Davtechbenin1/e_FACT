#Coding:utf-8
"""
	Gestion des recettes de l'entreprise
"""
import sys
recette_fic = "recettes"
def get_recettes_format(self,date,heure):
	#id = self.get_ident_of(self.recette_fic,True,date)
	dic = {
		#"N°":id,
		"date":date,
		'heure':heure,
		"opérateur":str(),
		"client":str(),
		"id commande":str(),
		"comptes":str(),
		"référence":str(),
		"motif":str(),
		"montant":float(),
		"solde précédent":float(),
		"solde finale":float()
	}
	return dic

def save_recettes(self,where,recettes_dic,date,heure):
	recettes_d = self.get_recettes_format(date,heure)
	ident = recettes_dic.get('N°')
	recettes_d.update(recettes_dic)
	recettes_d["N°"] = ident

	client = recettes_d.get('client')
	mont = recettes_d.get('montant')

	if recettes_d.get("motif") == "Règlement factures":
		WH = self.get_my_where(where,"clients")
		client_d = self.get_client(WH,client)
		client_dic = client_d.get('data')
		if client_dic:
			sold_client = client_dic.get('solde')
			recettes_d['solde précédent'] = sold_client
			recettes_d["solde finale"] = sold_client - mont
			self.save_paie_of_this_client(where,recettes_d,date)

			id_cmd = recettes_d.get('id commande')
			self.paiement_commande(where,id_cmd,ident,mont,date)
			
		else:
			return self.failed_response(recettes_d,where,ident
				,"save",E = "Client invalide alors qu'il s'agit d'un règlement de factures")

	info = recettes_d.get("montant")
	self._save_ident_to(where, ident, info)
	
	self.save_recettes_to(where,recettes_d.get('comptes'),
		ident,mont,date)
	return self.save_data(where, recettes_d, ident)

def get_recettes(self,where,ident:str=None):
	return self.get_data(where, ident)

def delete_recettes(self,where,ident):
	return self.delete_data(where,ident)
