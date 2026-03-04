#Coding:utf-8
import threading
import time, datetime,sys

Thread = threading.Thread

class Handler:
# Gestionnaire de stock
	from .Gestionnaires.de_stocks import (Repartition_stk,
		stk_of_this_magasin,stk_of_this_famille,stk_of_this_fournisseur,
		Trie_stk,get_magasin,get_stk_set,get_art_name,
		set_stk_compt_dic,Get_arrivage_from,Get_perte_from,Get_invent_from,
		Get_conso_interne_from,Up_predefinie,Up_this_predef,
		Get_transfert_mag_form)

	from .Gestionnaires.Usage_general import (add_connex_info,add_modal_surf,get_modal_surf,close_modal,play_sound,add_refused_error,
		End_app_,set_host,End_app,set_port,relance_con,UP_this_l,Get_famm_d,Up_all_base,UPP,True_up,Get_my_clt,imp_part_dic,
		Get_fourn_list,fournisseur,get_type_list,get_cat_list,verif_clot,get_lieu,get_hour,get_now,get_categorie_liste,get_this_sous_cat,
		add_back_but,Get_article_ident,get_depot_fond_typ,get_motif_decaiss_list,get_encaisse_type,get_moyen_paiement,get_fournisseur_list,
		get_img_from,Get_cmd_typ_list,Get_cmd_status_list,print_fic,clean_old_backup,handle_remove_readonly,End_zoecorp,add_refused_error2)

	from .Gestionnaires.G_impression import (impress_fich_paie,Generer_doxs)

	from .Gestionnaires.les_dates import (Get_mois_of,Get_date_of,get_today,real_date,get_yerterday,_get_yerterday,normalize_date,re_do_date,
		get_normal_date,Trie_date,sorted_by_date,get_7_days,get_dates_from,get_date_f,Sup_a,get_date_list,_month_from_years,_get_month_list,
		days_from_month,_get_all_days,_get_real_days,get_date_obj)

	from .Gestionnaires.G_personnel import (get_curent_perso,get_profile_perso,Get_User_info,Get_User_menu_of,Get_liste_type_perso,
		get_devers_perso,Up_Perso_dict,Get_this_perso_ident,get_all_perso,get_all_charger)

	from .e_MECEF import(tester_connexion_emecf,normalise_fact,Get_items,Get_payments_of,
		Get_all_paiem,get_autr_m,Confirmation_normaliser,QR_code)

	def __init__(self):
		self.perte_predefine = dict()
		self.invent_predefine = dict()
		self.conso_predefine = dict()
		self.transfert_predefine = dict()

		self.cmpt_par_magasin = dict()
		self.cmpt_par_fournisseur = dict()
		self.cmpt_par_famille = dict()

		self.class_par_magasin = {"Général":dict()}
		self.class_par_fournisseur = {"Général":dict()}
		self.class_par_famille = {"Général":dict()}
		self.magasin_list = list()
		self.actif_dict = dict()

	def this_run_handler(self):
		foncs = [self.Repartition_stk,self.Up_predefinie]
		[f() for f in foncs]


# Gestion des charges
	def Get_charges(self):
		return {
			"Achats consommés":["Achats de matières premières",
				"Achats de marchandises","Achats d'emballages",
				"Achats d'approvisionnements non stockés","autres"],
			"Charges du personnel":["Salaires et traitements",
				"Primes et gratifications","Cotisations sociales",
				"Avantage en nature","Transport",'Repas',"Logements"],
			"Services extérieurs":["Loyers","Entretien et réparations",
				"Assurances","Sous-traitance","Communications","Internet",
				"Hébergement web","Publicité et marketing","Honoraires",
				"Frais postaux","Documentations","Formation du personnel",
				"Frais bancaires"],
			"Impôts et taxes":["TVA","AIB",'Redevences',"Licences d'exploitation",
				"Droits de douane"],
			"Charges diverses":["Amortissement","Créances irrécouvrables",
				"Dons et mécénat","Pertes","Résultat d'inventaires"],
		}

