#Coding:utf-8

class stocks:
	from .type_articles import (type_article_format,update_type_article,add_article_to_type,
		sup_article_from_type,up_article_type_part,sup_article_type_part,get_article_types,
		get_type_article_name,get_this_type_article,get_type_article_ident)

	from .articles import (article_format,add_article,update_article,get_article,
		save_part_of_article,update_articles_after,destocker,stocker,get_article_names)

	from .categorie import (categorie_format,update_categorie,add_article_to_categorie,
		sup_article_from_categorie,up_categorie_part,sup_categorie_part,get_categories,
		get_categorie_name,get_this_categorie,get_categorie_ident)

	from .magasin import (magasin_format,update_magasin,add_article_to_magasin,
		sup_article_from_magasin,up_magasin_part,sup_magasin_part,get_magasins,
		get_magasin_name,get_this_magasin,get_magasin_ident,up_zone_mag,get_zone_mag,
		get_article_of_magasin)

	from .autres import (conditionement_format,grille_format,save_conditionements,save_grilles,
		get_conditionements,get_grilles,get_part_parametre,save_part_parametre)

	from .articles_to_show import (All_article_to_show,setting_price,from_3,get_my_redone_art,
		)
