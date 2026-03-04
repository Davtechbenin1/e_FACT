#Coding:utf-8
class general:
	from .general import (_general_handler,get_general_data,
		save_general_data,update_general_data,
		delete_general_data,_general_msg_hand)
	
	from .ident_hand import (_ident_hand,get_ident_of,
		_get_real_ident_to,_save_ident_to,_get_ident_from,
		_delete_ident_from)

	def entreprise_handler(self,msg):
		id = "entreprise"
		return self._general_msg_hand(id,msg)
		
	def famille_handler(self,msg):
		id = "fam_art"
		return self._general_msg_hand(id,msg)

	def conditionement_handler(self,msg):
		id = "cond_art"
		return self._general_msg_hand(id,msg)