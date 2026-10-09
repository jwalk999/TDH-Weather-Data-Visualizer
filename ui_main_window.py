# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QLabel, QLayout, QMainWindow, QMenu,
    QMenuBar, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(863, 599)
        MainWindow.setMouseTracking(False)
        MainWindow.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(u"hot-temperature.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        MainWindow.setDockOptions(QMainWindow.DockOption.AllowTabbedDocks|QMainWindow.DockOption.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.action_Set_Location = QAction(MainWindow)
        self.action_Set_Location.setObjectName(u"action_Set_Location")
        self.action_Check_Status = QAction(MainWindow)
        self.action_Check_Status.setObjectName(u"action_Check_Status")
        self.action_Reload_Data = QAction(MainWindow)
        self.action_Reload_Data.setObjectName(u"action_Reload_Data")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionReadme = QAction(MainWindow)
        self.actionReadme.setObjectName(u"actionReadme")
        self.action_Minimize = QAction(MainWindow)
        self.action_Minimize.setObjectName(u"action_Minimize")
        self.actionSet_Location = QAction(MainWindow)
        self.actionSet_Location.setObjectName(u"actionSet_Location")
        self.action_Check_Connection = QAction(MainWindow)
        self.action_Check_Connection.setObjectName(u"action_Check_Connection")
        self.action_Units = QAction(MainWindow)
        self.action_Units.setObjectName(u"action_Units")
        self.action_Units.setCheckable(True)
        self.action_Units.setChecked(True)
        self.action_Localization = QAction(MainWindow)
        self.action_Localization.setObjectName(u"action_Localization")
        self.action_Themes = QAction(MainWindow)
        self.action_Themes.setObjectName(u"action_Themes")
        self.actionGithub = QAction(MainWindow)
        self.actionGithub.setObjectName(u"actionGithub")
        self.action_Quit = QAction(MainWindow)
        self.action_Quit.setObjectName(u"action_Quit")
        self.actionCelcius = QAction(MainWindow)
        self.actionCelcius.setObjectName(u"actionCelcius")
        self.actionCelcius.setCheckable(True)
        self.actionShow_Forecast = QAction(MainWindow)
        self.actionShow_Forecast.setObjectName(u"actionShow_Forecast")
        self.actionShow_Graph = QAction(MainWindow)
        self.actionShow_Graph.setObjectName(u"actionShow_Graph")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAutoFillBackground(False)
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 829, 867))
        self.scrollAreaWidgetContents.setMinimumSize(QSize(800, 0))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.mainBox = QGroupBox(self.scrollAreaWidgetContents)
        self.mainBox.setObjectName(u"mainBox")
        self.mainBox.setMaximumSize(QSize(16777215, 16777215))
        self.mainBox.setBaseSize(QSize(0, 0))
        self.mainBox.setAutoFillBackground(True)
        self.mainBox.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.mainBox.setFlat(True)
        self.gridLayout_3 = QGridLayout(self.mainBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(9, 3, 5, 3)
        self.quipLabel = QLabel(self.mainBox)
        self.quipLabel.setObjectName(u"quipLabel")
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(14)
        self.quipLabel.setFont(font)

        self.gridLayout_3.addWidget(self.quipLabel, 0, 1, 2, 1)

        self.bigtempLabel = QLabel(self.mainBox)
        self.bigtempLabel.setObjectName(u"bigtempLabel")
        self.bigtempLabel.setFont(font)

        self.gridLayout_3.addWidget(self.bigtempLabel, 3, 0, 1, 1)

        self.sunriseLabel = QLabel(self.mainBox)
        self.sunriseLabel.setObjectName(u"sunriseLabel")
        font1 = QFont()
        font1.setFamilies([u"Calibri"])
        font1.setPointSize(12)
        self.sunriseLabel.setFont(font1)

        self.gridLayout_3.addWidget(self.sunriseLabel, 6, 0, 1, 1)

        self.locationLabel = QLabel(self.mainBox)
        self.locationLabel.setObjectName(u"locationLabel")
        self.locationLabel.setMinimumSize(QSize(0, 0))
        font2 = QFont()
        font2.setFamilies([u"Calibri"])
        font2.setPointSize(18)
        font2.setBold(True)
        self.locationLabel.setFont(font2)

        self.gridLayout_3.addWidget(self.locationLabel, 0, 0, 2, 1)

        self.bigprecLabel = QLabel(self.mainBox)
        self.bigprecLabel.setObjectName(u"bigprecLabel")
        self.bigprecLabel.setFont(font)

        self.gridLayout_3.addWidget(self.bigprecLabel, 4, 0, 1, 1)

        self.sunsetLabel = QLabel(self.mainBox)
        self.sunsetLabel.setObjectName(u"sunsetLabel")
        self.sunsetLabel.setFont(font1)

        self.gridLayout_3.addWidget(self.sunsetLabel, 6, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.mainBox)

        self.forecastBox = QGroupBox(self.scrollAreaWidgetContents)
        self.forecastBox.setObjectName(u"forecastBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.forecastBox.sizePolicy().hasHeightForWidth())
        self.forecastBox.setSizePolicy(sizePolicy)
        self.forecastBox.setMinimumSize(QSize(800, 0))
        self.forecastBox.setBaseSize(QSize(0, 0))
        self.forecastBox.setAutoFillBackground(True)
        self.forecastBox.setFlat(True)
        self.gridLayout_2 = QGridLayout(self.forecastBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(9, -1, 5, -1)
        self.tempsLabel = QLabel(self.forecastBox)
        self.tempsLabel.setObjectName(u"tempsLabel")
        self.tempsLabel.setFont(font1)

        self.gridLayout_2.addWidget(self.tempsLabel, 0, 0, 1, 7)

        self.precipFrame7 = QFrame(self.forecastBox)
        self.precipFrame7.setObjectName(u"precipFrame7")
        self.precipFrame7.setMinimumSize(QSize(0, 140))
        self.precipFrame7.setMaximumSize(QSize(110, 16777215))
        self.precipFrame7.setFont(font1)
        self.precipFrame7.setFrameShape(QFrame.Shape.StyledPanel)
        self.precipFrame7.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.precipFrame7, 4, 6, 1, 1)

        self.tempFrame4 = QFrame(self.forecastBox)
        self.tempFrame4.setObjectName(u"tempFrame4")
        self.tempFrame4.setMinimumSize(QSize(0, 140))
        self.tempFrame4.setMaximumSize(QSize(110, 16777215))
        self.tempFrame4.setFont(font1)
        self.tempFrame4.setFrameShape(QFrame.Shape.StyledPanel)
        self.tempFrame4.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.tempFrame4, 1, 3, 1, 1)

        self.tempFrame5 = QFrame(self.forecastBox)
        self.tempFrame5.setObjectName(u"tempFrame5")
        self.tempFrame5.setMinimumSize(QSize(0, 140))
        self.tempFrame5.setMaximumSize(QSize(110, 16777215))
        self.tempFrame5.setFont(font1)
        self.tempFrame5.setFrameShape(QFrame.Shape.StyledPanel)
        self.tempFrame5.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.tempFrame5, 1, 4, 1, 1)

        self.tempFrame3 = QFrame(self.forecastBox)
        self.tempFrame3.setObjectName(u"tempFrame3")
        self.tempFrame3.setMinimumSize(QSize(0, 140))
        self.tempFrame3.setMaximumSize(QSize(110, 16777215))
        self.tempFrame3.setFont(font1)
        self.tempFrame3.setFrameShape(QFrame.Shape.StyledPanel)
        self.tempFrame3.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.tempFrame3, 1, 2, 1, 1)

        self.tempFrame1 = QFrame(self.forecastBox)
        self.tempFrame1.setObjectName(u"tempFrame1")
        self.tempFrame1.setMinimumSize(QSize(0, 140))
        self.tempFrame1.setMaximumSize(QSize(110, 16777215))
        self.tempFrame1.setFont(font1)
        self.tempFrame1.setFrameShape(QFrame.Shape.StyledPanel)
        self.tempFrame1.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.tempFrame1, 1, 0, 1, 1)

        self.precipFrame1 = QFrame(self.forecastBox)
        self.precipFrame1.setObjectName(u"precipFrame1")
        self.precipFrame1.setMinimumSize(QSize(0, 140))
        self.precipFrame1.setMaximumSize(QSize(110, 16777215))
        self.precipFrame1.setFont(font1)
        self.precipFrame1.setFrameShape(QFrame.Shape.StyledPanel)
        self.precipFrame1.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.precipFrame1, 4, 0, 1, 1)

        self.tempFrame6 = QFrame(self.forecastBox)
        self.tempFrame6.setObjectName(u"tempFrame6")
        self.tempFrame6.setMinimumSize(QSize(0, 140))
        self.tempFrame6.setMaximumSize(QSize(110, 16777215))
        self.tempFrame6.setFont(font1)
        self.tempFrame6.setFrameShape(QFrame.Shape.StyledPanel)
        self.tempFrame6.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.tempFrame6, 1, 5, 1, 1)

        self.precipFrame4 = QFrame(self.forecastBox)
        self.precipFrame4.setObjectName(u"precipFrame4")
        self.precipFrame4.setMinimumSize(QSize(0, 140))
        self.precipFrame4.setMaximumSize(QSize(110, 16777215))
        self.precipFrame4.setFont(font1)
        self.precipFrame4.setFrameShape(QFrame.Shape.StyledPanel)
        self.precipFrame4.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.precipFrame4, 4, 3, 1, 1)

        self.precipFrame3 = QFrame(self.forecastBox)
        self.precipFrame3.setObjectName(u"precipFrame3")
        self.precipFrame3.setMinimumSize(QSize(0, 140))
        self.precipFrame3.setMaximumSize(QSize(110, 16777215))
        self.precipFrame3.setFont(font1)
        self.precipFrame3.setFrameShape(QFrame.Shape.StyledPanel)
        self.precipFrame3.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.precipFrame3, 4, 2, 1, 1)

        self.precipFrame2 = QFrame(self.forecastBox)
        self.precipFrame2.setObjectName(u"precipFrame2")
        self.precipFrame2.setMinimumSize(QSize(0, 140))
        self.precipFrame2.setMaximumSize(QSize(110, 16777215))
        self.precipFrame2.setFont(font1)
        self.precipFrame2.setFrameShape(QFrame.Shape.StyledPanel)
        self.precipFrame2.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.precipFrame2, 4, 1, 1, 1)

        self.line_2 = QFrame(self.forecastBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_2, 6, 0, 1, 7)

        self.tempFrame7 = QFrame(self.forecastBox)
        self.tempFrame7.setObjectName(u"tempFrame7")
        self.tempFrame7.setMinimumSize(QSize(0, 140))
        self.tempFrame7.setMaximumSize(QSize(110, 16777215))
        self.tempFrame7.setFont(font1)
        self.tempFrame7.setFrameShape(QFrame.Shape.StyledPanel)
        self.tempFrame7.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.tempFrame7, 1, 6, 1, 1)

        self.precipFrame6 = QFrame(self.forecastBox)
        self.precipFrame6.setObjectName(u"precipFrame6")
        self.precipFrame6.setMinimumSize(QSize(0, 140))
        self.precipFrame6.setMaximumSize(QSize(110, 16777215))
        self.precipFrame6.setFont(font1)
        self.precipFrame6.setFrameShape(QFrame.Shape.StyledPanel)
        self.precipFrame6.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.precipFrame6, 4, 5, 1, 1)

        self.precipsLabel = QLabel(self.forecastBox)
        self.precipsLabel.setObjectName(u"precipsLabel")
        self.precipsLabel.setFont(font1)

        self.gridLayout_2.addWidget(self.precipsLabel, 3, 0, 1, 7)

        self.precipFrame5 = QFrame(self.forecastBox)
        self.precipFrame5.setObjectName(u"precipFrame5")
        self.precipFrame5.setMinimumSize(QSize(0, 140))
        self.precipFrame5.setMaximumSize(QSize(110, 16777215))
        self.precipFrame5.setFont(font1)
        self.precipFrame5.setFrameShape(QFrame.Shape.StyledPanel)
        self.precipFrame5.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.precipFrame5, 4, 4, 1, 1)

        self.tempFrame2 = QFrame(self.forecastBox)
        self.tempFrame2.setObjectName(u"tempFrame2")
        self.tempFrame2.setMinimumSize(QSize(0, 140))
        self.tempFrame2.setMaximumSize(QSize(110, 16777215))
        self.tempFrame2.setFont(font1)
        self.tempFrame2.setFrameShape(QFrame.Shape.StyledPanel)
        self.tempFrame2.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.tempFrame2, 1, 1, 1, 1)

        self.tempPrecipSpacer = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.tempPrecipSpacer, 2, 0, 1, 7)

        self.precipLineSpacer = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.precipLineSpacer, 5, 0, 1, 7)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setColumnStretch(4, 1)
        self.gridLayout_2.setColumnStretch(5, 1)
        self.gridLayout_2.setColumnStretch(6, 1)

        self.verticalLayout_2.addWidget(self.forecastBox)

        self.plotArea = QWidget(self.scrollAreaWidgetContents)
        self.plotArea.setObjectName(u"plotArea")
        self.plotArea.setMinimumSize(QSize(0, 300))
        self.plotArea.setAutoFillBackground(True)
        self.verticalLayout = QVBoxLayout(self.plotArea)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        self.verticalLayout_2.addWidget(self.plotArea)

        self.verticalLayout_2.setStretch(2, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 863, 33))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_View = QMenu(self.menubar)
        self.menu_View.setObjectName(u"menu_View")
        self.menu_Settings = QMenu(self.menubar)
        self.menu_Settings.setObjectName(u"menu_Settings")
        self.menu_Help = QMenu(self.menubar)
        self.menu_Help.setObjectName(u"menu_Help")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_Settings.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menu_file.addAction(self.action_Reload_Data)
        self.menu_file.addAction(self.actionSave)
        self.menu_file.addAction(self.action_Check_Connection)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_Quit)
        self.menu_View.addAction(self.action_Units)
        self.menu_View.addAction(self.actionCelcius)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.actionShow_Forecast)
        self.menu_View.addAction(self.actionShow_Graph)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.action_Localization)
        self.menu_View.addAction(self.action_Themes)
        self.menu_Settings.addAction(self.actionSet_Location)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionGithub)
        self.menu_Help.addAction(self.actionReadme)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Too Damn Hot!", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save Graphs", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_Set_Location.setText(QCoreApplication.translate("MainWindow", u"&Set Location", None))
        self.action_Check_Status.setText(QCoreApplication.translate("MainWindow", u"&Check Status", None))
        self.action_Reload_Data.setText(QCoreApplication.translate("MainWindow", u"&Refresh", None))
