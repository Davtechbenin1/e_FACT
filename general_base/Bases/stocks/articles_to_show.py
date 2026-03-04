#Coding:utf-8
"""
	Gestion des articles a montrer sur l'application mobile
"""
def All_article_to_show(self,pays,commune,arrond,quart):
	"""
		Le principe de cette partie:
			- on prend les deux informations.
			- on récupère toutes les magasins possible
			- on recherche les articles associés aux magasins
			- on définie les prix de chaque article en fonction de 
			  magasin et du lieu de livraison du client (La clé est 
			  ident article +...+ ident magasin)
			- on classe le tout par ordre croissant
			
	"""
	#print(self.get_article())
	all_arti_dic = dict()
	zone_txt = self.format_part((pays,))
	zone_mag_list = self.get_zone_mag(zone_txt)
	real_zone = self.get_zone_ident(pays,commune,arrond,quart)
	for ident in zone_mag_list:
		article = self.get_article_of_magasin(ident)
		mag_addr = self.get_this_magasin(ident).get('adresse')
		magasin_zone = self.get_zone_ident(mag_addr.get('Pays'),
			mag_addr.get('Commune'),mag_addr.get('Arrondissement'),
			mag_addr.get('Quartier/Village'))
		for art_ident in article.keys():
			art_dic = dict(self.get_article(art_ident))
			th_art_dic = self.setting_price(real_zone,magasin_zone,ident,art_dic)
			self.art_dics_redone[f"{ident}...{art_ident}"] = th_art_dic
			cate_ident = art_dic.get('catégorie')
			cate_dic = all_arti_dic.get(cate_ident,dict())
			cate_dic[f"{ident}...{art_ident}"] = th_art_dic
			all_arti_dic[cate_ident] = cate_dic
	return all_arti_dic

def setting_price(self,destination_zone,magasin_zone,mag_ident,art_dic):
	liaison_ident = f"{destination_zone}...{magasin_zone}"
	liaison = self.get_liaison()
	liaison_montant = liaison.get(liaison_ident)
	if liaison_montant == None:
		if destination_zone == magasin_zone:
			liaison_montant = 200
		else:
			liaison_montant = 300
	prix_du_magasin = art_dic.get("prix de vente").get(mag_ident)
	marge = art_dic.get('taux de bénéfice')
	cond_prins = art_dic.get('stockage')
	prix_original = prix_du_magasin.get(cond_prins)
	marge_mont = round(float(prix_original)*float(marge)/100,0)
	final_prix = prix_original + marge_mont + liaison_montant
	art_dic['PVU'] = final_prix
	art_dic['cond principal'] = cond_prins
	art_dic['prix de livraison'] = liaison_montant
	art_dic['bénéfice'] = marge_mont
	art_dic["magasin d'origine"] = mag_ident
	art_dic['from_3'] = self.from_3(prix_original,marge_mont,liaison_montant)
	art_dic['catégorie name'] = self.get_categorie_name(art_dic.get('catégorie'))
	art_dic['this ident'] = f"{mag_ident}...{art_dic.get('id')}"
	return art_dic

def from_3(self,prix_original,marge_mont,liaison_montant):
	add_mont = round((liaison_montant + marge_mont)/2,0)
	return prix_original + add_mont

def get_my_redone_art(self,key):
	return self.art_dics_redone.get(key,dict())






