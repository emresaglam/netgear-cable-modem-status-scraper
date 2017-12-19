import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import json

class Client(QWebPage):
	def __init__(self, url):
		self.app = QApplication(sys.argv)
		QWebPage.__init__(self)
		self.loadFinished.connect(self.on_page_load)
		self.mainFrame().load(QUrl(url))
		self.app.exec_()

	def on_page_load(self):
		self.app.quit()

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

USERNAME = data["admin_username"]
PASSWORD = data["admin_password"]
HOST = data["modem_ip"]

auth_token = HTTPBasicAuth(USERNAME, PASSWORD)
url = "http://{}:{}@{}/DocsisStatus.htm".format(USERNAME, PASSWORD, HOST)
client_response = Client(url)
html_source = client_response.mainFrame().toHtml()

soup = BeautifulSoup(str(html_source), "html.parser")
dsTable = soup.find_all(id="dsTable")
trs = dsTable[0].find_all("tr")
channelData = []
channel = {}
row = 0
for tr in trs:
	if row > 0 :
		columns = tr.find_all("td")
		channel["id"] = int(columns[0].text)
		channel["status"] = columns[1].text
		channel["frequency"] = columns[4].text
		channel["power"] = columns[5].text
		channel["snr"] = columns[6].text
		channel["correctables"] = int(columns[7].text)
		channel["uncorrectables"] = int(columns[8].text)
		#Must use copy() here for python's dictionary's pointer like behavior
		channelData.append(channel.copy())
	row = row + 1

lockedCount = 0
uncorrectableCount = 0
totalUncorrectableError = 0
for ch in channelData:
	if ch["status"] == "Locked":
		lockedCount += 1
	if ch["uncorrectables"] > 0:
		uncorrectableCount += 1
		totalUncorrectableError = totalUncorrectableError + int(ch["uncorrectables"])
cableConnection = {}
cableConnection["locked_count"] = lockedCount
cableConnection["uncorrectable_error_count"] = uncorrectableCount
cableConnection["total_uncorrectable_error"] = totalUncorrectableError
cableConnection["channel_info"] = channelData

channelsInfo = json.dumps(cableConnection)

print channelsInfo

