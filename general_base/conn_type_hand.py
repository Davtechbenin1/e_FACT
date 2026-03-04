#"""
import os,requests
from lib.davbuild import *
def Def_Con(self):
	try:
		con = self.Connecte_to()
		if con:
			self.last_updated = {
				"general": "2025-05-01T00:00:00Z",
				"details": "2025-05-01T00:00:00Z"
			}
			self.All_data_Table = dict()

			api_url = "https://perfect-vibrancy-production.up.railway.app"
			ws_url = api_url.replace("https", "wss") + "/ws"

			ws = websocket.WebSocketApp(
				ws_url,
				on_message=self.on_message,
				on_open=self.on_open
			)

			cert_path = os.path.join(os.getcwd(), "media", "cacert.pem")
			#print(cert_path)
			ssl_context = ssl.create_default_context(cafile=cert_path)

			t = threading.Thread(target=lambda: ws.run_forever(sslopt={"context": ssl_context}), daemon=True)
			t.start()

	except requests.exceptions.ConnectionError as e:
		inf_dic = Get_local_json('CON_INFO')
		con = False

	return con
	
def Connecte_to(self):
	api_url = os.getenv("API_URL", "https://perfect-vibrancy-production.up.railway.app")
	self.th_url = f"{api_url}/api/"
	self.session.get(self.th_url + f"open_table/{self.th_entreprise}")
	return True


"""
import requests, websocket, threading
from lib.davbuild import *
def Def_Con(self):
	try:
		con = self.Connecte_to()
		if con:
			self.last_updated = {
				"general": "2025-05-01T00:00:00Z",
				"details": "2025-05-01T00:00:00Z"
			}
			self.Table_Base = dict()
			self.All_data_Table = dict()
			self.All_data_updated = dict()

			inf_dic = Get_local_json('CON_INFO')
			host = inf_dic.get('host') or "localhost"
			port = inf_dic.get('port') or 8010
	
			ws = websocket.WebSocketApp(
				f"ws://{host}:{port}/ws",
				on_message=self.on_message,
				on_open=self.on_open)

			t = threading.Thread(target=ws.run_forever, 
				daemon=True)
			t.start()
			time.sleep(1)

	except requests.exceptions.ConnectionError as e:
		inf_dic = Get_local_json('CON_INFO')
		self.sc.add_connex_info(**inf_dic)
		con = False
	
	return con
	
def Connecte_to(self):
	dic = {
		"host":"localhost",
		"port":'8010',
	}
	inf_dic = Get_local_json('CON_INFO')
	if not inf_dic:
		inf_dic = dic
		Save_local_json('CON_INFO',inf_dic)
	host = inf_dic.get('host') or "localhost"
	port = inf_dic.get('port') or 8010
	self.th_url = f"http://{host}:{port}/api/"
	self.session = requests.session()
	self.session.get(self.th_url+"open_table/ProGest")
	return True
#"""


def check_update(self):
	return self.get_curent_mobile_version()

def get_curent_apk(self,url):
	if "org.kivy.android" in sys.modules or "android" in sys.modules:
		from jnius import autoclass
		Intent = autoclass('android.content.Intent')
		Uri = autoclass('android.net.Uri')
		PythonActivity = autoclass('org.kivy.android.PythonActivity')

		intent = Intent(Intent.ACTION_VIEW)
		intent.setData(Uri.parse(url))
		intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
		PythonActivity.mActivity.startActivity(intent)
	else:
		import webbrowser
		webbrowser.open(url)
		