#Coding:utf-8
perte_fic = "pertes"
def get_perte_format(self,date):
	#id = self.get_ident_of(self.perte_fic,True,date)
	dic = {
		#"N°":id,
		"motif":str(),
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

def save_perte(self,where,cmd_dic,date):
	th_cmd = self.get_perte_format(date)
	id = cmd_dic.get('N°')
	th_cmd.update(cmd_dic)
	th_cmd["N°"] = id
	info = cmd_dic.get("montant TTC")

	self._save_ident_to(where, id, info,date)
	
	if th_cmd.get('status').lower() == "livrée":
		#print(th_cmd)
		self.livre_perte(where,th_cmd)
	return self.save_data(where, th_cmd, id)

def update_perte(self,where,cmd_dic):
	ident = cmd_dic.get('N°')
	info = cmd_dic.get("montant TTC")
	date = cmd_dic.get('date')
	self._save_ident_to(where, ident, info,date)
	if cmd_dic.get('status').lower() == "livrée":
		self.livre_perte(where,cmd_dic)
	return self.update_data(where, cmd_dic, ident)

def get_perte(self,where,ident:str=None):
	return self.get_data(where, ident)

def delete_perte(self,where,ident):
	return self.delete_data(where,ident)

# Gestion des actions spécifiques
def livre_perte(self,where,cmd_dic):
	mont_ttc = cmd_dic.get('montant TTC')
	articles = cmd_dic.get('articles')
	cmd_iden = cmd_dic.get('N°')
	mag = cmd_dic.get('magasin')
	for art_dic in articles.values():
		arr,part = where.split("_z_o_e_")
		WH = f"articles_z_o_e_{part}"
		self.save_pert(WH,art_dic, mag)



