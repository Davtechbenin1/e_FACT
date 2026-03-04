#Coding:utf-8
def type_article_format(self):
	return {
		"id":self.Get_type_article_ident(),
		"nom":str(),
		"articles":dict(),
		"stock":dict(),
		"ventes":dict(),
		"achats":dict(),
		"inventaires":dict(),
		}

def update_type_article(self,type_dic):
	self.Save_details_data(self.type_article_fic,type_dic)

def add_article_to_type(self,type_id,art_dic):
	"""
		Utiliser pour ajouter un article a un type donné
	"""
	type_dic = self.get_this_type_article(type_id)
	if not type_dic:
		return "identifiant du type d'article invalide"
	type_dic["articles"][art_dic.get('id')] = art_dic.get('désignation')
	#type_dic = self.up_article_type_part("stock",type_dic,art_dic)
	#type_dic = self.up_article_type_part("ventes",type_dic,art_dic)
	#type_dic = self.up_article_type_part("achats",type_dic,art_dic)
	#type_dic = self.up_article_type_part("inventaires",type_dic,art_dic)
	self.update_type_article(type_dic)

def sup_article_from_type(self,type_id,art_dic):
	"""
		Utiliser pour retirer un article d'un type donné
	"""
	type_dic = self.get_this_type_article(type_id)
	if not type_dic:
		return "identifiant du type d'article invalide"

	if art_dic.get('id') in type_dic['articles']:
		type_dic['articles'].pop(art_dic.get('id'))
	
	#type_dic = self.sup_article_type_part("stock",type_dic,art_dic)
	#type_dic = self.sup_article_type_part("ventes",type_dic,art_dic)
	#type_dic = self.sup_article_type_part("achats",type_dic,art_dic)
	#type_dic = self.sup_article_type_part("inventaires",type_dic,art_dic)
	self.update_type_article(type_dic)

def up_article_type_part(self,part,type_dic,art_dic):
	type_art_part = type_dic.get(part,dict())
	for k,v in art_dic.get(part).items():
		
		val = type_art_part.get(k)
		if not val:
			val = 0
		type_art_part[k] = val + v
	type_dic[part] = type_art_part
	return type_dic

def sup_article_type_part(self,part,type_dic,art_dic):
	type_art_part = type_dic.get(part,dict())
	for k,v in art_dic.get(part).items():
		val = type_art_part.get(k)
		if val:
			val -= v
		if not val:
			type_art_part.pop(k)
		elif val:
			type_art_part[k] = val
	type_dic[part] = type_art_part
	return type_dic

def get_article_types(self):
	return self.Get_details_data(self.type_article_fic)

def get_type_article_name(self,ident):
	if ident:
		return self.get_this_type_article(ident).get('nom',str())
	else:
		return str()		

def get_type_article_ident(self,name):
	dic = {dic.get('nom'):dic.get('id') 
		for dic in self.get_article_types().values()}
	return dic.get(name,str())

def get_this_type_article(self,ident):
	ident = self.redo_ident(ident)
	return self.get_article_types().get(ident,dict())

