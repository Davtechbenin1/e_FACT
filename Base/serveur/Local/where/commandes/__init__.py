#Coding:utf-8
class commandes:
	from .commandes import (get_cmd_format,save_cmd,update_cmd,
		get_cmd,delete_cmd,livre_cmd,retourn_cmd,cmd_fic,
		paiement_commande,update_plan_paie)

	from .historique import (save_cmd_non_solder,save_cmd_solder,
		get_cmd_non_solder,get_cmd_solder,_cmd_hist,delete_cmd_non_solder,
		delete_cmd_solder)

	def cmd_handler(self,msg):
		action = msg.get('action')
		where = msg.get('where')
		inf = None
		if not action:
			inf = False
		elif action.lower() == "save":
			inf = self.save_cmd(where,msg.get('data'),
				msg.get('date'))
			
		elif action.lower() == "get":
			inf = self.get_cmd(where,msg.get('id'))

		elif action.lower() == 'update':
			inf = self.update_cmd(where,msg.get('data'))

		elif action.lower() == 'delete':
			inf = self.delete_cmd(where,msg.get('id'))
		return inf

	def cmd_hist_handler(self,msg):
		action = msg.get('action')
		where = msg.get('where')
		inf = None
		if not action:
			inf = False
		elif action.lower() == "get":
			# id est soit: non_solder ou solder
			data = self._cmd_hist(where,msg.get('id'))
			inf = self.success_response(data,where,
				msg.get('id'),action)
		else:
			inf = self.failed_response({},
				where,msg.get("id"),action,
				E = "Action non valide")

		return inf
	