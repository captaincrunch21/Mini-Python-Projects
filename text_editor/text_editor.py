# binpress tutorial

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)
        self.filename = ""
        self.initUI()

    def initToolbar(self):
        self.NewAction = QtGui.QAction(QtGui.QIcon("icons/new.png"),"New",self)
        self.NewAction.setStatusTip("Create a new document.")
        self.NewAction.setShortcut("Ctrl+N")
        self.NewAction.triggered.connect(self.new)

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
        self.CutAction.triggered.connect(self.text.cut)

        self.CopyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
        self.CopyAction.setStatusTip("Copy text to clipboard")
        self.CopyAction.setShortcut("Ctrl+C")
        self.CopyAction.triggered.connect(self.text.copy)

        self.PasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste from clipboard",self)
        self.PasteAction.setStatusTip("Paste text from clipboard")
        self.PasteAction.setShortcut("Ctrl+V")
        self.PasteAction.triggered.connect(self.text.paste)

        self.UndoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
        self.UndoAction.setStatusTip("Undo last action")
        self.UndoAction.setShortcut("Ctrl+Z")
        self.UndoAction.triggered.connect(self.text.undo)

        self.RedoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        self.RedoAction.setStatusTip("Redo last undone thing")
        self.RedoAction.setShortcut("Ctrl+Y")
        self.RedoAction.triggered.connect(self.text.redo)

        self.fontAction = QtGui.QAction(QtGui.QIcon("icons/font.png"), "Font Options", self)
        self.fontAction.triggered.connect(self.font_change)
        self.fontAction.setStatusTip("Change Font Style")
        self.fontAction.setShortcut("Ctrl+F")

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


        self.toolbar.addAction(self.NewAction)
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

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.fontAction)
        self.toolbar.addAction(self.bgcolorAction)

        self.combo_box = QtGui.QComboBox(self)
        self.comboAction = self.toolbar.addWidget(self.combo_box)
        self.comboAction.setStatusTip("Change Style")
        self.combo_box.addItem('gtk+')
        self.combo_box.addItem("motif")
        self.combo_box.addItem("Windows")
        self.combo_box.addItem("cde")
        self.combo_box.addItem("Plastique")
        self.combo_box.addItem("Cleanlooks")
        self.combo_box.activated[str].connect(self.change_style)
        #self.combo_box.move(600, 10)

        self.toolbar.addSeparator()
        self.toolbar.addAction(BulletAction)
        self.toolbar.addAction(NumberedAction)

    def initFormatbar(self):
      self.formatbar = self.addToolBar("Format")


    def initMenubar(self):
      menubar = self.menuBar()

      file = menubar.addMenu("File")
      edit = menubar.addMenu("Edit")
      format_menu = menubar.addMenu('Format')

      file.addAction(self.NewAction)
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
      
      format_menu.addAction(self.fontAction)

    def initUI(self):
        self.text = QtGui.QTextEdit(self)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        # Setting tab to 4 spaces
        self.text.setTabStopWidth(33)

        self.setCentralWidget(self.text)

        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays the line and column number
        self.text.cursorPositionChanged.connect(self.cursorPosition)

        self.setWindowTitle("Writer")

        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

    def new(self):
        new_window = Main(self)
        new_window.showMaximized()

    def open(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File')

        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())

    def save(self):
        self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')

        with open(self.filename,"wt") as file:
            file.write(self.text.toPlainText())


    def preview(self):
        preview = QtGui.QPrintPreviewDialog()
        preview.paintRequested.connect(lambda p: self.text.print_(p))
        preview.exec_()

    def printer(self):
        dialog = QtGui.QPrintDialog()

        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print_(dialog.printer())


    def cursorPosition(self):
        cursor = self.text.textCursor()

        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))


    def font_change(self):
        font, valid = QtGui.QFontDialog.getFont()

        if valid:
            self.text.setFont(font)
        else:
            pass


    def change_bgcolor(self):
        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            self.text.setStyleSheet("QWidget { background-color : %s }" % color.name())
        else:
            self.text.setStyleSheet("QWidget { background-color : #ffffff }")

    def bulletList(self):
        cursor = self.text.textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):
        cursor = self.text.textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

    def change_style(self, text):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    window = Main()
    window.showMaximized()
    
    sys.exit(app.exec_())
