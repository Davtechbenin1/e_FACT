#Coding:utf-8
class comptes:
	from .comptes import (get_compte_format,
		update_compte,get_compte,delete_compte,save_recettes_to,
		save_depenses_to,update_cmpt_solde,save_compte,compt_fic)

	def comptes_handler(self,msg):
		action = msg.get('action')
		where = msg.get('where')
		inf = None
		if not action:
			inf = False
		elif action.lower() == "save":
			inf = self.save_compte(where,msg.get('data'),
				msg.get('date'))
			
		elif action.lower() == "get":
			inf = self.get_compte(where,msg.get('id'))

		elif action.lower() == 'update':
			inf = self.update_compte(where,msg.get('data'))

		elif action.lower() == 'delete':
			inf = self.delete_compte(where,msg.get('id'))
		return inf
	