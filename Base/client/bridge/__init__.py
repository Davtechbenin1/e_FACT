#Coding:utf-8
"""
	Ici, on regroupe les méthodes servant de pont de chaque
	module de gestion de la base de donnée
"""
class bridge:
	from .Articles import (Save_new_art,Save_article,
		Get_this_art_num,Get_article_list,
		Get_article_list_dict,Get_this_article,
		Get_famille_dict,Set_family_dict,
		add_to_family_dict,Update_article,acurate_stock)

	from .Arrivages import (Save_arrivage,Get_all_arrivage_id,
		Get_this_arrivage,get_arrivage_of,get_arrivages_ofs)

	from .Pertes import (Save_perte,Get_all_perte_id,
		Get_this_perte,get_perte_of,get_pertes_ofs)

	from .Clients import (Save_client,Supp_client,
		Update_client,Get_this_clt,Get_clt_list, 
		Get_this_clt_num,Get_this_clt_solde,)

	from .Commandes import (Save_cmd,Get_all_commandes,
		Modif_this_cmd,Sup_this_cmd,Get_this_cmd,
		Partage_hist,Get_cmd_impayer,Get_cmd_encours,
		get_cmds_of,Get_cmd_non_sold,get_cmds_of,
		get_cmds_ofs,get_fact_of,get_fact_retour_of)

	from .Comptes import (Save_compte,Get_comptes_dict,
		Update_this_compte,Get_this_compte,Get_mouve_of,
		Get_mouvs_of,Get_hist_solde_of,Default_caisse)

	from .Fournisseurs import (Default_fourn,
		Modif_fournisseur,Get_fournisseur_dict,
		Get_this_fournisseur,Save_fournisseur,
		Get_this_fourn_ident,Get_fournisseur_list,
		Get_fourn_by_name)

	from .Autres import (Get_ent_part,Get_all_paiement_of,
		Get_access_of,Genere_code,adresse_of,Get_autre_mont_of,
		Get_types_contrats,Get_types_contrats_list,
		Get_all_remb_form)
	