#if QT_CONFIG(shortcut)
        self.action_Reload_Data.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About Too Damn Hot!", None))
        self.actionReadme.setText(QCoreApplication.translate("MainWindow", u"&Readme...", None))
        self.action_Minimize.setText(QCoreApplication.translate("MainWindow", u"&Minimize", None))
        self.actionSet_Location.setText(QCoreApplication.translate("MainWindow", u"Set &Location", None))
        self.action_Check_Connection.setText(QCoreApplication.translate("MainWindow", u"&Check Connection", None))
        self.action_Units.setText(QCoreApplication.translate("MainWindow", u"Fahrenheit", None))
        self.action_Localization.setText(QCoreApplication.translate("MainWindow", u"&Localization", None))
        self.action_Themes.setText(QCoreApplication.translate("MainWindow", u"&Themes", None))
        self.actionGithub.setText(QCoreApplication.translate("MainWindow", u"Github...", None))
#if QT_CONFIG(tooltip)
        self.actionGithub.setToolTip(QCoreApplication.translate("MainWindow", u"https://github.com/jwalk999/TDH-Weather-Data-Visualizer", None))
#endif // QT_CONFIG(tooltip)
        self.action_Quit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
#if QT_CONFIG(shortcut)
        self.action_Quit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionCelcius.setText(QCoreApplication.translate("MainWindow", u"Celsius", None))
        self.actionShow_Forecast.setText(QCoreApplication.translate("MainWindow", u"Show Forecast", None))
        self.actionShow_Graph.setText(QCoreApplication.translate("MainWindow", u"Show Graph", None))
        self.mainBox.setTitle("")
        self.quipLabel.setText(QCoreApplication.translate("MainWindow", u"QUIPS", None))
        self.bigtempLabel.setText(QCoreApplication.translate("MainWindow", u"big temp", None))
        self.sunriseLabel.setText(QCoreApplication.translate("MainWindow", u"sunrise", None))
        self.locationLabel.setText(QCoreApplication.translate("MainWindow", u"location", None))
        self.bigprecLabel.setText(QCoreApplication.translate("MainWindow", u"weather cond", None))
        self.sunsetLabel.setText(QCoreApplication.translate("MainWindow", u"sunset", None))
        self.forecastBox.setTitle("")
        self.tempsLabel.setText(QCoreApplication.translate("MainWindow", u"Temps Label", None))
        self.precipsLabel.setText(QCoreApplication.translate("MainWindow", u"Precip Label", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_View.setTitle(QCoreApplication.translate("MainWindow", u"&View", None))
        self.menu_Settings.setTitle(QCoreApplication.translate("MainWindow", u"&Settings", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
    # retranslateUi

