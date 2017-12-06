import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth

class Client(QWebPage):
	def __init__(self, url):
		self.app = QApplication(sys.argv)
		QWebPage.__init__(self)
		self.loadFinished.connect(self.on_page_load)
		self.mainFrame().load(QUrl(url))
		self.app.exec_()

	def on_page_load(self):
		self.app.quit()

USERNAME = "CHANGEME"
PASSWORD = "CHANGEME"

auth_token = HTTPBasicAuth(USERNAME, PASSWORD)
url = "http://{}:{}@192.168.100.1/DocsisStatus.htm".format(USERNAME, PASSWORD)
client_response = Client(url)
html_source = client_response.mainFrame().toHtml()

soup = BeautifulSoup(str(html_source), "html.parser")
dsTable = soup.find_all(id="dsTable")
trs = dsTable[0].find_all("tr")
channels = []
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
		channels.append(channel)
	row = row + 1

print channels

