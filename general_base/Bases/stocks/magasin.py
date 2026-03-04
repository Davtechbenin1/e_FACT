#Coding:utf-8
def magasin_format(self):
	return {
		"id":self.Get_magasin_ident(),
		"nom":str(),
		"IFU":str(),
		'img':"media/logo.png",
		"articles":dict(),
		"stock":dict(),
		"ventes":dict(),
		"achats":dict(),
		"pertes":dict(),
		"inventaires":dict(),
		"adresse":{
			"Pays":str(),
			"Commune":str(),
			"Arrondissement":str(),
			"Quartier/Village":str(),
			"Indication":str()
		},
		"contact":{
			"Téléphone":str(),
			"Whatsapp":str(),
			"Email":str(),
		}
		}

def update_magasin(self,magasin_dic):
	zone = magasin_dic.get('adresse')
	lis = ["Pays","Commune","Arrondissement"]
	zone_txt = self.format_part([zone.get(i) for i in lis])
	self.up_zone_mag(zone_txt,magasin_dic.get('id'))
	self.Save_details_data(self.magasin_fic,magasin_dic)

def up_zone_mag(self,zone_txt,ident):
	all_mag_zon = self.get_zone_mag()
	mag_lis = all_mag_zon.get(zone_txt,list())
	mag_lis.append(ident)
	all_mag_zon[zone_txt] = mag_lis
	self.Save_general_data(self.magasin_fic+"Zone",all_mag_zon)

def get_zone_mag(self,zone_txt = str()):
	all_mag_zon = self.Get_general_data(self.magasin_fic+"Zone")
	if zone_txt:
		lis = list()
		ll = [all_mag_zon.get(txt) for txt in
			all_mag_zon.keys() if zone_txt.lower() in txt.lower()]
		for i in ll:
			lis.extend(i)
		return lis
	return all_mag_zon

def add_article_to_magasin(self,magasin_id,art_dic):
	"""
		Utiliser pour ajouter un article a un magasin donné
	"""
	magasin_dic = self.get_this_magasin(magasin_id)
	if not magasin_dic:
		return "identifiant de magasin invalide"
	magasin_dic["articles"][art_dic.get('id')] = art_dic.get('désignation')
	magasin_dic = self.up_magasin_part("stock",magasin_dic,art_dic)
	magasin_dic = self.up_magasin_part("ventes",magasin_dic,art_dic)
	magasin_dic = self.up_magasin_part("achats",magasin_dic,art_dic)
	magasin_dic = self.up_magasin_part("inventaires",magasin_dic,art_dic)
	self.update_magasin(magasin_dic)

def sup_article_from_magasin(self,magasin_id,art_dic):
	"""
		Utiliser pour retirer un article d'un magasin donné
	"""
	magasin_dic = self.get_this_magasin(magasin_id)
	if not magasin_dic:
		return "identifiant de magasin invalide"

	if art_dic.get('id') in magasin_dic['articles']:
		magasin_dic['articles'].pop(art_dic.get('id'))
	
	magasin_dic = self.sup_magasin_part("stock",magasin_dic,art_dic)
	magasin_dic = self.sup_magasin_part("ventes",magasin_dic,art_dic)
	magasin_dic = self.sup_magasin_part("achats",magasin_dic,art_dic)
	magasin_dic = self.sup_magasin_part("inventaires",magasin_dic,art_dic)
	self.update_magasin(magasin_dic)

def up_magasin_part(self,part,magasin_dic,art_dic):
	magasin_art_part = magasin_dic.get(part,dict())
	mag_part = art_dic.get(part).get(magasin_dic.get('id'),dict())
	for k,v in mag_part.items():
		val = magasin_art_part.get(k)
		if not val:
			val = 0
		magasin_art_part[k] = val + v
	magasin_dic[part] = magasin_art_part
	return magasin_dic

def sup_magasin_part(self,part,magasin_dic,art_dic):
	magasin_art_part = magasin_dic.get(part,dict())
	mag_part = art_dic.get(part).get(magasin_dic.get('id'),dict())
	for k,v in mag_part.items():
		val = magasin_art_part.get(k)
		if val:
			val -= v
		if not val:
			magasin_art_part.pop(k)
		elif val:
			magasin_art_part[k] = val
	magasin_dic[part] = magasin_art_part
	return magasin_dic

def get_magasins(self):
	return self.Get_details_data(self.magasin_fic)

def get_article_of_magasin(self,ident):
	return self.get_this_magasin(ident).get('articles')

def get_magasin_name(self,ident):
	if ident:
		return self.get_this_magasin(ident).get('nom',str())
	else:
		return str()

def get_magasin_ident(self,name):
	dic = {dic.get('nom'):dic.get('id') 
		for dic in self.get_magasins().values()}
	return dic.get(name,str())

def get_this_magasin(self,ident):
	ident = self.redo_ident(ident)
	return self.get_magasins().get(ident,dict())


