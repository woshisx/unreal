import sys,json,os
from strack_api.strack import Strack
st = Strack(base_url="https://strack.teamones.com/", login_name="chenxing", password="Zhuohua123")
print(st.login_name)