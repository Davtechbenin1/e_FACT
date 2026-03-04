#Coding:utf-8
"""
	Cette classe permet maintenant de gérer la connexion entre
	le gestionnaire de service interne et l'application.

	Ici, on envoie et demande des données. Aucun traitement logique
	n'est fait.

	donc coté serveur, nous avons des api qui permette la gestion
	de chaque action-name en fonction du fichier.


	La gestion par magasin permet de préciser le type de donné,
	type de gestion a prendre en compte. Pour les magasins, nous
	avons les données générales disponibles de façon général.
"""
'''
trafic_format = {
	"action":"get" | "save" | "delete" | "update",
	"where":"fichier",
	"id":str(),
	"data":"JSONB",
	"trafic-id":"uuid",
	"date":str(),
	"heure":str()
}
'''
import uuid, datetime, sys

def formatage(self,action,where,magasin,data = dict(),id = None):
	date = self.sc.get_today()
	lis = ("article","clients","comptes","fournisseurs")
	all_list = ("clients","fournisseurs","articles","comptes",
		"arrivages","pertes","commandes","recettes","depenses",)
	if action == "save":
		last_ident = data.get('N°')
		if not last_ident and where.lower() in all_list:
			if where.lower() in lis:
				th_id = self.sc.DB._data_main_obj.get_ident_of(where,False)
			else:
				th_id = self.sc.DB._data_main_obj.get_ident_of(where,True,date)

			data['N°'] = th_id
	where += f"_z_o_e_{magasin}"
	
	trafic = {
		"action":action,
		"where":where.lower(),
		"id":id,
		"data":data,
		"trafic-id":f"{where} {uuid.uuid4()}",
		"date":date,
		"heure":self.sc.get_hour()
	}
	#print(trafic)
	ret = self._data_main_obj.message_handler(trafic)
	#print(ret)
	if ret.get('status') == "ok":
		dic = ret.get("data")
		return dic
	else:
		raise ValueError(ret.get('message'))

def get_data(self,where,id = None,magasin:str = "_all_data_hand_"):
	return formatage(self,"get",where, magasin, id = id)

def save_data(self,where,data,magasin:str = "_all_data_hand_"):
	return formatage(self,"save",where, magasin, data)

def delete_data(self,where,id,magasin:str = "_all_data_hand_"):
	return formatage(self,"delete", where, magasin, id = id)

def update_data(self,where,data,id,magasin:str = "_all_data_hand_"):
	return formatage(self,"update",where, magasin, data,id)

def get_history(self,where, date:str = None,magasin:str = "_all_data_hand_"):
	return formatage(self,"history",where,magasin,id = date)