# Gestion des accès logiciels
	def Get_access_dict(self):
		return {
			"Accueil":{
				"Stocks":["lectures","écritures"],
				"Ventes":["écritures"],
				"Factures":["lectures","écritures"],
				"Factures retours":['écritures'],
				"Supprimer Factures":['écritures'],
				"Livrée les Factures":['écritures'],
				"Plan paiement":["écritures"],
			},
			"Suivie des creances":{
				"Factures générales":["lectures"],
				"Créances en cours":["lectures"],
				"Créances impayées":["lectures"],
				"Echéances du jours":["lectures"],
				"Historiques":["lectures"],
				'Point financier CA':["lectures","écritures"],
				"Statistiques":["lectures"],
			},
			"Ressouses Humaines":{
				"Personnels":["lectures","écritures"],
				"Postes":["lectures","écritures"],
				"Recrutements":["lectures","écritures"],
				"Candidat":["lectures","écritures"],
				"Gestion Candidat":["lectures","écritures"],
				"Entretient":["lectures","écritures"],
				"Salaires":["lectures","écritures"],
				"Accèss logiciel":["lectures","écritures"],
				"Supprimer postes":["écritures"],
			},
			"Clients":{
				"Clients":["lectures","écritures"],
				"Nouveau clients":["écritures"],
				"Identité":["lectures",],
				"Information client":["écritures"],
				"Commandes":["lectures"],
				"Paiements":["lectures"],
				"Historique d'action":['lectures'],
				"Affiliation":['lectures',"écritures"]
			},
			"Fournisseurs":{
				'Fournisseur':["lectures","écritures"],
				"Informations général":["lectures","écritures"],
				"Commandes":["lectures","écritures"],
				"Paiements Fournisseur":["lectures","écritures"],
			},
			"Partenaires":{
				"Partenaire":["lectures","écritures"],
				"Informations partenaire":["lectures","écritures"],
				"Historiques des actions":["lectures"],
				"Paiements partenaire":["lectures","écritures"],
			},
			"Finances":{
				"Encaissements":["lectures","écritures"],
				"Décaissement":["lectures","écritures"],
				"Montants accessoires":["lectures","écritures"],
				"Trésorerie interne":["lectures","écritures"],
				"Annuller un recouvrement":['écritures'],
				"Encaissements financier":["lectures","écritures"],
				"Déversement comptable":["écritures"],
				"Point financier":["lectures"],
				"Mouvement financier":["écritures"],
				"Historiques Comptable global":["lectures"],
			},
			"Info Général":{
				"Paramètre général":["lectures","écritures"],
				"Normalisation":["lectures","écritures"],
				"Connexion":['écritures'],
			},
			#"Aide":{"all":["all"]},
			"Profil":{"all":["all"]},	
			"Annalyse":{"all":["all"]},
		}

# Gestion des factures
	def Get_entet_info_dict(self):
		return {
			"Facturation":str(),
		}

	def Default_post(self):
		P1 = {
			"nom":"SECRETARIAT",
			"fonction principal":"Gestion des documents adminitratifs",
			"niveau hiérachique":"Standart",
			"catégorie":'Administration'
		}
		P2 = {
			"nom":"CHARGEE D'AFFAIRES",
			"fonction principal":"Gestion des clients",
			"niveau hiérachique":"Standart",
			"catégorie":'Commercial'
		}
		P3 = {
			"nom":"DIRECTION",
			"fonction principal":"Direction de l'entreprise",
			"niveau hiérachique":"Direction",
			"catégorie":'Administration'
		}
		P4 = {
			"nom":"COMPTABILITE",
			"fonction principal":"Gestion comptable",
			"niveau hiérachique":"Exécutive",
			"catégorie":'Administration'
		}
		P5 = {
			"nom":"CHARGEE DES OPERATIONS",
			"fonction principal":"Gestion Général",
			"niveau hiérachique":"Supervision",
			"catégorie":'Administration'
		}

		L = [P1,P2,P3,P4,P5]
		for p in L:
			P = self.DB.Poste_save_format()
			P.update(p)
			self.DB.Save_poste(P)


