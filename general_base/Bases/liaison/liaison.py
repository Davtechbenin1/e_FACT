#Coding:utf-8
"""
	Gestion de la base des liaisons et des zone
	de livraison
"""

def zone_format(self):
	return {
		"id":str(),
		"pays":str(),
		"commune":str(),
		"arrondissement":str(),
		"quartier/village":str(),
		"clients":dict(),
		"magasins":dict(),
		"commandes":dict(),#Pour les magasins
		"livraisons":dict(),#Pour les clients
	}

def add_zone(self,dic):
	if not dic.get('id'):
		pays = dic.get('pays')
		dic["id"] = self.Get_th_ident(pays.upper(),
			pays.upper())
	
	fic = dic.get('id').split("N°")[0]
	self.Save_details_data(fic,dic)
	all_zone_dic = self.get_all_zone()
	fic_dic = all_zone_dic.get(dic.get('pays'),dict())
	arron_d = fic_dic.get(dic.get('commune',dict()))
	ident_lis = arron_d.get(dic.get('arrondissement',list()))
	if not ident_lis:
		ident_lis = list()
	if dic.get('id') not in ident_lis:
		ident_lis.append(dic.get('id'))
		arron_d[dic.get('arrondissement')] = ident_lis
		fic_dic[dic.get('commune')] = arron_d
		all_zone_dic[dic.get('pays')] = fic_dic
		self.Save_general_data(self.zone_livraison_fic,
			all_zone_dic)
	return dic.get('id')

def get_zone(self,ident):
	fic = ident.split("N°")[0]
	zone = self.Get_details_data(fic,ident)
	if not zone:
		zone = dict()
	return zone

def update_zone(self,zone):
	ident = zone.get('id')
	fic = ident.split('N°')[0]
	self.Save_details_data(fic,zone)

def get_all_zone(self):
	dic= self.Get_general_data(self.zone_livraison_fic)
	if not dic:
		dic = dict()
	return dic

def add_pays(self,pays):
	all_zone_dic = self.get_all_zone()
	if pays not in all_zone_dic:
		all_zone_dic[pays] = dict()
		self.Save_general_data(self.zone_livraison_fic,all_zone_dic)
		return True
	return "Ce pays existe déjà dans la base"

def add_commune(self,pays,commune):
	all_zone_dic = self.get_all_zone()
	pays_dic = all_zone_dic.get(pays,dict())
	if commune not in pays_dic:
		pays_dic[commune] = dict()
		all_zone_dic[pays] = pays_dic
		self.Save_general_data(self.zone_livraison_fic,all_zone_dic)
		return True
	return "Cette commune existe déjà dans la base"

def add_arrond(self,pays,commune,arrond):
	all_zone_dic = self.get_all_zone()
	pays_dic = all_zone_dic.get(pays,dict())
	comu_dic = pays_dic.get(commune,dict())
	if arrond not in comu_dic:
		comu_dic[arrond] = dict()
		pays_dic[commune] = comu_dic
		all_zone_dic[pays] = pays_dic
		self.Save_general_data(self.zone_livraison_fic,all_zone_dic)
		return True
	return "Cet Arrondissement existe déjà dans la base"

def get_zone_ident(self,pays,commune,arrond,village):
	all_zone_dic = self.get_all_zone()
	ident_list = all_zone_dic.get(pays,dict()).get(commune,
		dict()).get(arrond,list())
	vill_ident = [ident for ident in ident_list 
		if self.get_zone(ident).get('quartier/village'
			).lower() == village.lower()]
	if vill_ident:
		return vill_ident[0]
	else:
		return None

def get_all_pays(self):
	all_zone_dic = self.get_all_zone()
	return all_zone_dic.keys()

def get_commune_of(self,pays):
	all_zone_dic = self.get_all_zone()
	return all_zone_dic.get(pays,dict()).keys()

def get_arrondissement_of(self,pays,commune):
	all_zone_dic = self.get_all_zone()
	return all_zone_dic.get(pays,dict()).get(commune,dict()).keys()

def get_village_of(self,pays,commune,arrond):
	all_zone_dic = self.get_all_zone()
	ident_list = all_zone_dic.get(pays,dict()).get(commune,
		dict()).get(arrond,list())
	vill_list = [self.get_zone(ident).get('quartier/village')
		for ident in ident_list]
	return vill_list


def get_zone_clients(self,ident):
	zone = self.get_zone(ident)
	return zone.get('clients',dict())

def get_zone_magasin(self,ident):
	zone = self.get_zone(ident)
	return zone.get('magasins',dict())

