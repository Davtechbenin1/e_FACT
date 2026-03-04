#Coding:utf-8

def _general_handler(self,fonc,*args):
	where = "general"
	return fonc(where,*args)

def get_general_data(self,id = None):
	"""
		Ici les id seront le plus souvent le nom des parties
		de gestion.
	"""
	if id:
		id = self.redo_ident(id)
	return self._general_handler(self.get_data,id)

def save_general_data(self,data,id):
	return self._general_handler(self.save_data,data,id)

def update_general_data(self,data,id):
	return self._general_handler(self.update_data,data,id)

def delete_general_data(self,id):
	return self._general_handler(self.delete_data,id)

def _general_msg_hand(self,id,msg):
	inf = None
	action = msg.get('action')
	th_id = msg.get('id')
	if not action:
		inf = False
	elif action.lower() == "save":
		inf = self.save_general_data(msg.get('data'),id)
	elif action.lower() == "get":
		inf = self.get_general_data(id)
		if th_id:
			inf_data = inf.get("data")
			inf = self.success_response(
				inf_data,inf.get("where"),th_id,"get")
	elif action.lower() == 'update':
		inf = self.update_general_data(msg.get('data'),id)
	elif action.lower() == 'delete':
		inf = self.delete_general_data(id)
	return inf
