#Coding:utf-8

class fournisseurs:
	from .fournisseur import (get_fournisseur_format,save_fournisseur,
		delete_fournisseur,update_fournisseur,get_fournisseur,
		save_cmd_of_this_fournisseur,save_paie_of_this_fournisseur,
		up_fourn_histo_cmd,up_fourn_histo_pay,forun_fic)

	def fournisseur_handler(self,msg):
		action = msg.get('action')
		where = msg.get("where")
		inf = None
		if not action:
			inf = False
			
		elif action.lower() == "save":
			inf = self.save_fournisseur(where,msg.get('data'),
				msg.get('date'))
			
		elif action.lower() == "get":
			inf = self.get_fournisseur(where,msg.get('id'))
		
		elif action.lower() == 'update':
			inf = self.update_fournisseur(where,msg.get('data'))
		
		elif action.lower() == 'delete':
			inf = self.delete_fournisseur(where,msg.get('id'))

		return inf