def get_zone_commandes(self,ident):
	zone = self.get_zone(ident)
	return zone.get('commandes',dict())

def get_zone_livraisons(self,ident):
	zone = self.get_zone(ident)
	return zone.get('livraisons',dict())

def add_zone_clients(self,ident,clt_ident,clt_name):
	zone = self.get_zone(ident)
	clt_dics = zone.get('clients')
	clt_dics[clt_ident] = clt_name
	zone['clients'] = clt_dics
	self.update_zone(zone)

def add_zone_magasins(self,ident,maga_ident,maga_name):
	zone = self.get_zone(ident)
	maga_dics = zone.get('magasins')
	maga_dics[maga_ident] = maga_name
	zone['magasins'] = maga_dics
	self.update_zone(zone)

def add_zone_commandes(self,ident,cmd_ident,cmd_mont):
	zone = self.get_zone(ident)
	cmd_dics = zone.get('commandes')
	cmd_dics[cmd_ident] = cmd_mont
	zone['commandes'] = cmd_dics
	self.update_zone(zone)

def add_zone_livraisons(self,ident,livrai_ident,livrai_mont):
	zone = self.get_zone(ident)
	livrai_dics = zone.get('livraisons')
	livrai_dics[livrai_ident] = livrai_mont
	zone['livraisons'] = livrai_dics
	self.update_zone(zone)

# Gestions des paramètrages de gestion des prix
def get_liaison(self):
	param_dic = self.Get_details_data(self.liaison_fic,self.liaison_fic)
	if not param_dic:
		param_dic = dict()
		param_dic['id'] = self.liaison_fic
		param_dic['liaison'] = dict()
		param_dic['general'] = dict()#Pour la gestion des options généraux
		self.Save_details_data(self.liaison_fic,param_dic)
	return param_dic.get('liaison')

def get_general(self):
	param_dic = self.Get_details_data(self.liaison_fic,self.liaison_fic)
	if not param_dic:
		param_dic = dict()
		param_dic['id'] = self.liaison_fic
		param_dic['liaison'] = dict()
		param_dic['general'] = dict()#Pour la gestion des options généraux
		self.Save_details_data(self.liaison_fic,param_dic)
	return param_dic.get('general')

def update_liason(self,liason_dic):
	param_dic = self.Get_details_data(self.liaison_fic,self.liaison_fic)
	param_dic['liaison'] = liason_dic
	self.Save_details_data(self.liaison_fic,param_dic)

def update_general(self,general_dic):
	param_dic = self.Get_details_data(self.liaison_fic,self.liaison_fic)
	param_dic['general'] = general_dic
	self.Save_details_data(self.liaison_fic,param_dic)

def save_liaison(self,source, desti, mont, both_size = True):
	all_liason = self.get_liaison()
	all_liason[self.get_ident_tup((source, desti))] = mont
	if both_size:
		all_liason[self.get_ident_tup((desti, source))] = mont
	self.update_liason(all_liason)

def get_ident_tup(self,tup):
	return '...'.join(tup)

def save_general(self,part,key_tup,ident_tup):
	"""
		Les parties ici sont:
		pays
		commune
		arrondissement

		key_tup représente le nom de nature des
		lieu généraux

		ident_tup représente le tuple des identifiants
		des points de racordement
	"""
	all_general = self.get_general()
	part_dic = all_general.get(part,dict())
	part_dic[self.get_ident_tup(key_tup)] = ident_tup
	all_general[part] = part_dic
	self.update_general(all_general)

def get_info_from_ident(self,ident,lis = list()):
		obj_dic = self.get_zone(ident)
		if not lis:
			lis = ["pays",'commune',"arrondissement","quartier/village"]
		if obj_dic:
			return ' -> '.join([obj_dic.get(i,str()) for i in lis])
		else:
			return str()

def get_param_str(self,key,mont):
	tup = key.split('...')
	if len(tup) == 2:
		orig,arri = tup
		all_dic = self.get_liaison()
		print(tup)
		invers = all_dic.get(self.get_ident_tup((arri,orig)),float())
		dic = {
			"id":key,
			"id origine":orig,
			"id arrivée":arri,
			"Origine":self.get_info_from_ident(orig),
			"Arrivée":self.get_info_from_ident(arri),
			"Montant":mont,
			"Inverse":invers,
			"Commande":len(self.get_zone_commandes(orig)),
			"Livraison":len(self.get_zone_livraisons(orig))
		}
		return dic
	return dict()




