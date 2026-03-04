#Coding:utf-8
"""
	Gestion de méthode de sauvegarde
"""
from lib.davbuild import Cache_error

@Cache_error
def Fournisseur_save_decaisse(self,wid):
	th_dic = wid.this_decaiss_info
	ident = wid.this_decaiss_info.get('N°')
	founr_n = th_dic.get('bénéficiaire')
	mont = th_dic.get('montant décaissé')
	dic = self.sc.DB.Get_paiement_f_cmd()
	four_dic = self.sc.DB.Get_fourn_by_name(founr_n)
	four_id = four_dic.get('N°')
	dic['ecrit ident'] = ident
	dic['montant'] = mont
	dic['commande associée'] = th_dic.get('référence')
	dic['solde précédent'] = four_dic.get("solde")
	dic['fournisseur'] = four_id

	solde = four_dic.get('solde')
	if not solde:
		solde = float()
	solde -= mont
	four_dic["solde"] = solde

	self.sc.DB.Save_fourn_paie(dic)
	self.sc.DB.Modif_fournisseur(four_dic)

@Cache_error
def Partenaires_save_decaiss(self,wid):
	th_dic = wid.this_decaiss_info
	ident = th_dic.get('N°')
	dic = self.sc.DB.Get_paie_format()
	self.mont = 'Général'
	dic["libelé"] = self.mont
	dic['montant'] = th_dic.get('montant décaissé')
	dic['mode de paiement'] = th_dic.get("compte de sortie")
	dic['N°'] = ident
	cmpt_infos = self.sc.DB.Get_this_partenaires_by_name(th_dic.get('bénéficiaire'))
	paie_dic = cmpt_infos.get("paiements",dict())
	if not paie_dic:
		paie_dic = dict()
	paie_dic[ident] = dic
	cmpt_infos['paiements'] = paie_dic
	cmpt_infos["solde"] -= th_dic.get('montant décaissé')
	self.sc.DB.Update_partenaire(cmpt_infos)

@Cache_error
def Personnel_save_decaiss(self,wid):
	th_dic = wid.this_decaiss_info
	ident = th_dic.get('N°')
	dic = self.sc.DB.activite_format()
	dic['type'] = "Décaissement"
	dic['valeur monétaire'] = th_dic.get('montant décaissé')
	dic['bénéficiaire'] = th_dic.get('bénéficiaire')
	dic['motif'] = th_dic.get('motif de décaissement')
	self.sc.DB.Save_activite(dic)
