#Coding:utf-8
article_fic = "article"
import sys

def get_article_format(self,date):
	return {
		#"N°":,
		"famille":str(),
		'img':'media/logo.png',
		"désignation":str(),
		"stocks":{},
		"stock general":{},
		"seuil d'approvisionnement":int(),
		"dernier activité":date,
		"arrivage":{},#Représente l'arrivage totale
		"vente":{},#Représente la vente totale
		"perte":{},#Représente les pertes totales
		
		"inventaire":dict(),
		"prix d'achat":{},# Représente le prix d'achat actuelle

		"prix de vente":dict(),
		"prix de vente à crédit":dict(),
		"conditionnement":dict(),#{key:(val,key)}
		"stockage":str(),# Pour identifier le stockage principale des conditionnements	
	}

def save_article(self,where,data,date = None):
	if not date:
		date = self.get_today()
	th_data = self.get_article_format(date)
	th_data["dernier activité"] = date
	ident = data.get('N°')
	"""
	img = data.get('img')
	if img:
		img = self.Save_image(img)
	"""
	th_data.update(data)
	th_data['N°'] = ident
	#data["img"] = img

	
	info = data.get("désignation")
	self._save_ident_to(where, ident, info,
		where)
	return self.save_data(where, th_data, ident)

def get_article(self,where,ident: str = None):
	dic = self.get_data(where, ident)
	#print(dic)
	return dic

def update_article(self, where, data, ident: str = None):
	"""
	img = data.get('img')
	if img:
		img = self.Save_image(img)
	#data["img"] = img
	"""
	if not ident:
		ident = data.get('N°')

	info = data.get("désignation")
	self._save_ident_to(where, ident, info,
		where)
	return self.update_data(where, data, ident)

def delete_article(self, where,ident):	
	return self.delete_data(where,ident)

# Gestion des actions spécifiques directe sur l'article
def save_arr(self, where,art_d,mag,fourn):
	"""
		Ici, on met à jour:
		-> stocks par magasin
		-> stocks général
		-> prix d'achat
		-> arrivage total
	"""
	#print(art_d)
	th_article_dic = self.get_article(where,art_d.get('N°')).get("data")
	#print()
	#print(th_article_dic)
	#print("---------------")
	#sys.exit()
	mag_stock = th_article_dic.get('stocks').get(mag,dict())
	stk_gene = th_article_dic.get('stock general',dict())
	prix_achat = th_article_dic.get("prix d'achat").get(fourn,dict())
	arrivage_total = th_article_dic.get('arrivage')
	cond = th_article_dic.get("conditionnement")

	achat = art_d.get('achats')
	prix = art_d.get("prix d'achat").get(fourn)
	prix_achat.update(prix)
	for k,val in achat.items():
		stk_val = mag_stock.setdefault(k,int())
		stk_val += val
		mag_stock[k] = stk_val

		stk_val = stk_gene.setdefault(k,int())
		stk_val += val
		stk_gene[k] = stk_val

		stk_val = arrivage_total.setdefault(k,int())
		stk_val += val
		arrivage_total[k] = stk_val

	th_article_dic["stocks"][mag] = self.correct_stock(mag_stock, cond)
	th_article_dic["stock general"] = self.correct_stock(stk_gene, cond)
	th_article_dic["arrivage"] = self.correct_stock(arrivage_total, cond)
	th_article_dic["prix d'achat"][fourn] = prix_achat

	self.update_article(where,th_article_dic)

def save_pert(self,where,art_d,mag):
	"""
		Ici, on met à jour:
		-> stocks par magasin
		-> stocks général
		-> arrivage total
	"""
	th_article_dic = self.get_article(where,art_d.get('N°')).get('data')
	mag_stock = th_article_dic.get('stocks').get(mag,dict())
	stk_gene = th_article_dic.get('stock general',dict())
	perte_total = th_article_dic.get('perte')
	cond = th_article_dic.get("conditionnement")

	achat = art_d.get('pertes')
	for k,val in achat.items():
		stk_val = mag_stock.setdefault(k,int())
		stk_val -= val
		mag_stock[k] = stk_val

		stk_val = stk_gene.setdefault(k,int())
		stk_val -= val
		stk_gene[k] = stk_val

		stk_val = perte_total.setdefault(k,int())
		stk_val += val
		perte_total[k] = stk_val

	th_article_dic["stocks"][mag] = self.correct_stock(mag_stock,cond)
	th_article_dic["stock general"] = self.correct_stock(stk_gene,cond)
	th_article_dic["perte"] = self.correct_stock(perte_total,cond)

	self.update_article(where,th_article_dic)

