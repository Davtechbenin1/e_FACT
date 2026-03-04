#Coding:utf-8

class depenses:
	from .depenses import (get_depenses_format,save_depenses,
		get_depenses,delete_depenses,depense_fic)

	def depenses_handler(self,msg):
		action = msg.get('action')
		where = msg.get('where')
		inf = None
		if not action:
			inf = False
		elif action.lower() == "save":
			inf = self.save_depenses(where,msg.get('data'),
				msg.get('date'),msg.get('heure'))
			
		elif action.lower() == "get":
			inf = self.get_depenses(where,msg.get('id'))

		elif action.lower() == 'delete':
			inf = self.delete_depenses(where,msg.get('id'))
		return inf
	

