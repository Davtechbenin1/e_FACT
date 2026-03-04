#Coding:utf-8

class recettes:
	from .recettes import (get_recettes_format,save_recettes,
		get_recettes,delete_recettes,recette_fic)

	def recettes_handler(self,msg):
		action = msg.get('action')
		where = msg.get('where')
		inf = None
		if not action:
			inf = False
		elif action.lower() == "save":
			inf = self.save_recettes(where,msg.get('data'),
				msg.get('date'),msg.get('heure'))
			
		elif action.lower() == "get":
			inf = self.get_recettes(where,msg.get('id'))

		elif action.lower() == 'delete':
			inf = self.delete_recettes(where,msg.get('id'))
		return inf
	

