#Coding:utf-8
from lib.davbuild import *
from General_surf import *
from .model1 import ProInvoiceA4

def get_adress(self,ent_dic):
	inf = f"""{ent_dic.get('ville',str())} {ent_dic.get('pays',str())}"""
	if ent_dic.get('quartier'):
		inf += f"\n{ent_dic.get('quartier')}"
		if ent_dic.get('maison'):
			inf += f" {ent_dic.get('maison')}"
	elif ent_dic.get('maison'):
		inf += f"\n{ent_dic.get('maison')}"
	return inf

def get_fact_num(self,fact_id):
	ind = fact_id.split('N°')[-1]
	return ind.split("_")[-1][-3:]

def Factures_impression(self,cmd_dic):
	ent_p_dict = self.sc.DB.get_entreprise()
	clt_id = cmd_dic.get('client')
	fact_id = cmd_dic.get('N°')
	clt_dic = self.sc.DB.Get_this_clt(clt_id)
	company = {
		"name": ent_p_dict.get('sigle'),
		"address": self.get_adress(ent_p_dict),
		"phone": ent_p_dict.get('whatsapp',str()) or ent_p_dict.get('téléphone',str()),
		"email": ent_p_dict.get("email",str())
	}

	client = {
		"name": f"{clt_dic.get('nom')} {clt_dic.get('prénom',str())}",
		"address": self.get_adress(clt_dic)
	}
	items = list()
	mont_ht = float()

	for article in cmd_dic.get("articles").values():
		vente = article.get("ventes")
		prix = article.get("prix de vente")
		for key,qte in vente.items():
			if qte:
				dic = {
					"desc": article.get('Désignation'), 
					"qty": qte, 
					"unit_price": prix.get(key),
					"unité":key,
					"total": qte * prix.get(key)
				}
				mont_ht = qte * prix.get(key)
				items.append(dic)
	
	info_str = f"""\
date d'émission: {cmd_dic.get("date d'émission")}
date d'impression: {self.sc.get_today()}
heur d'impression: {self.sc.get_hour()}
Vendeur: {cmd_dic.get('auteur')}"""
	
	fact_name = f"{client.get('name').strip()}.pdf"

	pdf = ProInvoiceA4(GET_FILE_DIRECTORY(fact_name))
	pdf.add_header(company, f"PROFORMA N°{self.get_fact_num(fact_id)}", info_str)
	pdf.add_client_info(client)
	pdf.add_items(items)
	pdf.add_totals(mont_ht,
		0,get_autre_m(cmd_dic.get('autre montant')),
		cmd_dic.get('montant TTC'))
	pdf.add_footer("static/logo.png")
	pdf.build()

	open_pdf(fact_name)

def get_autre_m(dic):
	aut = int()
	for v in dic.values():
		aut += v
	return aut

#Gestion des accèss logiciel
def get_access(self,part):
	return True
	"""
		Ceci est pour la gestion des Menus principales du logiciel
	
	if self.sc.DB.curent_access == "All":
		return True
	else:
		if part in self.sc.DB.curent_access.keys():
			return True
	return False
	"""

