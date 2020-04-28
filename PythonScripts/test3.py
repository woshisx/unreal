import main
import websocket
websocket.enableTrace(True)
from strack_api.strack import Strack
st = Strack(base_url="https://strack.teamones.com/", login_name="strack", password="strack")
token = st.get_event_server().get('token')
ws = main.Main("wss://log.teamones.com/wss?sign=%s"%token)
ws.start()