#Coding:utf-8

class clients:
	from .clients import (client_fic,get_client_format,save_client,
		delete_client,update_client,get_client,save_cmd_of_this_client,
		save_paie_of_this_client,up_histo_cmd,up_histo_pay)

	def clients_handler(self,msg):
		action = msg.get('action')
		where = msg.get("where")
		inf = None
		if not action:
			inf = False
			
		elif action.lower() == "save":
			inf = self.save_client(where,msg.get('data'),
				date = msg.get('date'))
			
		elif action.lower() == "get":
			inf = self.get_client(where,msg.get('id'))
		
		elif action.lower() == 'update':
			inf = self.update_client(where,msg.get('data'))
		
		elif action.lower() == 'delete':
			inf = self.delete_client(where,msg.get('id'))

		return inf

