import sys, re
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, pyqtSlot

class Find(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.last_idx = 0
        self.initUI()

    def initUI(self):
        Label1 = QtGui.QLabel("Find :")
        Label2 = QtGui.QLabel("Replace :")

        FindButton = QtGui.QPushButton("Find", self)
        FindButton.clicked.connect(self.find)

        ReplaceButton = QtGui.QPushButton("Replace", self)
        ReplaceButton.clicked.connect(self.replace)

        ReplaceAllButton = QtGui.QPushButton("Replace All", self)
        ReplaceAllButton.clicked.connect(self.replace_all)

        self.FindField = QtGui.QLineEdit(self)

        self.ReplaceField = QtGui.QLineEdit(self)

        layout = QtGui.QGridLayout()

        layout.addWidget(Label1, 1, 0)
        layout.addWidget(self.FindField, 1, 1, 1, 4)
        layout.addWidget(FindButton, 2, 1)
        layout.addWidget(Label2, 3, 0)
        layout.addWidget(self.ReplaceField, 3, 1, 1, 4)
        layout.addWidget(ReplaceButton, 4, 1)
        layout.addWidget(ReplaceAllButton, 4, 2)

        self.setGeometry(300, 300, 360, 250)
        self.setWindowTitle("Find & Replace")
        self.setLayout(layout)

    def find(self):
        text = str(self.parent.textarea.toPlainText())
        query = str(self.FindField.text())

        self.last_idx = text.find(query, self.last_idx + 1)
        if(self.last_idx >= 0):
            end = self.last_idx + len(query)
            self.move_cursor(self.last_idx, end)
        else:
            self.last_idx = 0
            self.parent.textarea.moveCursor(QtGui.QTextCursor.End)

        '''
        pattern = re.compile("(?:\A|\s+)"+query+"(?=\Z|\s+)")
        match = pattern.search(text, self.last_idx + 1)

        if(match):
            self.last_idx = match.start()
            self.move_cursor(self.last_idx, match.end())
        else:
            self.last_idx = 0
            self.parent.textarea.moveCursor(QtGui.QTextCursor.End)
        '''

    def replace(self):
        cursor = self.parent.textarea.textCursor()
        if(cursor.hasSelection()):
            cursor.insertText(self.ReplaceField.text())
            self.parent.textarea.setTextCursor(cursor)

    def replace_all(self):
        self.last_idx = 0
        self.find()

        while(self.last_idx):
            self.replace()
            self.find()

    def move_cursor(self, start, end):
        cursor = self.parent.textarea.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, end - start)
        self.parent.textarea.setTextCursor(cursor)

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)
        self.filename = ""
        self.initUI()

    def initToolbar(self):
        self.NewTabAction = QtGui.QAction(QtGui.QIcon("icons/new.png"), "New File", self)
        self.NewTabAction.setStatusTip("Create a new document")
        self.NewTabAction.setShortcut("Ctrl+N")
        self.NewTabAction.triggered.connect(self.new_tab)

        self.OpenAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open file",self)
        self.OpenAction.setStatusTip("Open existing document")
        self.OpenAction.setShortcut("Ctrl+O")
        self.OpenAction.triggered.connect(self.open)

        self.SaveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
        self.SaveAction.setStatusTip("Save document")
        self.SaveAction.setShortcut("Ctrl+S")
        self.SaveAction.triggered.connect(self.save)

        self.PrintAction = QtGui.QAction(QtGui.QIcon("icons/print.png"),"Print document",self)
        self.PrintAction.setStatusTip("Print document")
        self.PrintAction.setShortcut("Ctrl+P")
        self.PrintAction.triggered.connect(self.printer)

        self.PreviewAction = QtGui.QAction(QtGui.QIcon("icons/preview.png"),"Page view",self)
        self.PreviewAction.setStatusTip("Preview page before printing")
        self.PreviewAction.setShortcut("Ctrl+Shift+P")
        self.PreviewAction.triggered.connect(self.preview)

        self.exitAction = QtGui.QAction(QtGui.QIcon("icons/quit.png"), "Exit", self)
        self.exitAction.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.exitAction.setStatusTip("Exit")
        self.exitAction.setShortcut("Ctrl+Q")

        self.CutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"),"Cut to clipboard",self)
        self.CutAction.setStatusTip("Delete and copy text to clipboard")
        self.CutAction.setShortcut("Ctrl+X")
        self.CutAction.triggered.connect(self.cut)

        self.CopyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
        self.CopyAction.setStatusTip("Copy text to clipboard")
        self.CopyAction.setShortcut("Ctrl+C")
        self.CopyAction.triggered.connect(self.copy)

        self.PasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste from clipboard",self)
        self.PasteAction.setStatusTip("Paste text from clipboard")
        self.PasteAction.setShortcut("Ctrl+V")
        self.PasteAction.triggered.connect(self.paste)

        self.UndoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
        self.UndoAction.setStatusTip("Undo last action")
        self.UndoAction.setShortcut("Ctrl+Z")
        self.UndoAction.triggered.connect(self.undo)

        self.RedoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        self.RedoAction.setStatusTip("Redo last undone thing")
        self.RedoAction.setShortcut("Ctrl+Y")
        self.RedoAction.triggered.connect(self.redo)

        self.fontAction = QtGui.QAction(QtGui.QIcon("icons/font.png"), "Font Options", self)
        self.fontAction.triggered.connect(self.font_change)
        self.fontAction.setStatusTip("Change Font Style")
        self.fontAction.setShortcut("Ctrl+T")

        self.FindAction = QtGui.QAction(QtGui.QIcon("icons/find.png"), "Find/Replace", self)
        self.FindAction.triggered.connect(Find(self).show)
        self.FindAction.setStatusTip("Find or replace words/phrases in the file")
        self.FindAction.setShortcut("Ctrl+F")

        BulletAction = QtGui.QAction(QtGui.QIcon("icons/bullet.png"),"Insert bullet List",self)
        BulletAction.setStatusTip("Insert bulleted list")
        BulletAction.setShortcut("Ctrl+Shift+B")
        BulletAction.triggered.connect(self.bulletList)

        NumberedAction = QtGui.QAction(QtGui.QIcon("icons/number.png"),"Insert numbered List",self)
        NumberedAction.setStatusTip("Insert numbered list")
        NumberedAction.setShortcut("Ctrl+Shift+L")
        NumberedAction.triggered.connect(self.numberList)

        self.bgcolorAction = QtGui.QAction(QtGui.QIcon("icons/bg-color.png"), "Change Bg Color", self)
        self.bgcolorAction.setStatusTip("Change Background Color")
        self.bgcolorAction.triggered.connect(self.change_bgcolor)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.OpenAction)
        self.toolbar.addAction(self.SaveAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.PrintAction)
        self.toolbar.addAction(self.PreviewAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.CutAction)
        self.toolbar.addAction(self.CopyAction)
        self.toolbar.addAction(self.PasteAction)
        self.toolbar.addAction(self.UndoAction)
        self.toolbar.addAction(self.RedoAction)
        self.toolbar.addAction(self.FindAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.fontAction)
        self.toolbar.addAction(self.bgcolorAction)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("gtk+"))
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))

        self.toolbar.addSeparator()
        self.toolbar.addAction(BulletAction)
        self.toolbar.addAction(NumberedAction)

    def cut(self):
        self.textarea = self.text_areas[self.central_widget.currentIndex()]
        self.textarea.cut()

    def copy(self):
        self.textarea = self.text_areas[self.central_widget.currentIndex()]
        self.textarea.copy()

    def paste(self):
        self.textarea = self.text_areas[self.central_widget.currentIndex()]
        #print(self.central_widget.currentIndex())
        self.textarea.paste()

    def undo(self):
        self.textarea = self.text_areas[self.central_widget.currentIndex()]
        self.textarea.undo()

    def redo(self):
        self.textarea = self.text_areas[self.central_widget.currentIndex()]
        self.textarea.redo()

    def initMenubar(self):
      menubar = self.menuBar()

      file = menubar.addMenu("File")
      edit = menubar.addMenu("Edit")
      format_menu = menubar.addMenu('Format')

      file.addAction(self.NewTabAction)
      file.addAction(self.OpenAction)
      file.addAction(self.SaveAction)
      file.addAction(self.PrintAction)
      file.addAction(self.PreviewAction)
      file.addAction(self.exitAction)

      edit.addAction(self.UndoAction)
      edit.addAction(self.RedoAction)
      edit.addAction(self.CutAction)
      edit.addAction(self.CopyAction)
      edit.addAction(self.PasteAction)
      edit.addAction(self.FindAction)
      
      format_menu.addAction(self.fontAction)

    def init_tab_bar(self):
        self.tabs_action = []
        self.close_tabs_action = []
        self.text_areas = []

    def initUI(self):
        self.close_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.close_tab)
        self.next_tab_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Tab"), self, self.next_tab)
        self.previous_tab_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Shift+Tab"), self, self.previous_tab)
        self.central_widget = QtGui.QTabWidget()
        self.central_widget.setTabsClosable(True)
        self.central_widget.tabCloseRequested.connect(self.remove_tab)
        self.setCentralWidget(self.central_widget)

        self.initToolbar()
        self.initMenubar()
        self.init_tab_bar()

        self.idx = 0
        self.new_tab()

        self.statusbar = self.statusBar()
        self.setWindowTitle("Writer")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

    def new(self):
        new_window = Main(self)
        new_window.showMaximized()

    def show_tab(self, index):
        self.central_widget.setCurrentWidget(self.text_areas[self.central_widget.currentIndex()])
        self.textarea = self.text_areas[self.central_widget.currentIndex()]

    @pyqtSlot()
    def previous_tab(self):
        index = self.central_widget.currentIndex()
        if(index == 0):
            index = self.central_widget.count() - 1
        else:
            index -= 1
        self.central_widget.setCurrentWidget(self.text_areas[index])
        self.textarea = self.text_areas[index] 

    @pyqtSlot()
    def next_tab(self):
        index = self.central_widget.currentIndex()
        if(index + 1 == self.central_widget.count()):
            index = 0
        else:
            index += 1
        self.central_widget.setCurrentWidget(self.text_areas[index])
        self.textarea = self.text_areas[index]

    @pyqtSlot()
    def close_tab(self):
        index = self.central_widget.currentIndex()
        if(len(str(self.text_areas[index].toPlainText()).strip()) == 0):
            self.central_widget.removeTab(index)

            self.tabs_action.remove(self.tabs_action[index])
            self.close_tabs_action.remove(self.close_tabs_action[index])
            self.text_areas.remove(self.text_areas[index])

            if(self.central_widget.count() == 0):
                QtGui.QApplication.quit()

            return

        quit_msg = "Have you saved your work ?\nIf not, are you sure you want to close this tab without saving ?"
        reply = QtGui.QMessageBox.question(self, 'Alert', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            self.central_widget.removeTab(index)
            
            self.tabs_action.remove(self.tabs_action[index])
            self.close_tabs_action.remove(self.close_tabs_action[index])
            self.text_areas.remove(self.text_areas[index])

            if(self.central_widget.count() == 0):
                QtGui.QApplication.quit()
        else:
            pass

    def remove_tab(self, index):
        if(len(str(self.text_areas[index].toPlainText()).strip()) == 0):
            self.central_widget.removeTab(index)

            self.tabs_action.remove(self.tabs_action[index])
            self.close_tabs_action.remove(self.close_tabs_action[index])
            self.text_areas.remove(self.text_areas[index])

            if(self.central_widget.count() == 0):
                QtGui.QApplication.quit()

            return

        quit_msg = "Have you saved your work ?\nIf not, are you sure you want to close this tab without saving ?"
        reply = QtGui.QMessageBox.question(self, 'Alert', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            self.central_widget.removeTab(index)
            
            self.tabs_action.remove(self.tabs_action[index])
            self.close_tabs_action.remove(self.close_tabs_action[index])
            self.text_areas.remove(self.text_areas[index])

            if(self.central_widget.count() == 0):
                QtGui.QApplication.quit()
        else:
            pass
    
    def new_tab(self):
        self.length = len(self.tabs_action)
        self.tabs_action.append(QtGui.QAction("Untitled"+str(self.length), self))

        self.close_tabs_action.append(QtGui.QAction("x", self))
        self.text_areas.append(QtGui.QTextEdit(self))
        # Setting tab to 4 spaces
        self.text_areas[-1].setTabStopWidth(33)

        self.central_widget.addTab(self.text_areas[-1], "Untitled"+str(self.length))
        self.central_widget.setCurrentWidget(self.text_areas[-1])

        index = len(self.tabs_action)-1
        self.idx = index

        self.tabs_action[index].triggered.connect(lambda checked, index=index: self.show_tab(index))
        # If the cursor position changes, call the function that displays the line and column number
        self.text_areas[self.idx].cursorPositionChanged.connect(self.cursorPosition)

    def open(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        self.idx = self.central_widget.currentIndex()
        if self.filename:
            # rt and r are same mode
            with open(self.filename, "rt") as file:
                self.text_areas[self.idx].setText(file.read())

    def save(self):
        self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        # for IO error when the dialog box is closed
        try:
            with open(self.filename, "wt") as file:
                file.write(self.text_areas[self.central_widget.currentIndex()].toPlainText())
        except:
            pass

    def preview(self):
        preview = QtGui.QPrintPreviewDialog()
        preview.paintRequested.connect(lambda p: self.textarea.print_(p))
        preview.exec_()

    def printer(self):
        dialog = QtGui.QPrintDialog()

        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text_areas[self.central_widget.currentIndex()].document().print_(dialog.printer())

    def cursorPosition(self):
        cursor = self.text_areas[self.central_widget.currentIndex()].textCursor()

        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))

    def font_change(self):
        font, valid = QtGui.QFontDialog.getFont()

        if valid:
            self.text_areas[self.central_widget.currentIndex()].setFont(font)
        else:
            pass

    def change_bgcolor(self):
        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            self.text_areas[self.central_widget.currentIndex()].setStyleSheet("QWidget { background-color : %s }" % color.name())
        else:
            self.text_areas[self.central_widget.currentIndex()].setStyleSheet("QWidget { background-color : #ffffff }")

    def bulletList(self):
        cursor = self.text_areas[self.central_widget.currentIndex()].textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):
        cursor = self.text_areas[self.central_widget.currentIndex()].textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit ?"
        reply = QtGui.QMessageBox.question(self, 'Alert', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    window = Main()
    window.showMaximized()
    
    sys.exit(app.exec_())