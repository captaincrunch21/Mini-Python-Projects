import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl, QString
from PyQt4.QtWebKit import QWebView, QWebPage
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

class UrlInput(QLineEdit):
    def __init__(self, browser):
        super(UrlInput, self).__init__()
        self.browser = browser
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        url = QUrl(self.text())
        browser.load(url)

class JavaScriptEvaluator(QLineEdit):
    def __init__(self, page):
        super(JavaScriptEvaluator, self).__init__()
        self.page = page
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        frame = self.page.currentFrame()
        result = frame.evaluateJavaScript(self.text())

class ActionBox(QWidget):
    def __init__(self,page):
        super(ActionBox, self).__init__()
        self.page = page

        self.BackButton = QPushButton('<-', self)
        self.BackButton.setFixedWidth(40)
        self.BackButton.clicked.connect(self._go_back)

        self.ForwardButton = QPushButton('->', self)
        self.ForwardButton.setFixedWidth(40)
        self.ForwardButton.clicked.connect(self._go_forward)

        self.ReloadButton = QPushButton('Refresh', self)
        self.ReloadButton.setFixedWidth(80)
        self.ReloadButton.clicked.connect(self._refresh)

        self.StopButton = QPushButton('Stop', self)
        self.StopButton.setFixedWidth(80)
        self.StopButton.clicked.connect(self._stop)

        # Don't know to adjust padding between the buttons, so making this shitty invisible space eater item to eat the space :D
        self.SpaceEater = QSpacerItem(1200, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        layout = QGridLayout(self)

        layout.addWidget(self.BackButton,0,1)
        layout.addWidget(self.ForwardButton,0,2)
        layout.addWidget(self.ReloadButton,0,3)
        layout.addWidget(self.StopButton,0,4)

        layout.addItem(self.SpaceEater,0,5)

    def _go_back(self):
        self.page.triggerAction(QWebPage.Back)

    def _go_forward(self):
        self.page.triggerAction(QWebPage.Forward)

    def _refresh(self):
        self.page.triggerAction(QWebPage.Reload)

    def _stop(self):
        self.page.triggerAction(QWebPage.Stop)

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
        global page, url_input
        #print(page.mainFrame().baseUrl().toString())
        url_input.setText(QString(page.mainFrame().baseUrl().toString()))
        url_input.clearFocus()
        status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        status, ok = status.toInt()
        self.table.update([url, str(status), content_type])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    grid = QGridLayout()
    browser = QWebView()
    url_input = UrlInput(browser)
    requests_table = RequestsTable()

    manager = Manager(requests_table)
    page = QWebPage()
    page.setNetworkAccessManager(manager)
    browser.setPage(page)

    js_eval = JavaScriptEvaluator(page)
    commands = ActionBox(page)

    grid.addWidget(url_input, 1, 0)
    grid.addWidget(commands, 2, 0)
    grid.addWidget(browser, 3, 0)
    grid.addWidget(requests_table, 4, 0)
    grid.addWidget(js_eval, 5, 0)

    main_frame = QWidget()
    main_frame.setLayout(grid)
    window = QMainWindow()
    window.setWindowTitle('Browser')
    window.setCentralWidget(main_frame)
    window.showMaximized()
    
    sys.exit(app.exec_())
