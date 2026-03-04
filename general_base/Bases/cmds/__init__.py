#Coding:utf-8

class cmds:
	from .commandes import (cmd_format,add_cmd,update_cmd,get_cmd,
		get_original_cmd,get_type_of_cmd,add_type_of_cmd,up_all_cmd_base,
		get_all_cmd_base,get_all_cmd_base_of,update_type_of_cmd,_add_cmd)
	
	from .gestion_commandes import (modif_this_cmd,paie_this_cmd,
		livre_this_cmd,set_live_to,confirmer_cmd,anuler_this_cmd,
		get_all_cmd_type_of,get_all_cmd_of,get_all_cmd_orig_of)