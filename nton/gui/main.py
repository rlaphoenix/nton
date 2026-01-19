# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QCommandLinkButton, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpinBox, QStackedWidget,
    QStatusBar, QVBoxLayout, QWidget)

from nton.gui.widgets import FileDropper
import nton.gui.resources.icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(420, 547)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(420, 547))
        MainWindow.setMaximumSize(QSize(420, 547))
        icon1 = QIcon()
        icon1.addFile(u":/branding/images/nton.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon1)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        icon2 = QIcon()
        icon2.addFile(u":/menubar/open.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionOpen.setIcon(icon2)
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        icon3 = QIcon()
        icon3.addFile(u":/menubar/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionClose.setIcon(icon3)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        icon4 = QIcon()
        icon4.addFile(u":/menubar/exit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionExit.setIcon(icon4)
        self.actionExit.setMenuRole(QAction.QuitRole)
        self.actionTroubleshooting = QAction(MainWindow)
        self.actionTroubleshooting.setObjectName(u"actionTroubleshooting")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionAbout.setMenuRole(QAction.AboutRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.appPage = QStackedWidget(self.centralwidget)
        self.appPage.setObjectName(u"appPage")
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.verticalLayout_8 = QVBoxLayout(self.page1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.openLabel = QLabel(self.page1)
        self.openLabel.setObjectName(u"openLabel")
        font = QFont()
        font.setFamilies([u"Segoe UI Light"])
        font.setPointSize(16)
        self.openLabel.setFont(font)
        self.openLabel.setStyleSheet(u"border: 3px solid #dcdcdc;\n"
"            border-style: dashed;\n"
"            border-radius: 8px;")
        self.openLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.openLabel)

        self.appPage.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.verticalLayout_2 = QVBoxLayout(self.page2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.a_nameAuthorIconLayout = QHBoxLayout()
        self.a_nameAuthorIconLayout.setObjectName(u"a_nameAuthorIconLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.nameBox = QGroupBox(self.page2)
        self.nameBox.setObjectName(u"nameBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.nameBox.sizePolicy().hasHeightForWidth())
        self.nameBox.setSizePolicy(sizePolicy2)
        self.horizontalLayout_3 = QHBoxLayout(self.nameBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.name = QLineEdit(self.nameBox)
        self.name.setObjectName(u"name")
        self.name.setMaxLength(512)

        self.horizontalLayout_3.addWidget(self.name)


        self.verticalLayout_3.addWidget(self.nameBox)

        self.authorBox = QGroupBox(self.page2)
        self.authorBox.setObjectName(u"authorBox")
        sizePolicy2.setHeightForWidth(self.authorBox.sizePolicy().hasHeightForWidth())
        self.authorBox.setSizePolicy(sizePolicy2)
        self.horizontalLayout_4 = QHBoxLayout(self.authorBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.author = QLineEdit(self.authorBox)
        self.author.setObjectName(u"author")
        self.author.setMaxLength(256)

        self.horizontalLayout_4.addWidget(self.author)


        self.verticalLayout_3.addWidget(self.authorBox)


        self.a_nameAuthorIconLayout.addLayout(self.verticalLayout_3)

        self.icon = QLabel(self.page2)
        self.icon.setObjectName(u"icon")
        self.icon.setMinimumSize(QSize(125, 125))
        self.icon.setMaximumSize(QSize(125, 125))
        self.icon.setFrameShape(QFrame.Box)
        self.icon.setPixmap(QPixmap(u":/branding/images/sad.png"))
        self.icon.setScaledContents(True)

        self.a_nameAuthorIconLayout.addWidget(self.icon)


        self.verticalLayout_2.addLayout(self.a_nameAuthorIconLayout)

        self.b_generalInfoBox = QGroupBox(self.page2)
        self.b_generalInfoBox.setObjectName(u"b_generalInfoBox")
        sizePolicy2.setHeightForWidth(self.b_generalInfoBox.sizePolicy().hasHeightForWidth())
        self.b_generalInfoBox.setSizePolicy(sizePolicy2)
        self.verticalLayout_5 = QVBoxLayout(self.b_generalInfoBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.screenshots = QComboBox(self.b_generalInfoBox)
        self.screenshots.addItem("")
        self.screenshots.addItem("")
        self.screenshots.setObjectName(u"screenshots")

        self.gridLayout_2.addWidget(self.screenshots, 1, 3, 1, 1)

        self.screenshotsLabel = QLabel(self.b_generalInfoBox)
        self.screenshotsLabel.setObjectName(u"screenshotsLabel")

        self.gridLayout_2.addWidget(self.screenshotsLabel, 1, 2, 1, 1)

        self.videoCaptureLabel = QLabel(self.b_generalInfoBox)
        self.videoCaptureLabel.setObjectName(u"videoCaptureLabel")

        self.gridLayout_2.addWidget(self.videoCaptureLabel, 1, 0, 1, 1)

        self.displayVersionLabel = QLabel(self.b_generalInfoBox)
        self.displayVersionLabel.setObjectName(u"displayVersionLabel")

        self.gridLayout_2.addWidget(self.displayVersionLabel, 0, 2, 1, 1)

        self.displayVersion = QLineEdit(self.b_generalInfoBox)
        self.displayVersion.setObjectName(u"displayVersion")
        self.displayVersion.setMaxLength(16)

        self.gridLayout_2.addWidget(self.displayVersion, 0, 3, 1, 1)

        self.versionLabel = QLabel(self.b_generalInfoBox)
        self.versionLabel.setObjectName(u"versionLabel")

        self.gridLayout_2.addWidget(self.versionLabel, 0, 0, 1, 1)

        self.videoCapture = QComboBox(self.b_generalInfoBox)
        self.videoCapture.addItem("")
        self.videoCapture.addItem("")
        self.videoCapture.addItem("")
        self.videoCapture.setObjectName(u"videoCapture")

        self.gridLayout_2.addWidget(self.videoCapture, 1, 1, 1, 1)

        self.version = QSpinBox(self.b_generalInfoBox)
        self.version.setObjectName(u"version")
        self.version.setEnabled(False)
        self.version.setMaximum(999999999)

        self.gridLayout_2.addWidget(self.version, 0, 1, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout_2)


        self.verticalLayout_2.addWidget(self.b_generalInfoBox)

        self.d_titleIdBox = QGroupBox(self.page2)
        self.d_titleIdBox.setObjectName(u"d_titleIdBox")
        sizePolicy2.setHeightForWidth(self.d_titleIdBox.sizePolicy().hasHeightForWidth())
        self.d_titleIdBox.setSizePolicy(sizePolicy2)
        self.verticalLayout_6 = QVBoxLayout(self.d_titleIdBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.titleId = QLineEdit(self.d_titleIdBox)
        self.titleId.setObjectName(u"titleId")
        font1 = QFont()
        font1.setFamilies([u"Courier New"])
        self.titleId.setFont(font1)

        self.horizontalLayout.addWidget(self.titleId)

        self.randomizeIdButton = QPushButton(self.d_titleIdBox)
        self.randomizeIdButton.setObjectName(u"randomizeIdButton")

        self.horizontalLayout.addWidget(self.randomizeIdButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.titleIdWarning = QLabel(self.d_titleIdBox)
        self.titleIdWarning.setObjectName(u"titleIdWarning")
        self.titleIdWarning.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.titleIdWarning)


        self.verticalLayout_2.addWidget(self.d_titleIdBox)

        self.argsBox = QGroupBox(self.page2)
        self.argsBox.setObjectName(u"argsBox")
        self.verticalLayout_4 = QVBoxLayout(self.argsBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.args = QLineEdit(self.argsBox)
        self.args.setObjectName(u"args")

        self.verticalLayout_4.addWidget(self.args)

        self.loadRomButton = QPushButton(self.argsBox)
        self.loadRomButton.setObjectName(u"loadRomButton")

        self.verticalLayout_4.addWidget(self.loadRomButton)


        self.verticalLayout_2.addWidget(self.argsBox)

        self.e_buildLayout = QHBoxLayout()
        self.e_buildLayout.setObjectName(u"e_buildLayout")
        self.buildButton = QCommandLinkButton(self.page2)
        self.buildButton.setObjectName(u"buildButton")
        sizePolicy.setHeightForWidth(self.buildButton.sizePolicy().hasHeightForWidth())
        self.buildButton.setSizePolicy(sizePolicy)
        self.buildButton.setMaximumSize(QSize(182, 41))

        self.e_buildLayout.addWidget(self.buildButton)


        self.verticalLayout_2.addLayout(self.e_buildLayout)

        self.appPage.addWidget(self.page2)

        self.verticalLayout.addWidget(self.appPage)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 420, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        self.statusbar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.screenshotsLabel.setBuddy(self.screenshots)
        self.videoCaptureLabel.setBuddy(self.videoCapture)
        self.displayVersionLabel.setBuddy(self.displayVersion)
        self.versionLabel.setBuddy(self.version)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.name, self.author)
        QWidget.setTabOrder(self.author, self.version)
        QWidget.setTabOrder(self.version, self.displayVersion)
        QWidget.setTabOrder(self.displayVersion, self.videoCapture)
        QWidget.setTabOrder(self.videoCapture, self.screenshots)
        QWidget.setTabOrder(self.screenshots, self.buildButton)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionTroubleshooting)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.appPage.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"NTON v1.0.0", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
#if QT_CONFIG(shortcut)
        self.actionClose.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+F4", None))
#endif // QT_CONFIG(shortcut)
        self.actionTroubleshooting.setText(QCoreApplication.translate("MainWindow", u"Troubleshooting", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.openLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\"\n"
"            font-weight:700;\">Choose an NRO</span> or drag it\n"
"            here.</p></body></html>", None))
        self.nameBox.setTitle(QCoreApplication.translate("MainWindow", u"&Name", None))
        self.name.setText(QCoreApplication.translate("MainWindow", u"nx-hbmenu", None))
        self.authorBox.setTitle(QCoreApplication.translate("MainWindow", u"&Author", None))
        self.author.setText(QCoreApplication.translate("MainWindow", u"switchbrew", None))
        self.icon.setText("")
        self.b_generalInfoBox.setTitle(QCoreApplication.translate("MainWindow", u"General Information", None))
        self.screenshots.setItemText(0, QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.screenshots.setItemText(1, QCoreApplication.translate("MainWindow", u"Disabled", None))

        self.screenshotsLabel.setText(QCoreApplication.translate("MainWindow", u"Screenshots", None))
        self.videoCaptureLabel.setText(QCoreApplication.translate("MainWindow", u"Video Capture", None))
        self.displayVersionLabel.setText(QCoreApplication.translate("MainWindow", u"&Display Version", None))
        self.displayVersion.setText(QCoreApplication.translate("MainWindow", u"3.5.1", None))
        self.versionLabel.setText(QCoreApplication.translate("MainWindow", u"&Version", None))
        self.videoCapture.setItemText(0, QCoreApplication.translate("MainWindow", u"Disabled", None))
        self.videoCapture.setItemText(1, QCoreApplication.translate("MainWindow", u"Manual", None))
        self.videoCapture.setItemText(2, QCoreApplication.translate("MainWindow", u"Enabled", None))

#if QT_CONFIG(tooltip)
        self.version.setToolTip(QCoreApplication.translate("MainWindow", u"hacBrewPack cannot yet specify the Application Version, see\n"
"                 https://github.com/The-4n/hacBrewPack/issues/15", None))
#endif // QT_CONFIG(tooltip)
        self.d_titleIdBox.setTitle(QCoreApplication.translate("MainWindow", u"Title ID", None))
        self.titleId.setInputMask(QCoreApplication.translate("MainWindow", u">BBHHHHHHHHHHHBBB", None))
        self.titleId.setText(QCoreApplication.translate("MainWindow", u"010D6FD3B35CD000", None))
        self.randomizeIdButton.setText(QCoreApplication.translate("MainWindow", u"Randomize", None))
        self.titleIdWarning.setText(QCoreApplication.translate("MainWindow", u"Warning: Setting the Title ID to that of another Title will\n"
"               override it, and in Tinfoil's case, without warning. Overriding a\n"
"               System Title will brick your system!", None))
        self.argsBox.setTitle(QCoreApplication.translate("MainWindow", u"Arguments", None))
        self.args.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Extra parameters used when calling the NRO...", None))
        self.loadRomButton.setText(QCoreApplication.translate("MainWindow", u"Create ROM Forwarder", None))
        self.buildButton.setText(QCoreApplication.translate("MainWindow", u"Build NSP Forwarder", None))
#if QT_CONFIG(shortcut)
        self.buildButton.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Space", None))
#endif // QT_CONFIG(shortcut)
        self.buildButton.setDescription("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

