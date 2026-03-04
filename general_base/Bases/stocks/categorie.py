#Coding:utf-8
def categorie_format(self):
	return {
		"id":self.Get_categorie_ident(),
		"nom":str(),
		'img':"media/logo.png",
		"articles":dict(),
		"stock":dict(),
		"ventes":dict(),
		"achats":dict(),
		"inventaires":dict(),
		}

def update_categorie(self,categorie_dic):
	self.Save_details_data(self.categorie_fic,categorie_dic)

def add_article_to_categorie(self,categorie_id,art_dic):
	"""
		Utiliser pour ajouter un article a un categorie donné
	"""
	art_dic['catégorie'] = categorie_id
	self.update_article(art_dic)
	categorie_dic = self.get_this_categorie(categorie_id)
	if not categorie_dic:
		return "identifiant du categorie d'article invalide"
	categorie_dic["articles"][art_dic.get('id')] = art_dic.get('désignation')
	#categorie_dic = self.up_categorie_part("stock",categorie_dic,art_dic)
	#categorie_dic = self.up_categorie_part("ventes",categorie_dic,art_dic)
	#categorie_dic = self.up_categorie_part("achats",categorie_dic,art_dic)
	#categorie_dic = self.up_categorie_part("inventaires",categorie_dic,art_dic)
	self.update_categorie(categorie_dic)

def sup_article_from_categorie(self,categorie_id,art_dic):
	"""
		Utiliser pour retirer un article d'un categorie donné
	"""
	art_dic['catégorie'] = str()
	self.update_article(art_dic)
	categorie_dic = self.get_this_categorie(categorie_id)
	if not categorie_dic:
		return "identifiant du categorie d'article invalide"

	if art_dic.get('id') in categorie_dic['articles']:
		categorie_dic['articles'].pop(art_dic.get('id'))
	
	#categorie_dic = self.sup_categorie_part("stock",categorie_dic,art_dic)
	#categorie_dic = self.sup_categorie_part("ventes",categorie_dic,art_dic)
	#categorie_dic = self.sup_categorie_part("achats",categorie_dic,art_dic)
	#categorie_dic = self.sup_categorie_part("inventaires",categorie_dic,art_dic)
	self.update_categorie(categorie_dic)

def up_categorie_part(self,part,categorie_dic,art_dic):
	categorie_art_part = categorie_dic.get(part,dict())
	for k,v in art_dic.get(part).items():
		
		val = categorie_art_part.get(k)
		if not val:
			val = 0
		categorie_art_part[k] = val + v
	categorie_dic[part] = categorie_art_part
	return categorie_dic

def sup_categorie_part(self,part,categorie_dic,art_dic):
	categorie_art_part = categorie_dic.get(part,dict())
	for k,v in art_dic.get(part).items():
		val = categorie_art_part.get(k)
		if val:
			val -= v
		if not val:
			categorie_art_part.pop(k)
		elif val:
			categorie_art_part[k] = val
	categorie_dic[part] = categorie_art_part
	return categorie_dic

def get_categories(self):
	return self.Get_details_data(self.categorie_fic)

def get_categorie_name(self,ident):
	if ident:
		return self.get_this_categorie(ident).get('nom',str())
	else:
		return str()
	
def get_categorie_ident(self,name):
	dic = {dic.get('nom'):dic.get('id') 
		for dic in self.get_categories().values()}
	return dic.get(name,str())

def get_this_categorie(self,ident):
	ident = self.redo_ident(ident)
	return self.get_categories().get(ident,dict())

