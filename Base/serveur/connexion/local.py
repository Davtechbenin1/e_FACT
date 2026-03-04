#Coding:utf-8
"""
	Gestion de la base Local sqlite
"""
import sqlite3
from pathlib import Path
import json, sys
from datetime import datetime
import threading
import string
import traceback

def success_response(self,data,where,id,action):
	#self.up_cur_set()
	#self.cur.close()
	return {
		"status":'ok',
		"data":data,
		"message":f'{action} {where} at {id} went successfully',
		"action":action,
		"where":where
	}

def up_cur_set(self):
	if self.cur:
		#self.cur.close()
		self.cur = self.conn.cursor()

def failed_response(self,data,where,id,action,E = None):
	if not E:
		E = traceback.format_exc()
	#self.up_cur_set()
	#self.cur.close()
	return {
		"status":'error',
		"data":data,
		"message":f'{action} {where} at {id} went wrong. \n this is what goes wrong:\n{E}',
		"action":action,
		"where":where
	}

def open_local_connexion(self):
	Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

	# check_same_thread=False si tu comptes accéder depuis plusieurs threads (Kivy)
	self.conn = sqlite3.connect(self.db_path, timeout=5.0, check_same_thread=False)
	self.conn.row_factory = sqlite3.Row  # accès par noms de colonnes
	cur = self.conn.cursor()

	# PRAGMAs conseillés pour mobile
	cur.execute("PRAGMA journal_mode=WAL;")
	cur.execute("PRAGMA synchronous=NORMAL;")
	cur.execute("PRAGMA foreign_keys=ON;")
	cur.execute("PRAGMA busy_timeout=5000;")  # ms
	#self.cur.close()
	
def close_local_connexion(self):
	"""Ferme proprement la base."""
	if self.cur:
		#self.cur.close()
		self.cur = None
	if self.conn:
		self.conn.close()
		self.conn = None

def create_table(self, where: str):
	"""
	Crée une table au format Progest si elle n'existe pas déjà.
	- id : clé unique auto-incrémentée
	- data : JSON stocké en texte
	- updated_at : horodatage ISO8601
	"""
	#print(where)
	cur = self.conn.cursor()
	if where not in self.created_table:
		sql = f"""
		CREATE TABLE IF NOT EXISTS {where} (
			id TEXT PRIMARY KEY,
			data TEXT NOT NULL,
			updated_at TIMESTAMP NOT NULL
		)
		"""
		self.created_table.add(where)
		#try:
		cur.execute(sql)
		self.conn.commit()
	return cur
	#	except Exception as E:
	##		print(E)
# ------------------
def update_data(self,where,data,id):
	#try:

	#self.up_cur_set()
	where = self.redo_ident(where)
	cur = self.create_table(where)

	# récupérer l’existant
	#print(where,id)
	#sys.exit()
	th_data = self._get_data(where, id) or {}
	th_data.update(data)

	now = datetime.utcnow().isoformat()
	#print(where,data,id)

	sql = f"""
	INSERT INTO {where} (id, data, updated_at)
	VALUES (?, ?, ?)
	ON CONFLICT(id)
	DO UPDATE SET
		data = excluded.data,
		updated_at = excluded.updated_at
	"""
	#print(th_data)
	
	cur.execute(sql, (id, json.dumps(th_data), now))
	self.conn.commit()

	# cache APRÈS succès DB
	self._up_cache_local(where, th_data, id)

	ret = self.success_response( data, where, id, "update")
	cur.close()
	#except Exception as E:
	#	ret = self.failed_response(data,where,id,"update")

	return ret

def save_data(self,where,data,id):
	return self.update_data(where,data,id)

def _get_data(self,where,id):
	#self.up_cur_set()
	where = self.redo_ident(where)
	tab_cache = self._local_cache.get(where, {})
	cur = self.conn.cursor()
	if id:
		#if id in tab_cache:
		#	return tab_cache[id]
		#else:
		sql = f"SELECT id, data FROM {where} WHERE id = ?"
		cur.execute(sql, (id,))
		row = cur.fetchone()
		cur.close()
		if row:
			data = json.loads(row['data'])
			if data:
				self._up_cache_local(where,data,id)
			return data or dict()
		else:
			return dict()
	
	else:
		#if not tab_cache:
		sql = f"SELECT id, data FROM {where}"
		cur.execute(sql)
		rows = cur.fetchall()
		cur.close()
		tab_cache = {row['id']:json.loads(row['data'])
			for row in rows}
		#if tab_cache:
		#	self._up_cache_local(where,tab_cache)
		return tab_cache or dict()

def get_data(self, where: str, id: str = None):
	#try:
	self.create_table(where)
	data = self._get_data(where,id)
	ret = self.success_response(data,where,id,'get')
	#except Exception as E:
	#	ret = self.failed_response(dict(),where,id,'get')
	return ret

def delete_data(self, where: str, id: str):
	#try:
	#self.up_cur_set()
	where = self.redo_ident(where)
	cur = self.create_table(where)

	# --- Suppression en base ---
	sql = f"DELETE FROM {where} WHERE id = ?"
	cur.execute(sql, (id,))
	deleted = cur.rowcount > 0  # True si suppression effective
	cur.close()
	# --- Suppression du cache ---
	if deleted:
		tab_cache = self._local_cache.get(where, {})
		if id in tab_cache:
			with self._lock_dict.setdefault(where,
				threading.Lock()):
				del tab_cache[id]
				self._local_cache[where] = tab_cache

	ret = self.success_response(dict(),where,id,"delete")
	#except:
	#	ret = self.failed_response(dict(),where,id,"delete")
	return ret
# ------------------
def redo_ident(self,where):
	if where:
		p = "1234567890_"+string.ascii_lowercase
		th_txt = str()
		for i in where.lower():
			if i not in p:
				i = "xx"
			th_txt += i
		return th_txt
	return str()

def _up_cache_local(self,where,data,id = None):
	with self._lock_dict.setdefault(where,threading.Lock()):
		tab_dic = self._local_cache.get(where,dict())
		if id:
			tab_dic[id] = data
		else:
			tab_dic.update(data)
		self._local_cache[where] = tab_dic

