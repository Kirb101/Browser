import sys
import os
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QStatusBar, QFrame, QWidget, QMessageBox, QAction, QMenuBar

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NuggetWeb is the best title AWETheBird could think of. Anything else like 'AWETheBrowser' is kinda stupid")
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet("background-color: #bfbfbf; color: black;")
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.settings = QWebEngineSettings.globalSettings()
        self.settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        main_layout = QVBoxLayout()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.mousePressEvent = self.mousePressEvent
        self.status_bar.mouseMoveEvent = self.mouseMoveEvent

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        main_layout.addWidget(frame)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL here")
        self.url_bar.returnPressed.connect(self.navigate)
        self.status_bar.addWidget(self.url_bar)

        self.back_button = QPushButton("←")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setFixedSize(25, 25)
        self.status_bar.addWidget(self.back_button)

        self.forward_button = QPushButton("→")
        self.forward_button.clicked.connect(self.go_forward)
        self.forward_button.setFixedSize(25, 25)
        self.status_bar.addWidget(self.forward_button)

        self.refresh_button = QPushButton("")
        self.refresh_button.setStyleSheet("font-family: Segoe Fluent Icons; font-size: 16px; color: black;")
        self.refresh_button.clicked.connect(self.refresh)
        self.refresh_button.setFixedSize(25, 25)
        self.status_bar.addWidget(self.refresh_button)

        self.close_button = QPushButton("")
        self.close_button.setStyleSheet("font-family: Segoe Fluent Icons; font-size: 16px; color: black;")
        self.close_button.setFixedSize(25, 25)
        self.close_button.clicked.connect(self.close)
        self.status_bar.addPermanentWidget(self.close_button)

        self.maximize_button = QPushButton("")
        self.maximize_button.setStyleSheet("font-family: Segoe Fluent Icons; font-size: 16px; color: black;")
        self.maximize_button.setFixedSize(25, 25)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.status_bar.addPermanentWidget(self.maximize_button)

        self.minimize_button = QPushButton("")
        self.minimize_button.setStyleSheet("font-family: Segoe Fluent Icons; font-size: 16px; color: black;")
        self.minimize_button.setFixedSize(25, 25)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.status_bar.addPermanentWidget(self.minimize_button)

        self.web_view = QWebEngineView()
        frame_layout.addWidget(self.web_view)

        self.load_default_homepage()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.create_menu_bar()

        self.show()

    def load_default_homepage(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        homepage_path = os.path.join(current_dir, "Homepage.html")
        self.web_view.load(QUrl.fromLocalFile(homepage_path))

    def navigate(self):
        url = self.url_bar.text()
        if url:
            if not url.startswith("https://"):
                url = "https://" + url
            self.web_view.load(QUrl(url))

    def go_back(self):
        self.web_view.back()

    def go_forward(self):
        self.web_view.forward()

    def refresh(self):
        self.web_view.reload()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if hasattr(self, 'drag_position'):
                self.move(event.globalPos() - self.drag_position)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.menu_bar.show()

    def create_menu_bar(self):
        self.menu_bar = QMenuBar()
        
        # File menu
        file_menu = self.menu_bar.addMenu('File')
        file_menu.addAction('Exit', self.close)

        # Edit menu
        edit_menu = self.menu_bar.addMenu('Edit')
        self.copy_action = QAction('Copy', self)
        self.copy_action.setShortcut('Ctrl+C')
        self.copy_action.triggered.connect(self.copy)
        edit_menu.addAction(self.copy_action)

        self.paste_action = QAction('Paste', self)
        self.paste_action.setShortcut('Ctrl+V')
        self.paste_action.triggered.connect(self.paste)
        edit_menu.addAction(self.paste_action)

        self.dark_mode_action = QAction('Dark mode', self)
        self.dark_mode_action.triggered.connect(self.toggle_light_dark_mode)
        edit_menu.addAction(self.dark_mode_action)

        # French action
        french_action = QAction('French', self)
        french_action.triggered.connect(lambda: self.web_view.load(QUrl('https://en.wikipedia.org/wiki/French_language')))
        self.menu_bar.addAction(french_action)

        # About menu
        about_menu = self.menu_bar.addMenu('About')
        about_nuggetweb_action = QAction('About NuggetWeb', self)
        about_nuggetweb_action.triggered.connect(self.about_nuggetweb)
        about_menu.addAction(about_nuggetweb_action)

        about_awethebird_action = QAction('About AWETheBird', self)
        about_awethebird_action.triggered.connect(self.about_awethebird)
        about_menu.addAction(about_awethebird_action)

        about_menu.addSeparator()

        wip_action = QAction('W.I.P., Version 1.4', self)
        wip_action.setEnabled(False)
        about_menu.addAction(wip_action)

        self.setMenuBar(self.menu_bar)
        self.menu_bar.hide()

    def about_nuggetweb(self):
        print("NuggetWeb is by AWETheBird. What else lol")
        QMessageBox.information(self, "", "NuggetWeb is by AWETheBird. What else lol")

    def about_awethebird(self):
        print("AWETheBird is a developer. pls go to twitch.tv/awethebird. i alr opened youtube to ruin what you were previously doing but you can go back")
        self.web_view.load(QUrl('https://www.youtube.com/@awethebird'))
        QMessageBox.information(self, "", "AWETheBird is a developer. pls go to twitch.tv/awethebird. i alr opened youtube to ruin what you were previously doing but you can go back")

    def toggle_light_dark_mode(self):
        current_style_sheet = self.styleSheet()
        if "background-color: #333;" in current_style_sheet:
            self.setStyleSheet("background-color: #bfbfbf; color: black;")
            icon_color = "black"
            self.dark_mode_action.setText("Dark mode")
        else:
            self.setStyleSheet("background-color: #333; color: white;")
            icon_color = "white"
            self.dark_mode_action.setText("Light mode")
        icons = [self.url_bar, self.back_button, self.forward_button,
                 self.refresh_button, self.close_button, self.maximize_button, self.minimize_button]
        for icon in icons:
            icon.setStyleSheet(f"font-family: Segoe Fluent Icons; font-size: 16px; color: {icon_color};")

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_button.setText("")
        else:
            self.showMaximized()
            self.maximize_button.setText("")

    def copy(self):
        if self.web_view.focusWidget():
            self.web_view.triggerPageAction(QWebEngineView.Copy)

    def paste(self):
        if self.web_view.focusWidget():
            self.web_view.triggerPageAction(QWebEngineView.Paste)

def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
