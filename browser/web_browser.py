import sys, pickle, os, urllib2, pymsgbox
from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl, QString, QSize
from PyQt4.QtWebKit import QWebView, QWebPage
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

if(os.path.exists("bookmarks.txt")):
	b = open("bookmarks.txt","rb")
	try:
		bookmarks = pickle.loads(b.read())
	except:
		bookmarks = list()
	b.close()
else:
	b = open("bookmarks.txt","w")
	b.close()

url = ""

def check_connection():
	try:
		# Only reason to connect to this link : the site is very lightweight !
		response=urllib2.urlopen('http://motherfuckingwebsite.com',timeout=5)
		return True
	except:
		return False

class JavaScriptEvaluator(QLineEdit):
	def __init__(self, page):
		super(JavaScriptEvaluator, self).__init__()
		self.page = page
		self.returnPressed.connect(self._return_pressed)

	def _return_pressed(self):
		frame = self.page.currentFrame()
		result = frame.evaluateJavaScript(self.text())

class RequestsTable(QTableWidget):
	header = ["url", "status", "content-type"]

	def __init__(self):
		super(RequestsTable, self).__init__()
		self.setColumnCount(3)
		self.setHorizontalHeaderLabels(self.header)
		header = self.horizontalHeader()
		header.setStretchLastSection(True)
		header.setResizeMode(QHeaderView.ResizeToContents)

	def update(self, data):
		last_row = self.rowCount()
		next_row = last_row + 1
		self.setRowCount(next_row)
		for col, dat in enumerate(data, 0):
			if not dat:
				continue
			self.setItem(last_row, col, QTableWidgetItem(dat))

class Manager(QNetworkAccessManager):
	def __init__(self, table):
		QNetworkAccessManager.__init__(self)
		self.finished.connect(self._finished)
		self.table = table

	def _finished(self, reply):
		headers = reply.rawHeaderPairs()
		headers = {str(k):str(v) for k,v in headers}
		content_type = headers.get("Content-Type")
		url = reply.url().toString()
		try:
			status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
			status, ok = status.toInt()
			self.table.update([url, str(status), content_type])
		except:
			pass

