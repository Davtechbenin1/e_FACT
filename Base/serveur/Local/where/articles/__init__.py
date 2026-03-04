#Coding:utf-8

class articles:
	from .articles import (get_article_format, save_article, get_article,
		update_article,delete_article,save_arr,save_pert,save_invent,
		save_transf,save_deskt_transf,save_stock_transf,correct_stock,
		acurate_stock,save_vent,save_retour,article_fic)

	from .param import (conditionement_format,grille_format,save_conditionements,
		save_grilles,get_conditionements,get_grilles,get_part_parametre,
		save_part_parametre,condition_fic,grille_fic)


	def articles_handler(self,msg):
		action = msg.get('action')
		inf = None
		where = msg.get('where')
		date = msg.get('date')
		if not action:
			inf = False
		elif action.lower() == "save":
			inf = self.save_article(where,msg.get('data'),
				date = date)
		elif action.lower() == "get":
			inf = self.get_article(where,msg.get('id'),
				)
		elif action.lower() == 'update':
			inf = self.update_article(where,msg.get('data'),
				msg.get('id'),)
		elif action.lower() == 'delete':
			inf = self.delete_article(where,msg.get('id'))
		return inf
