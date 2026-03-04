#Coding:utf-8
arri_fic = "arrivages"
def get_arrivage_format(self,date):
	dic = {
		#"N°":id,
		"fournisseur":str(),
		"bon_commande":str(),# Pour référencer la commande fournisseur choisi
		"magasin":str(),
		"date":date,
		"articles":dict(),
		'autres montant':dict(),
		"montant HT":float(),
		"taxes":float(),
		"montant TTC":float(),
		'status':"Livrée",
	}
	return dic

def save_arrivage(self,where,cmd_dic,date = None):
	if not date:
		date = self.sc.get_today()
	th_cmd = self.get_arrivage_format(date)
	id = cmd_dic.get('N°')
	th_cmd.update(cmd_dic)
	th_cmd["N°"] = id
	info = cmd_dic.get("montant TTC")

	self._save_ident_to(where, id, info,date)
	
	if th_cmd.get('status').lower() == "Livrée".lower():
		#print(th_cmd)
		self.livre_arrivage(where,th_cmd)
	return self.save_data(where, th_cmd, id)

def update_arrivage(self,where,cmd_dic,date = None):
	if not date:
		date = self.sc.get_today()
	ident = cmd_dic.get('N°')
	info = cmd_dic.get("montant TTC")
	self._save_ident_to(where, ident, info,date)
	if cmd_dic.get('status de la commande').lower() == "Livrée".lower():
		if cmd_dic.get("montant TTC") < 0:
			self.retourn_arrivage(where,cmd_dic)
		else:
			self.livre_arrivage(where,cmd_dic)
	return self.update_data(where, cmd_dic, ident)

def get_arrivage(self,where,ident:str=None,date = None):
	date = self.sc.get_today()
	return self.get_data(where, ident)

def delete_arrivage(self,where,ident,date = None):
	date = self.sc.get_today()
	return self.delete_data(where,ident)

# Gestion des actions spécifiques
def livre_arrivage(self,where,cmd_dic,date = None):
	mont_ttc = cmd_dic.get('montant TTC')
	articles = cmd_dic.get('articles')
	cmd_iden = cmd_dic.get('N°')
	mag = cmd_dic.get('magasin')
	fourn = cmd_dic.get('fournisseur').strip()
	ret = self.save_cmd_of_this_fournisseur(where,cmd_dic, False,
		date = date)
	if ret:
		for art_dic in articles.values():
			arr,part = where.split("_z_o_e_")
			WH = f"articles_z_o_e_{part}"
			self.save_arr(WH,art_dic, mag,fourn)

def retourn_arrivage(self,where,cmd_dic,date = None):
	mont_ttc = cmd_dic.get('montant TTC')
	articles = cmd_dic.get('articles')
	cmd_iden = cmd_dic.get('N°')
	mag = cmd_dic.get('magasin')
	ret = self.save_cmd_of_this_fournisseur(where,cmd_dic, True,
		date = date)
	if ret:
		for art_dic in articles.values():
			arr,part = where.split("_z_o_e_")
			WH = f"articles_z_o_e_{part}"
			self.save_pert(WH,art_dic, mag)
	