class Main(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.initUI()

	def initUI(self):
		self.grid = QGridLayout()
		
		self.url_input = QLineEdit(self)
		self.url_input.setFixedWidth(1350)
		self.url_input.returnPressed.connect(self.Enter)

		self.BackButton = QPushButton('', self)
		self.BackButton.setIcon(QIcon('icons/back.png'))
		self.BackButton.setIconSize(QSize(40,20))
		self.BackButton.setFixedWidth(40)
		self.BackButton.setFixedHeight(30)
		self.BackButton.clicked.connect(self._go_back)

		self.ForwardButton = QPushButton('', self)
		self.ForwardButton.setIcon(QIcon('icons/forward.png'))
		self.ForwardButton.setIconSize(QSize(40,20))
		self.ForwardButton.setFixedWidth(40)
		self.ForwardButton.setFixedHeight(30)
		self.ForwardButton.clicked.connect(self._go_forward)

		self.ReloadButton = QPushButton('', self)
		self.ReloadButton.setIcon(QIcon('icons/refresh.png'))
		self.ReloadButton.setIconSize(QSize(40,20))
		self.ReloadButton.setFixedWidth(40)
		self.ReloadButton.setFixedHeight(30)
		self.ReloadButton.clicked.connect(self._refresh)

		self.StopButton = QPushButton('', self)
		self.StopButton.setIcon(QIcon('icons/stop.png'))
		self.StopButton.setIconSize(QSize(40,20))
		self.StopButton.setFixedWidth(40)
		self.StopButton.setFixedHeight(30)
		self.StopButton.clicked.connect(self._stop)

		self.BookButton = QPushButton("",self)
		self.BookButton.setIcon(QIcon('icons/un-bookmark.png'))
		self.BookButton.setIconSize(QSize(40,20))
		self.BookButton.setFixedWidth(40)
		self.BookButton.setFixedHeight(30)
		self.BookButton.clicked.connect(self._bookmark)

		# Don't know to adjust padding between the buttons, so making this shitty invisible space eater item to eat the space :D
		self.SpaceEater = QSpacerItem(1300, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
		
		self.SpaceEater2 = QSpacerItem(5, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

		self.list = QComboBox(self)
		self.list.setFixedHeight(27)

		for urls in bookmarks:
			self.list.addItem(urls)

		self.list.activated[str].connect(self.handle_bookmarks)
		self.list.view().setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)

		self.layout = QGridLayout()

		self.layout.addWidget(self.BackButton,1,0)
		self.layout.addItem(self.SpaceEater2,1,1)
		self.layout.addWidget(self.ForwardButton,1,2)
		self.layout.addItem(self.SpaceEater2,1,3)
		self.layout.addWidget(self.ReloadButton,1,4)
		self.layout.addItem(self.SpaceEater2,1,5)
		self.layout.addWidget(self.StopButton,1,6)
		self.layout.addItem(self.SpaceEater,1,7)
		self.layout.addWidget(self.BookButton,1,8)
		self.layout.addItem(self.SpaceEater2,1,9)
		self.layout.addWidget(self.list,1,10)

		self.progress_bar = QProgressBar()
		self.progress_bar.setMaximumWidth(120)

		self.status = self.statusBar()
		self.status.addPermanentWidget(self.progress_bar)
		self.status.hide()

		self.browser = QWebView(loadProgress = self.progress_bar.setValue,
						loadFinished = self.progress_bar.hide,
						loadStarted = self.progress_bar.show,
						titleChanged = self.setWindowTitle)

		self.requests_table = RequestsTable()
		self.requests_table.hide()

		self.manager = Manager(self.requests_table)
		self.page = QWebPage()
		self.page.setNetworkAccessManager(self.manager)
		self.browser.setPage(self.page)

		self.info_grid = QGridLayout()

		self.info_label1 = QLabel("Requests Console")
		self.hide_requests_table = QPushButton("+")
		self.hide_requests_table.setFixedWidth(80)
		self.hide_requests_table.clicked.connect(self._hide_RequestsTable)

		self.info_grid.addWidget(self.info_label1,0,0)
		self.info_grid.addWidget(self.hide_requests_table,0,1)

		self.info_label2 = QLabel("JS Evaluator")

		self.js_eval = JavaScriptEvaluator(self.page)

		self.grid.addWidget(self.url_input,0,0)
		self.grid.addItem(self.layout,1,0)
		self.grid.addWidget(self.browser, 2, 0)
		self.grid.addItem(self.info_grid)
		self.grid.addWidget(self.requests_table, 4, 0)
		self.grid.addWidget(self.info_label2, 5, 0)
		self.grid.addWidget(self.js_eval, 6, 0)

		self.main_frame = QWidget()
		self.main_frame.setLayout(self.grid)

		self.setCentralWidget(self.main_frame)
		self.setWindowTitle('PySurf')

		self.browser.urlChanged.connect(self.UrlChanged)
		self.browser.page().linkHovered.connect(self.LinkHovered)

	def _hide_RequestsTable(self):
		if(self.hide_requests_table.text() == "-"):
			self.hide_requests_table.setText("+")
			self.requests_table.hide()
		else:
			self.hide_requests_table.setText("-")
			self.requests_table.show()

	def UrlChanged(self):
		self.url_input.setText(self.browser.url().toString())

	def LinkHovered(self,l):
		self.status.showMessage(l)

	def Enter(self):
		global url
		global bookmarks

		url = self.url_input.text()

		http = "http://"
		www = "www."

		if(www in url and http not in url):
			url = http + url

		elif("." not in url):
			url = "http://www.google.com/search?q="+url

		elif(http in url and www not in url):
			url = url[:7] + www + url[7:]

		elif(http and www not in url):
			url = http + www + url

		self.url_input.setText(url)

		self.browser.load(QUrl(url))

		if(url in bookmarks):
			self.BookButton.setIcon(QIcon('icons/bookmark.png'))
			self.BookButton.setIconSize(QSize(40,20))
		else:
			self.BookButton.setIcon(QIcon('icons/un-bookmark.png'))
			self.BookButton.setIconSize(QSize(40,20))

		self.status.show()

	def _go_back(self):
		self.page.triggerAction(QWebPage.Back)

	def _go_forward(self):
		self.page.triggerAction(QWebPage.Forward)

	def _refresh(self):
		self.page.triggerAction(QWebPage.Reload)

	def _stop(self):
		self.page.triggerAction(QWebPage.Stop)

	def _bookmark(self):
		global url
		global bookmarks

		if(url in bookmarks):
			idx = bookmarks.index(url)
			bookmarks.remove(url)
			b = open("bookmarks.txt","wb")
			pickle.dump(bookmarks,b)
			b.close()
			self.BookButton.setIcon(QIcon('icons/un-bookmark.png'))
			self.BookButton.setIconSize(QSize(40,20))
			self.list.removeItem(idx)
		else:
			bookmarks.append(url)
			b = open("bookmarks.txt","wb")
			pickle.dump(bookmarks,b)
			b.close()
			self.BookButton.setIcon(QIcon('icons/bookmark.png'))
			self.BookButton.setIconSize(QSize(40,20))
			self.list.addItem(url)

	def handle_bookmarks(self, choice):
		global url

		url = choice
		self.url_input.setText(url)
		self.Enter()

if(__name__ == '__main__'):
	network_available = False

	while(network_available == False):
		network_available = check_connection()
		if(network_available == False):
			pymsgbox.alert(text = "No Internet Connection found !", title = "Alert", button = "Retry")

	app = QApplication(sys.argv)
	window = Main()
	window.showMaximized()

	sys.exit(app.exec_())