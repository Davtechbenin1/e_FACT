#Coding:utf-8
class arrivages:
	from .arrivages import (get_arrivage_format,save_arrivage,
		update_arrivage,get_arrivage,delete_arrivage,
		livre_arrivage,retourn_arrivage,arri_fic)

	def arrivages_handler(self,msg):
		action = msg.get('action')
		where = msg.get('where')
		date = msg.get('date')
		inf = None
		if not action:
			inf = False
		elif action.lower() == "save":
			inf = self.save_arrivage(where,msg.get('data'),
				date = date)
			
		elif action.lower() == "get":
			inf = self.get_arrivage(where,msg.get('id'),
				date = date)

		elif action.lower() == 'update':
			inf = self.update_arrivage(where,msg.get('data'),
				date = date)

		elif action.lower() == 'delete':
			inf = self.delete_arrivage(where,msg.get('id'),
				date = date)
		return inf
	