def save_invent(self,where,art_d,mag):
	"""
		Ici, on met à jour:
		-> stocks par magasin
		-> stocks général
		-> arrivage total
	"""
	th_article_dic = self.get_article(where,art_d.get('N°')).get('data')
	mag_stock = th_article_dic.get('stocks').get(mag,dict())
	stk_gene = th_article_dic.get('stock general',dict())
	invent_total = th_article_dic.get('inventaire',dict())
	cond = th_article_dic.get("conditionnement")

	invent = art_d.get('résultat')
	for k,val in invent.items():
		stk_val = mag_stock.setdefault(k,int())
		stk_val += val
		mag_stock[k] = stk_val

		stk_val = stk_gene.setdefault(k,int())
		stk_val += val
		stk_gene[k] = stk_val

	
	invent_total[self.sc.get_today()] = invent

	th_article_dic["stocks"][mag] = self.correct_stock(mag_stock,cond)
	th_article_dic["stock general"] = self.correct_stock(stk_gene,cond)
	th_article_dic["inventaire"] = invent_total

	self.update_article(where,th_article_dic)

def save_transf(self,where,art_d,mag_source,mag_destination):
	th_article_dic = self.get_article(where,art_d.get('N°')).get('data')
	th_article_dic = self.save_deskt_transf(art_d,
		th_article_dic,mag_source)
	th_article_dic = self.save_stock_transf(art_d,
		th_article_dic,mag_destination)
	self.update_article(where,th_article_dic)

def save_deskt_transf(self,where,art_d,th_article_dic,mag_source):
	mag = mag_source
	mag_stock = th_article_dic.get('stocks').get(mag,dict())
	transfert_total = th_article_dic.setdefault('transfert',dict()).get(mag,dict())
	cond = th_article_dic.get("conditionnement")
	achat = art_d.get('destockage')
	for k,val in achat.items():
		stk_val = mag_stock.setdefault(k,int())
		stk_val -= val
		mag_stock[k] = stk_val

		stk_val = transfert_total.setdefault(k,int())
		stk_val -= val
		transfert_total[k] = stk_val

	th_article_dic["stocks"][mag] = self.correct_stock(mag_stock, cond)
	th_article_dic["transfert"][mag] = self.correct_stock(transfert_total, cond)

	return th_article_dic

def save_stock_transf(self,where,art_d,th_article_dic,mag_destination):
	mag = mag_destination
	mag_stock = th_article_dic.get('stocks').get(mag,dict())

	transfert_total = th_article_dic.setdefault('transfert',dict()).get(mag,dict())
	cond = th_article_dic.get("conditionnement")

	achat = art_d.get('destockage')
	for k,val in achat.items():
		stk_val = mag_stock.setdefault(k,int())
		stk_val += val
		mag_stock[k] = stk_val

		stk_val = transfert_total.setdefault(k,int())
		stk_val += val
		transfert_total[k] = stk_val

	th_article_dic["stocks"][mag] = self.correct_stock(mag_stock, cond)
	th_article_dic["transfert"][mag] = self.correct_stock(transfert_total, cond)

	return th_article_dic

