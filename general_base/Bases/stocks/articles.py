#Coding:utf-8
def article_format(self):
	return {
		"id":self.Get_article_ident(),
		"type":str(),
		"magasin":dict(),
		"catégorie":str(),
		"img":"media/logo.png",
		"imgs":list(),
		"désignation":str(),
		"stock":dict(),
		"stocks":dict(),#Cet stock est géré en fonction du magasin
		"seuil d'alerte":int(),
		"dernier activité":str(),
		"prix de vente":dict(),
		"conditionnement":dict(),#{key:(val,key)}
		"stockage":str(),# Pour identifier le stockage principale des conditionnements
		"fournisseurs":dict(),
		"taux de bénéfice":float(),
		"achats":dict(),
		"ventes":dict(),
		"inventaires":dict(),
		"historique":{
			"ventes":dict(),
			"achats":dict(),
			"pertes":dict(),
			"inventaires":dict(),
		}
	}

def add_article(self,dic):
	self.update_article(dic)
	magasin = dic.get('magasin')
	categorie = dic.get("catégorie")
	type = dic.get('type')
	self.add_article_to_categorie(categorie,dic)
	self.add_article_to_type(type,dic)
	self.add_article_to_magasin(magasin,dic)

def update_article(self,dic):
	self.Save_details_data(self.article_fic,dic)

def get_article(self,ident = None):
	dic = self.Get_details_data(self.article_fic)
	if ident:
		ident = self.redo_ident(ident)
		return dic.get(ident)
	else:
		return dic

def get_article_names(self):
	lis = self.get_article().values()
	name_dict = {dic.get("désignation"):dic.get('id') 
		for dic in lis if dic}
	return name_dict

# Gestion de la vente d'article
def save_part_of_article(self,magasin,part,art_id,qte,prix):
	date = self.sc.get_today()
	article = self.get_article(art_id)
	art_vent = article.get(part)
	date_vente_dic = art_vent.get(date,dict())
	for key,th_qte in qte.items():
		key_liste = date_vente_dic.get(key,list())
		key_liste.append((th_qte,prix.get(key)))
		date_vente_dic[key] = key_liste
	art_vent[date] = date_vente_dic
	article[part] = art_vent
	if part in ("ventes","pertes"):
		article = self.historique_part(article,"ventes",qte)
		return self.destocker(magasin,article,qte)
	elif part in ("achats","inventaires"):
		return self.stocker(magasin,article,qte)

def update_articles_after(self,magasin,part,part_dic):
	"""
		part_dic = {
			id:{qte:dict(),prix:dict(),taxes:dict(),montant:dict()}
		}
	"""
	all_art_up = dict()
	for ident,art_d in part_dic.items():
		all_art_up[ident] = self.save_part_of_article(magasin,part,ident,
			art_d.get('qte'),art_d.get('prix'))
	self.Save_multiple_data(self.article_fic,all_art_up)

def destocker(self,magasin,article,qte):
	art_stk = article.get("stock")
	mag_stk = art_stk.get(magasin,dict())
	for key,th_qte in qte.items():
		mag_stk[key] -= th_qte
	art_stk[magasin] = mag_stk
	article['stock'] = art_stk
	return article

def stocker(self,magasin,article,qte):
	art_stk = article.get("stock")
	mag_stk = art_stk.get(magasin,dict())
	for key,th_qte in qte.items():
		mag_stk[key] += th_qte
	art_stk[magasin] = mag_stk
	article['stock'] = art_stk
	return article

def historique_part(self,article,part,qte,add = True):
	hist_dic = article.get("historique").get(part)
	date_dic = hist_dic.get(self.sc.get_today(),dict())
	for key,th_qte in qte.items():
		th_qq = date_dic.get(key,0)
		if add:
			th_qq += th_qte
		else:
			th_qq -= th_qte
		date_dic[key] = th_qq
	hist_dic[self.sc.get_today] = date_dic
	article['historique'][part] = hist_dic
	return article
