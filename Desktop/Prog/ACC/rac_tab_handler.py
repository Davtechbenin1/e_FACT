from lib.davbuild import *
from General_surf import *


@Cache_error
def close_info_surf(self,wid):
	srf = wid.info
	self.suspended.append(srf.part)
	self.histo_part.remove_widget(srf)

@Cache_error
def show_art_rup(self,wid):
	dic = self.info_dict.get("Articles en ruptures")
	liste = [self.get_art_info(d) for d in dic.values()]
	entete = ["Famille","Désignation","Activitée récente","Stock actuel",
		"Vente total","Achat total"]
	wid_l = [.2,.2,.15,.15,.15,.15]
	titre = "Détails des articles en rupture"
	self.add_rac_tab(entete,wid_l,liste,titre)

@Cache_error
def show_art_ale(self,wid):
	...

@Cache_error
def show_art_per(self,wid):
	...

@Cache_error
def show_art_cri(self,wid):
	dic = self.info_dict.get("Stock critique")
	liste = [self.get_art_info(d) for d in dic.values()]
	entete = ["Famille","Désignation","Activitée récente","Stock actuel",
		"Vente total","Achat total"]
	wid_l = [.2,.2,.15,.15,.15,.15]
	titre = "Détails des articles dont le stock est critique"
	self.add_rac_tab(entete,wid_l,liste,titre)

#-------------------------------------
def show_client_debit(self,wid):
	dic = self.info_dict.get("Clients débiteurs")
	liste = dic.values()
	entete = ["N°","nom","prénom","tel","solde",'status',"chargé d'affaire"]
	wid_l = [.15,.15,.15,.13,.15,.12,.15]
	titre = "Détails des clients débiteurs"
	self.add_rac_tab(entete,wid_l,liste,titre)

def show_creance_en_cour(self,wid):
	dic = self.info_dict.get("Créances en cours")
	liste = dic.values()
	entete = ["Nom du client","chargé d'affaire","numéro à contacter",
		"montant TTC","montant payé","montant restant",
		"date d'émission"]
	wid_l = [.2,.15,.1,.1,.15,.15,.15]
	titre = "Détails des créances en cours"
	self.add_rac_tab(entete,wid_l,liste,titre)

def show_creance_imp(self,wid):
	dic = self.info_dict.get("Créances impayées")
	liste = dic.values()
	entete = ["Nom du client","chargé d'affaire","numéro à contacter",
		"montant TTC","montant payé","montant restant",
		"date d'émission"]
	wid_l = [.2,.15,.1,.1,.15,.15,.15]
	titre = "Détails des créances impayée"
	self.add_rac_tab(entete,wid_l,liste,titre)

def show_eche_du_jour(self,wid):
	dic = self.info_dict.get("Echéances du jours")
	liste = dic.values()
	entete = ["Nom du client","chargé d'affaire",
		"numéro à contacter",
		"montant de l'échéance",
		'Montant total restant',
		"Echéance N°"]
	wid_l = [.2,.15,.1,.1,.15,.15,.15]
	titre = "Détails des échéances en cours"
	self.add_rac_tab(entete,wid_l,liste,titre)

def show_eche_imp(self,wid):
	dic = self.info_dict.get("Echéances non respectées")
	liste = dic.values()
	entete = ["Nom du client","chargé d'affaire",
		"numéro à contacter",
		"échéance échus non payé",
		'Montant total restant',
		"nombre d'impayé"]
	wid_l = [.2,.15,.1,.1,.15,.15,.15]
	titre = "Détails des échéances non respectées"
	self.add_rac_tab(entete,wid_l,liste,titre)
