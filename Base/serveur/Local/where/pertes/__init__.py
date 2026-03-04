#Coding:utf-8
class pertes:
	from .pertes import (get_perte_format,save_perte,
		update_perte,get_perte,delete_perte,
		livre_perte,perte_fic)

	def pertes_handler(self,msg):
		action = msg.get('action')
		where = msg.get('where')
		inf = None
		if not action:
			inf = False
		elif action.lower() == "save":
			inf = self.save_perte(where,msg.get('data'),
				msg.get('date'))
			
		elif action.lower() == "get":
			inf = self.get_perte(where,msg.get('id'))

		elif action.lower() == 'update':
			inf = self.update_perte(where,msg.get('data'))

		elif action.lower() == 'delete':
			inf = self.delete_perte(where,msg.get('id'))
		return inf
	