def correct_stock(self,stocks,conditionement):
	all_stks = dict()
	th_all_stks = dict()
	if len(conditionement) == 1:
		return stocks
	for key,tup in conditionement.items():
		val,cond = tup
		if cond == None:
			stockage_pr = key
		else:
			all_stks[cond] = [val,key]
	
	new_all_stks = {stockage_pr:1}

	for key,tup in all_stks.items():
		val,cond = tup
		if key == stockage_pr:
			ref_to_stk_pr = cond
			val_to_stk_pr = val
			continue
	all_stks.pop(stockage_pr)
	lenf = len(all_stks)
	new_all_stks[ref_to_stk_pr] = val_to_stk_pr
	while lenf:
		for key,tup in all_stks.items():
			val,cond = tup
			if key == ref_to_stk_pr:
				val_to_stk_pr *= val
				stockage_pr = key
				ref_to_stk_pr = cond
				new_all_stks[ref_to_stk_pr] = val_to_stk_pr
				continue
		all_stks.pop(stockage_pr)
		lenf = len(all_stks)

	stk_al = float()
	for key,val in stocks.items():
		th_val = new_all_stks.get(key)
		stk_al += (val*val_to_stk_pr)/th_val
	th_stock = dict()
	for k,v in new_all_stks.items():
		th_stock[k] = int(stk_al) // int((val_to_stk_pr)/v)
		stk_al = stk_al%int((val_to_stk_pr)/v)
	return th_stock

def acurate_stock(self,stocks,conditionement):
	all_stks = dict()
	th_all_stks = dict()
	if len(conditionement) == 1:
		val = int()
		for v in stocks.values():
			val += v
		return val
	for key,tup in conditionement.items():
		val,cond = tup
		if cond == None:
			stockage_pr = key
		else:
			all_stks[cond] = [val,key]
	
	new_all_stks = {stockage_pr:1}

	for key,tup in all_stks.items():
		val,cond = tup
		if key == stockage_pr:
			ref_to_stk_pr = cond
			val_to_stk_pr = val
			continue
	all_stks.pop(stockage_pr)
	lenf = len(all_stks)
	new_all_stks[ref_to_stk_pr] = val_to_stk_pr
	while lenf:
		for key,tup in all_stks.items():
			val,cond = tup
			if key == ref_to_stk_pr:
				val_to_stk_pr *= val
				stockage_pr = key
				ref_to_stk_pr = cond
				new_all_stks[ref_to_stk_pr] = val_to_stk_pr
				continue
		all_stks.pop(stockage_pr)
		lenf = len(all_stks)

	return val_to_stk_pr

def save_vent(self,where,art_d,mag):
	th_article_dic = self.get_article(where,art_d.get('N°')).get('data')
	mag_stock = th_article_dic.get('stocks').get(mag,dict())
	stk_gene = th_article_dic.get('stock general',dict())
	vente_total = th_article_dic.get('vente')
	cond = th_article_dic.get("conditionnement")

	achat = art_d.get('ventes')
	for k,val in achat.items():
		stk_val = mag_stock.setdefault(k,int())
		stk_val -= val
		mag_stock[k] = stk_val

		stk_val = stk_gene.setdefault(k,int())
		stk_val -= val
		stk_gene[k] = stk_val

		stk_val = vente_total.setdefault(k,int())
		stk_val += val
		vente_total[k] = stk_val

	th_article_dic["stocks"][mag] = self.correct_stock(mag_stock,cond)
	th_article_dic["stock general"] = self.correct_stock(stk_gene,cond)
	th_article_dic["vente"] = self.correct_stock(vente_total,cond)

	self.update_article(where,th_article_dic)

def save_retour(self,where,art_d,mag):
	th_article_dic = self.get_article(where,art_d.get('N°')).get('data')
	mag_stock = th_article_dic.get('stocks').get(mag,dict())
	stk_gene = th_article_dic.get('stock general',dict())
	vente_total = th_article_dic.get('vente')
	cond = th_article_dic.get("conditionnement")

	achat = art_d.get('ventes')
	for k,val in achat.items():
		stk_val = mag_stock.setdefault(k,int())
		stk_val += val
		mag_stock[k] = stk_val

		stk_val = stk_gene.setdefault(k,int())
		stk_val += val
		stk_gene[k] = stk_val

		stk_val = vente_total.setdefault(k,int())
		stk_val -= val
		vente_total[k] = stk_val

	th_article_dic["stocks"][mag] = self.correct_stock(mag_stock,cond)
	th_article_dic["stock general"] = self.correct_stock(stk_gene,cond)
	th_article_dic["vente"] = self.correct_stock(vente_total,cond)

	self.update_article(where,th_article_dic)



