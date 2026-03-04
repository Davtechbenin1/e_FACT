#Coding:utf-8
"""
	Gestion des méthodes divers servant de pont entre la
	base et l'interface
"""
import hashlib
#'''
# Gestion des entreprises:
def Get_ent_part(self,part):
	dic = self.get_entreprise()
	return dic.get(part,str())

# Gestion des recettes
def Get_all_paiement_of(self,date_liste):
	all_recette_list = self.get_recette_history()
	all_dic = dict()
	for date in date_liste:
		dic = all_recette_list.get(date,dict())
		for ident in dic.keys():
			all_dic[ident] = self.get_recette(ident)
		
	return all_dic

# Gestion de lé génération de code
def Genere_code(self,data: str) -> str:
	sha = hashlib.sha256()
	sha.update(data.encode('utf-8'))
	liste = sha.hexdigest()[:15]
	print('_______________________________')
	print(liste)
	return liste

# Gestion des accèss logiciel
def Get_access_of(self,part):
	return ["lectures","écritures"]

# Gestions divers
def adresse_of(self,id_clt):
	clt_dic = self.get_client(id_clt)
	return f"{clt_dic.get('pays',str())}, {clt_dic.get('ville')}, {clt_dic.get('quartier')}, {clt_dic.get('maison')}".strip()

def Get_autre_mont_of(self,cmd_dic):
	dic = cmd_dic.get('autre montant',dict())
	if dic:
		return sum(list(dic.values()))
	else:
		return int()

def Get_types_contrats(self):
	dic = {"Hebdomadaire":'Hebdomadaire',
		"Mensuelle":"Mensuelle",
		"Journalier":'Journalier'
		}
	return dic

def Get_types_contrats_list(self):
	return [i for i in self.Get_types_contrats()]

def Get_all_remb_form(self):
	return ("Hebdomadaire","Mensuelle","Journalier")

'''

txt = """Sigle:GSmart UserDurée:365Message:J'aimerai obtenir la licence de ZoeCorp pour une durée de 365 Jours. Pour bénéficier de 30 Jours suplémentaire.date:17-02-2026Montant:54750"""
def Genere_code(data: str) -> str:
	sha = hashlib.sha256()
	sha.update(data.encode('utf-8'))
	liste = sha.hexdigest()[:15]
	print(liste)
	return liste

Genere_code(txt)

#'''