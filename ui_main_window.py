# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1100, 740)
        MainWindow.setMinimumSize(QSize(900, 600))
        icon = QIcon()
        icon.addFile(u"hot-temperature.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
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
        self.centralLayout = QHBoxLayout(self.centralwidget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setObjectName(u"centralLayout")
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.navList = QListWidget(self.centralwidget)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        self.navList.setObjectName(u"navList")
        self.navList.setMinimumSize(QSize(188, 0))
        self.navList.setMaximumSize(QSize(188, 16777215))
        self.navList.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.navList.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.centralLayout.addWidget(self.navList)

        self.pages = QStackedWidget(self.centralwidget)
        self.pages.setObjectName(u"pages")
        self.nowPage = QWidget()
        self.nowPage.setObjectName(u"nowPage")
        self.nowPageLayout = QVBoxLayout(self.nowPage)
        self.nowPageLayout.setObjectName(u"nowPageLayout")
        self.nowPageLayout.setContentsMargins(0, 0, 0, 0)
        self.nowScroll = QScrollArea(self.nowPage)
        self.nowScroll.setObjectName(u"nowScroll")
        self.nowScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.nowScroll.setWidgetResizable(True)
        self.nowContents = QWidget()
        self.nowContents.setObjectName(u"nowContents")
        self.nowContents.setProperty(u"page", True)
        self.nowLayout = QVBoxLayout(self.nowContents)
        self.nowLayout.setSpacing(14)
        self.nowLayout.setObjectName(u"nowLayout")
        self.nowLayout.setContentsMargins(20, 20, 20, 20)
        self.alertBanner = QFrame(self.nowContents)
        self.alertBanner.setObjectName(u"alertBanner")
        self.alertBanner.setProperty(u"banner", True)
        self.alertBannerLayout = QHBoxLayout(self.alertBanner)
        self.alertBannerLayout.setSpacing(14)
        self.alertBannerLayout.setObjectName(u"alertBannerLayout")
        self.alertBannerLayout.setContentsMargins(14, 10, 14, 10)
        self.alertTitleLabel = QLabel(self.alertBanner)
        self.alertTitleLabel.setObjectName(u"alertTitleLabel")

        self.alertBannerLayout.addWidget(self.alertTitleLabel)

        self.alertDetailLabel = QLabel(self.alertBanner)
        self.alertDetailLabel.setObjectName(u"alertDetailLabel")

        self.alertBannerLayout.addWidget(self.alertDetailLabel)

        self.alertBannerSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.alertBannerLayout.addItem(self.alertBannerSpacer)

        self.alertLinkLabel = QLabel(self.alertBanner)
        self.alertLinkLabel.setObjectName(u"alertLinkLabel")

        self.alertBannerLayout.addWidget(self.alertLinkLabel)


        self.nowLayout.addWidget(self.alertBanner)

        self.mainBox = QFrame(self.nowContents)
        self.mainBox.setObjectName(u"mainBox")
        self.mainBox.setProperty(u"card", True)
        self.heroLayout = QGridLayout(self.mainBox)
        self.heroLayout.setObjectName(u"heroLayout")
        self.heroLayout.setHorizontalSpacing(32)
        self.heroLayout.setVerticalSpacing(4)
        self.heroLayout.setContentsMargins(24, 20, 24, 20)
        self.locationLabel = QLabel(self.mainBox)
        self.locationLabel.setObjectName(u"locationLabel")

        self.heroLayout.addWidget(self.locationLabel, 0, 0, 1, 1)

        self.dateLabel = QLabel(self.mainBox)
        self.dateLabel.setObjectName(u"dateLabel")

        self.heroLayout.addWidget(self.dateLabel, 1, 0, 1, 1)

        self.bigtempLabel = QLabel(self.mainBox)
        self.bigtempLabel.setObjectName(u"bigtempLabel")

        self.heroLayout.addWidget(self.bigtempLabel, 2, 0, 1, 1)

        self.bigprecLabel = QLabel(self.mainBox)
        self.bigprecLabel.setObjectName(u"bigprecLabel")

        self.heroLayout.addWidget(self.bigprecLabel, 3, 0, 1, 1)

        self.hiloLabel = QLabel(self.mainBox)
        self.hiloLabel.setObjectName(u"hiloLabel")

        self.heroLayout.addWidget(self.hiloLabel, 4, 0, 1, 1)

        self.quipKickerLabel = QLabel(self.mainBox)
        self.quipKickerLabel.setObjectName(u"quipKickerLabel")

        self.heroLayout.addWidget(self.quipKickerLabel, 0, 1, 1, 1)

        self.quipLabel = QLabel(self.mainBox)
        self.quipLabel.setObjectName(u"quipLabel")
        self.quipLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.quipLabel.setWordWrap(True)

        self.heroLayout.addWidget(self.quipLabel, 1, 1, 2, 1)

        self.statsLayout = QHBoxLayout()
        self.statsLayout.setSpacing(12)
        self.statsLayout.setObjectName(u"statsLayout")
        self.humidityLabel = QLabel(self.mainBox)
        self.humidityLabel.setObjectName(u"humidityLabel")

        self.statsLayout.addWidget(self.humidityLabel)

        self.windLabel = QLabel(self.mainBox)
        self.windLabel.setObjectName(u"windLabel")

        self.statsLayout.addWidget(self.windLabel)

        self.uvLabel = QLabel(self.mainBox)
        self.uvLabel.setObjectName(u"uvLabel")

        self.statsLayout.addWidget(self.uvLabel)

        self.precipNowLabel = QLabel(self.mainBox)
        self.precipNowLabel.setObjectName(u"precipNowLabel")

        self.statsLayout.addWidget(self.precipNowLabel)


        self.heroLayout.addLayout(self.statsLayout, 3, 1, 1, 1)

        self.sunLayout = QHBoxLayout()
        self.sunLayout.setSpacing(24)
        self.sunLayout.setObjectName(u"sunLayout")
        self.sunriseLabel = QLabel(self.mainBox)
        self.sunriseLabel.setObjectName(u"sunriseLabel")

        self.sunLayout.addWidget(self.sunriseLabel)

        self.sunsetLabel = QLabel(self.mainBox)
        self.sunsetLabel.setObjectName(u"sunsetLabel")

        self.sunLayout.addWidget(self.sunsetLabel)

        self.sunSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.sunLayout.addItem(self.sunSpacer)


        self.heroLayout.addLayout(self.sunLayout, 4, 1, 1, 1)

        self.heroLayout.setColumnStretch(1, 1)

        self.nowLayout.addWidget(self.mainBox)

        self.forecastBox = QFrame(self.nowContents)
        self.forecastBox.setObjectName(u"forecastBox")
        self.forecastLayout = QVBoxLayout(self.forecastBox)
        self.forecastLayout.setSpacing(8)
        self.forecastLayout.setObjectName(u"forecastLayout")
        self.forecastLayout.setContentsMargins(0, 0, 0, 0)
        self.tempsLabel = QLabel(self.forecastBox)
        self.tempsLabel.setObjectName(u"tempsLabel")

        self.forecastLayout.addWidget(self.tempsLabel)

        self.daysLayout = QHBoxLayout()
        self.daysLayout.setSpacing(8)
        self.daysLayout.setObjectName(u"daysLayout")
        self.tempFrame1 = QFrame(self.forecastBox)
        self.tempFrame1.setObjectName(u"tempFrame1")

        self.daysLayout.addWidget(self.tempFrame1)

        self.tempFrame2 = QFrame(self.forecastBox)
        self.tempFrame2.setObjectName(u"tempFrame2")

        self.daysLayout.addWidget(self.tempFrame2)

        self.tempFrame3 = QFrame(self.forecastBox)
        self.tempFrame3.setObjectName(u"tempFrame3")

        self.daysLayout.addWidget(self.tempFrame3)

        self.tempFrame4 = QFrame(self.forecastBox)
        self.tempFrame4.setObjectName(u"tempFrame4")

        self.daysLayout.addWidget(self.tempFrame4)

        self.tempFrame5 = QFrame(self.forecastBox)
        self.tempFrame5.setObjectName(u"tempFrame5")

        self.daysLayout.addWidget(self.tempFrame5)

        self.tempFrame6 = QFrame(self.forecastBox)
        self.tempFrame6.setObjectName(u"tempFrame6")

        self.daysLayout.addWidget(self.tempFrame6)

        self.tempFrame7 = QFrame(self.forecastBox)
        self.tempFrame7.setObjectName(u"tempFrame7")

        self.daysLayout.addWidget(self.tempFrame7)


        self.forecastLayout.addLayout(self.daysLayout)


        self.nowLayout.addWidget(self.forecastBox)

        self.plotArea = QWidget(self.nowContents)
        self.plotArea.setObjectName(u"plotArea")
        self.plotArea.setMinimumSize(QSize(0, 420))
        self.verticalLayout = QVBoxLayout(self.plotArea)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.nowLayout.addWidget(self.plotArea)

        self.nowScroll.setWidget(self.nowContents)

        self.nowPageLayout.addWidget(self.nowScroll)

        self.pages.addWidget(self.nowPage)
        self.hourlyPage = QWidget()
        self.hourlyPage.setObjectName(u"hourlyPage")
        self.hourlyPageLayout = QVBoxLayout(self.hourlyPage)
        self.hourlyPageLayout.setObjectName(u"hourlyPageLayout")
        self.hourlyPageLayout.setContentsMargins(0, 0, 0, 0)
        self.hourlyScroll = QScrollArea(self.hourlyPage)
        self.hourlyScroll.setObjectName(u"hourlyScroll")
        self.hourlyScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.hourlyScroll.setWidgetResizable(True)
        self.hourlyContents = QWidget()
        self.hourlyContents.setObjectName(u"hourlyContents")
        self.hourlyContents.setProperty(u"page", True)
        self.hourlyLayout = QVBoxLayout(self.hourlyContents)
        self.hourlyLayout.setSpacing(4)
        self.hourlyLayout.setObjectName(u"hourlyLayout")
        self.hourlyLayout.setContentsMargins(20, 20, 20, 20)
        self.hourlyTitle = QLabel(self.hourlyContents)
        self.hourlyTitle.setObjectName(u"hourlyTitle")

        self.hourlyLayout.addWidget(self.hourlyTitle)

        self.hourlySubtitle = QLabel(self.hourlyContents)
        self.hourlySubtitle.setObjectName(u"hourlySubtitle")
        self.hourlySubtitle.setWordWrap(True)

        self.hourlyLayout.addWidget(self.hourlySubtitle)

        self.hourlyList = QWidget(self.hourlyContents)
        self.hourlyList.setObjectName(u"hourlyList")
        self.hourlyListLayout = QVBoxLayout(self.hourlyList)
        self.hourlyListLayout.setSpacing(2)
        self.hourlyListLayout.setObjectName(u"hourlyListLayout")
        self.hourlyListLayout.setContentsMargins(0, 10, 0, 0)

        self.hourlyLayout.addWidget(self.hourlyList)

        self.hourlySpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.hourlyLayout.addItem(self.hourlySpacer)

        self.hourlyScroll.setWidget(self.hourlyContents)

        self.hourlyPageLayout.addWidget(self.hourlyScroll)

        self.pages.addWidget(self.hourlyPage)
        self.tenDayPage = QWidget()
        self.tenDayPage.setObjectName(u"tenDayPage")
        self.tenDayPageLayout = QVBoxLayout(self.tenDayPage)
        self.tenDayPageLayout.setObjectName(u"tenDayPageLayout")
        self.tenDayPageLayout.setContentsMargins(0, 0, 0, 0)
        self.tenDayScroll = QScrollArea(self.tenDayPage)
        self.tenDayScroll.setObjectName(u"tenDayScroll")
        self.tenDayScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.tenDayScroll.setWidgetResizable(True)
        self.tenDayContents = QWidget()
        self.tenDayContents.setObjectName(u"tenDayContents")
        self.tenDayContents.setProperty(u"page", True)
        self.tenDayLayout = QVBoxLayout(self.tenDayContents)
        self.tenDayLayout.setSpacing(4)
        self.tenDayLayout.setObjectName(u"tenDayLayout")
        self.tenDayLayout.setContentsMargins(20, 20, 20, 20)
        self.tenDayTitle = QLabel(self.tenDayContents)
        self.tenDayTitle.setObjectName(u"tenDayTitle")

        self.tenDayLayout.addWidget(self.tenDayTitle)

        self.tenDaySubtitle = QLabel(self.tenDayContents)
        self.tenDaySubtitle.setObjectName(u"tenDaySubtitle")
        self.tenDaySubtitle.setWordWrap(True)

        self.tenDayLayout.addWidget(self.tenDaySubtitle)

        self.tenDayList = QWidget(self.tenDayContents)
        self.tenDayList.setObjectName(u"tenDayList")
        self.tenDayListLayout = QVBoxLayout(self.tenDayList)
        self.tenDayListLayout.setSpacing(0)
        self.tenDayListLayout.setObjectName(u"tenDayListLayout")
        self.tenDayListLayout.setContentsMargins(0, 12, 0, 0)

        self.tenDayLayout.addWidget(self.tenDayList)

        self.tenDaySpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.tenDayLayout.addItem(self.tenDaySpacer)

        self.tenDayScroll.setWidget(self.tenDayContents)

        self.tenDayPageLayout.addWidget(self.tenDayScroll)

        self.pages.addWidget(self.tenDayPage)
        self.alertsPage = QWidget()
        self.alertsPage.setObjectName(u"alertsPage")
        self.alertsPageLayout = QVBoxLayout(self.alertsPage)
        self.alertsPageLayout.setObjectName(u"alertsPageLayout")
        self.alertsPageLayout.setContentsMargins(0, 0, 0, 0)
        self.alertsScroll = QScrollArea(self.alertsPage)
        self.alertsScroll.setObjectName(u"alertsScroll")
        self.alertsScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.alertsScroll.setWidgetResizable(True)
        self.alertsContents = QWidget()
        self.alertsContents.setObjectName(u"alertsContents")
        self.alertsContents.setProperty(u"page", True)
        self.alertsLayout = QVBoxLayout(self.alertsContents)
        self.alertsLayout.setSpacing(12)
        self.alertsLayout.setObjectName(u"alertsLayout")
        self.alertsLayout.setContentsMargins(20, 20, 20, 20)
        self.alertsTitle = QLabel(self.alertsContents)
        self.alertsTitle.setObjectName(u"alertsTitle")

        self.alertsLayout.addWidget(self.alertsTitle)

        self.alertsSubtitle = QLabel(self.alertsContents)
        self.alertsSubtitle.setObjectName(u"alertsSubtitle")

        self.alertsLayout.addWidget(self.alertsSubtitle)

        self.alertsList = QWidget(self.alertsContents)
        self.alertsList.setObjectName(u"alertsList")
        self.alertsListLayout = QVBoxLayout(self.alertsList)
        self.alertsListLayout.setSpacing(10)
        self.alertsListLayout.setObjectName(u"alertsListLayout")
        self.alertsListLayout.setContentsMargins(0, 0, 0, 0)

        self.alertsLayout.addWidget(self.alertsList)

        self.alertsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.alertsLayout.addItem(self.alertsSpacer)

        self.alertsScroll.setWidget(self.alertsContents)

        self.alertsPageLayout.addWidget(self.alertsScroll)

        self.pages.addWidget(self.alertsPage)
        self.radarPage = QWidget()
        self.radarPage.setObjectName(u"radarPage")
        self.radarPage.setProperty(u"page", True)
        self.radarLayout = QVBoxLayout(self.radarPage)
        self.radarLayout.setSpacing(8)
        self.radarLayout.setObjectName(u"radarLayout")
        self.radarLayout.setContentsMargins(20, 20, 20, 20)
        self.radarTitle = QLabel(self.radarPage)
        self.radarTitle.setObjectName(u"radarTitle")

        self.radarLayout.addWidget(self.radarTitle)

        self.radarSubtitle = QLabel(self.radarPage)
        self.radarSubtitle.setObjectName(u"radarSubtitle")

        self.radarLayout.addWidget(self.radarSubtitle)

        self.radarHost = QWidget(self.radarPage)
        self.radarHost.setObjectName(u"radarHost")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.radarHost.sizePolicy().hasHeightForWidth())
        self.radarHost.setSizePolicy(sizePolicy)
        self.radarHostLayout = QVBoxLayout(self.radarHost)
        self.radarHostLayout.setObjectName(u"radarHostLayout")
        self.radarHostLayout.setContentsMargins(0, 0, 0, 0)

        self.radarLayout.addWidget(self.radarHost)

        self.pages.addWidget(self.radarPage)
        self.locationsPage = QWidget()
        self.locationsPage.setObjectName(u"locationsPage")
        self.locationsPageLayout = QVBoxLayout(self.locationsPage)
        self.locationsPageLayout.setObjectName(u"locationsPageLayout")
        self.locationsPageLayout.setContentsMargins(0, 0, 0, 0)
        self.locationsScroll = QScrollArea(self.locationsPage)
        self.locationsScroll.setObjectName(u"locationsScroll")
        self.locationsScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.locationsScroll.setWidgetResizable(True)
        self.locationsContents = QWidget()
        self.locationsContents.setObjectName(u"locationsContents")
        self.locationsContents.setProperty(u"page", True)
        self.locationsLayout = QVBoxLayout(self.locationsContents)
        self.locationsLayout.setSpacing(4)
        self.locationsLayout.setObjectName(u"locationsLayout")
        self.locationsLayout.setContentsMargins(20, 20, 20, 20)
        self.locationsHeader = QHBoxLayout()
        self.locationsHeader.setObjectName(u"locationsHeader")
        self.locationsTitle = QLabel(self.locationsContents)
        self.locationsTitle.setObjectName(u"locationsTitle")

        self.locationsHeader.addWidget(self.locationsTitle)

        self.locationsHeaderSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.locationsHeader.addItem(self.locationsHeaderSpacer)

        self.addLocationButton = QPushButton(self.locationsContents)
        self.addLocationButton.setObjectName(u"addLocationButton")
        self.addLocationButton.setProperty(u"primary", True)

        self.locationsHeader.addWidget(self.addLocationButton)


        self.locationsLayout.addLayout(self.locationsHeader)

        self.locationsSubtitle = QLabel(self.locationsContents)
        self.locationsSubtitle.setObjectName(u"locationsSubtitle")

        self.locationsLayout.addWidget(self.locationsSubtitle)

        self.locationsList = QWidget(self.locationsContents)
        self.locationsList.setObjectName(u"locationsList")
        self.locationsListLayout = QVBoxLayout(self.locationsList)
        self.locationsListLayout.setSpacing(0)
        self.locationsListLayout.setObjectName(u"locationsListLayout")
        self.locationsListLayout.setContentsMargins(0, 12, 0, 0)

        self.locationsLayout.addWidget(self.locationsList)

        self.locationsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.locationsLayout.addItem(self.locationsSpacer)

        self.locationsScroll.setWidget(self.locationsContents)

        self.locationsPageLayout.addWidget(self.locationsScroll)

        self.pages.addWidget(self.locationsPage)
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName(u"settingsPage")
        self.settingsPageLayout = QVBoxLayout(self.settingsPage)
        self.settingsPageLayout.setObjectName(u"settingsPageLayout")
        self.settingsPageLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsScroll = QScrollArea(self.settingsPage)
        self.settingsScroll.setObjectName(u"settingsScroll")
        self.settingsScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.settingsScroll.setWidgetResizable(True)
        self.settingsContents = QWidget()
        self.settingsContents.setObjectName(u"settingsContents")
        self.settingsContents.setProperty(u"page", True)
        self.settingsLayout = QVBoxLayout(self.settingsContents)
        self.settingsLayout.setSpacing(14)
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.settingsLayout.setContentsMargins(20, 20, 20, 20)
        self.settingsTitle = QLabel(self.settingsContents)
        self.settingsTitle.setObjectName(u"settingsTitle")

        self.settingsLayout.addWidget(self.settingsTitle)

        self.settingsBox = QFrame(self.settingsContents)
        self.settingsBox.setObjectName(u"settingsBox")
        self.settingsBox.setProperty(u"card", True)
        self.settingsBox.setMaximumSize(QSize(760, 16777215))
        self.settingsForm = QFormLayout(self.settingsBox)
        self.settingsForm.setObjectName(u"settingsForm")
        self.settingsForm.setHorizontalSpacing(24)
        self.settingsForm.setVerticalSpacing(16)
        self.settingsForm.setContentsMargins(20, 18, 20, 18)
        self.unitsCaption = QLabel(self.settingsBox)
        self.unitsCaption.setObjectName(u"unitsCaption")

        self.settingsForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.unitsCaption)

        self.unitsCombo = QComboBox(self.settingsBox)
        self.unitsCombo.addItem("")
        self.unitsCombo.addItem("")
        self.unitsCombo.setObjectName(u"unitsCombo")

        self.settingsForm.setWidget(0, QFormLayout.ItemRole.FieldRole, self.unitsCombo)

        self.themeCaption = QLabel(self.settingsBox)
        self.themeCaption.setObjectName(u"themeCaption")

        self.settingsForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.themeCaption)

        self.themeCombo = QComboBox(self.settingsBox)
        self.themeCombo.setObjectName(u"themeCombo")

        self.settingsForm.setWidget(1, QFormLayout.ItemRole.FieldRole, self.themeCombo)

        self.viewCaption = QLabel(self.settingsBox)
        self.viewCaption.setObjectName(u"viewCaption")

        self.settingsForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.viewCaption)

        self.viewChecks = QHBoxLayout()
        self.viewChecks.setSpacing(20)
        self.viewChecks.setObjectName(u"viewChecks")
        self.showForecastCheck = QCheckBox(self.settingsBox)
        self.showForecastCheck.setObjectName(u"showForecastCheck")
        self.showForecastCheck.setChecked(True)

        self.viewChecks.addWidget(self.showForecastCheck)

        self.showGraphCheck = QCheckBox(self.settingsBox)
        self.showGraphCheck.setObjectName(u"showGraphCheck")
        self.showGraphCheck.setChecked(True)

        self.viewChecks.addWidget(self.showGraphCheck)

        self.viewChecksSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.viewChecks.addItem(self.viewChecksSpacer)


        self.settingsForm.setLayout(2, QFormLayout.ItemRole.FieldRole, self.viewChecks)

        self.heatCaption = QLabel(self.settingsBox)
        self.heatCaption.setObjectName(u"heatCaption")

        self.settingsForm.setWidget(3, QFormLayout.ItemRole.LabelRole, self.heatCaption)

        self.heatThresholdSpin = QSpinBox(self.settingsBox)
        self.heatThresholdSpin.setObjectName(u"heatThresholdSpin")
        self.heatThresholdSpin.setMinimum(80)
        self.heatThresholdSpin.setMaximum(130)
        self.heatThresholdSpin.setValue(105)

        self.settingsForm.setWidget(3, QFormLayout.ItemRole.FieldRole, self.heatThresholdSpin)

        self.locationCaption = QLabel(self.settingsBox)
        self.locationCaption.setObjectName(u"locationCaption")

        self.settingsForm.setWidget(4, QFormLayout.ItemRole.LabelRole, self.locationCaption)

        self.locationRow = QHBoxLayout()
        self.locationRow.setSpacing(12)
        self.locationRow.setObjectName(u"locationRow")
        self.locationValueLabel = QLabel(self.settingsBox)
        self.locationValueLabel.setObjectName(u"locationValueLabel")

        self.locationRow.addWidget(self.locationValueLabel)

        self.changeLocationButton = QPushButton(self.settingsBox)
        self.changeLocationButton.setObjectName(u"changeLocationButton")

        self.locationRow.addWidget(self.changeLocationButton)

        self.locationRowSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.locationRow.addItem(self.locationRowSpacer)


        self.settingsForm.setLayout(4, QFormLayout.ItemRole.FieldRole, self.locationRow)

        self.refreshCaption = QLabel(self.settingsBox)
        self.refreshCaption.setObjectName(u"refreshCaption")

        self.settingsForm.setWidget(5, QFormLayout.ItemRole.LabelRole, self.refreshCaption)

        self.refreshValueLabel = QLabel(self.settingsBox)
        self.refreshValueLabel.setObjectName(u"refreshValueLabel")

        self.settingsForm.setWidget(5, QFormLayout.ItemRole.FieldRole, self.refreshValueLabel)


        self.settingsLayout.addWidget(self.settingsBox)

        self.settingsSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settingsLayout.addItem(self.settingsSpacer)

        self.settingsScroll.setWidget(self.settingsContents)

        self.settingsPageLayout.addWidget(self.settingsScroll)

        self.pages.addWidget(self.settingsPage)

        self.centralLayout.addWidget(self.pages)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1100, 33))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_View = QMenu(self.menubar)
        self.menu_View.setObjectName(u"menu_View")
        self.menu_Settings = QMenu(self.menubar)
        self.menu_Settings.setObjectName(u"menu_Settings")
        self.menu_Help = QMenu(self.menubar)
        self.menu_Help.setObjectName(u"menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

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

        self.pages.setCurrentIndex(0)


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

        __sortingEnabled = self.navList.isSortingEnabled()
        self.navList.setSortingEnabled(False)
        ___qlistwidgetitem = self.navList.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"Now", None))
        ___qlistwidgetitem1 = self.navList.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Hourly", None))
        ___qlistwidgetitem2 = self.navList.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"10-Day", None))
        ___qlistwidgetitem3 = self.navList.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Alerts", None))
        ___qlistwidgetitem4 = self.navList.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Radar", None))
        ___qlistwidgetitem5 = self.navList.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Locations", None))
        ___qlistwidgetitem6 = self.navList.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.navList.setSortingEnabled(__sortingEnabled)

        self.alertTitleLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"strong", None))
        self.alertTitleLabel.setText(QCoreApplication.translate("MainWindow", u"Excessive Heat Warning", None))
        self.alertDetailLabel.setText(QCoreApplication.translate("MainWindow", u"alert detail", None))
        self.alertLinkLabel.setText(QCoreApplication.translate("MainWindow", u"Details \u2192", None))
        self.locationLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"location", None))
        self.locationLabel.setText(QCoreApplication.translate("MainWindow", u"location", None))
        self.dateLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"sub", None))
        self.dateLabel.setText(QCoreApplication.translate("MainWindow", u"date \u00b7 updated", None))
        self.bigtempLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"bigtemp", None))
        self.bigtempLabel.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.bigprecLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"body", None))
        self.bigprecLabel.setText(QCoreApplication.translate("MainWindow", u"weather cond \u00b7 feels like", None))
        self.hiloLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"sub", None))
        self.hiloLabel.setText(QCoreApplication.translate("MainWindow", u"H -- \u00b7 L --", None))
        self.quipKickerLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"kicker", None))
        self.quipKickerLabel.setText(QCoreApplication.translate("MainWindow", u"BUCKET", None))
        self.quipLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"headline", None))
        self.quipLabel.setText(QCoreApplication.translate("MainWindow", u"QUIPS", None))
        self.humidityLabel.setText(QCoreApplication.translate("MainWindow", u"humidity", None))
        self.windLabel.setText(QCoreApplication.translate("MainWindow", u"wind", None))
        self.uvLabel.setText(QCoreApplication.translate("MainWindow", u"uv", None))
        self.precipNowLabel.setText(QCoreApplication.translate("MainWindow", u"precip", None))
        self.sunriseLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"sunrise", None))
        self.sunriseLabel.setText(QCoreApplication.translate("MainWindow", u"sunrise", None))
        self.sunsetLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"sunset", None))
        self.sunsetLabel.setText(QCoreApplication.translate("MainWindow", u"sunset", None))
        self.tempsLabel.setProperty(u"role", QCoreApplication.translate("MainWindow", u"section", None))
        self.tempsLabel.setText(QCoreApplication.translate("MainWindow", u"Next 7 days", None))
        self.hourlyTitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"title", None))
        self.hourlyTitle.setText(QCoreApplication.translate("MainWindow", u"Hour by hour.", None))
        self.hourlySubtitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"subtitle", None))
        self.hourlySubtitle.setText(QCoreApplication.translate("MainWindow", u"The bar is the temperature. The faint line is feels-like. Both are bad.", None))
        self.tenDayTitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"title", None))
        self.tenDayTitle.setText(QCoreApplication.translate("MainWindow", u"Ten days of this.", None))
        self.tenDaySubtitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"subtitle", None))
        self.tenDaySubtitle.setText(QCoreApplication.translate("MainWindow", u"subtitle", None))
        self.alertsTitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"title", None))
        self.alertsTitle.setText(QCoreApplication.translate("MainWindow", u"Alerts", None))
        self.alertsSubtitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"subtitle", None))
        self.alertsSubtitle.setText(QCoreApplication.translate("MainWindow", u"subtitle", None))
        self.radarTitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"title", None))
        self.radarTitle.setText(QCoreApplication.translate("MainWindow", u"Radar", None))
        self.radarSubtitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"subtitle", None))
        self.radarSubtitle.setText(QCoreApplication.translate("MainWindow", u"Radar loop, no API key needed. US: NEXRAD via Iowa Environmental Mesonet. Elsewhere: RainViewer. Map: Esri Gray Canvas.", None))
        self.locationsTitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"title", None))
        self.locationsTitle.setText(QCoreApplication.translate("MainWindow", u"Locations", None))
        self.addLocationButton.setText(QCoreApplication.translate("MainWindow", u"+ Add place", None))
        self.locationsSubtitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"subtitle", None))
        self.locationsSubtitle.setText(QCoreApplication.translate("MainWindow", u"Compare your suffering.", None))
        self.settingsTitle.setProperty(u"role", QCoreApplication.translate("MainWindow", u"title", None))
        self.settingsTitle.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.unitsCaption.setProperty(u"role", QCoreApplication.translate("MainWindow", u"sub", None))
        self.unitsCaption.setText(QCoreApplication.translate("MainWindow", u"Units", None))
        self.unitsCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"Fahrenheit", None))
        self.unitsCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"Celsius", None))

        self.themeCaption.setProperty(u"role", QCoreApplication.translate("MainWindow", u"sub", None))
        self.themeCaption.setText(QCoreApplication.translate("MainWindow", u"Theme", None))
        self.viewCaption.setProperty(u"role", QCoreApplication.translate("MainWindow", u"sub", None))
        self.viewCaption.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.showForecastCheck.setText(QCoreApplication.translate("MainWindow", u"Show Forecast", None))
        self.showGraphCheck.setText(QCoreApplication.translate("MainWindow", u"Show Graph", None))
        self.heatCaption.setProperty(u"role", QCoreApplication.translate("MainWindow", u"sub", None))
        self.heatCaption.setText(QCoreApplication.translate("MainWindow", u"Heat alert at", None))
        self.heatThresholdSpin.setSuffix(QCoreApplication.translate("MainWindow", u"\u00b0F heat index", None))
        self.locationCaption.setProperty(u"role", QCoreApplication.translate("MainWindow", u"sub", None))
        self.locationCaption.setText(QCoreApplication.translate("MainWindow", u"Location", None))
        self.locationValueLabel.setText(QCoreApplication.translate("MainWindow", u"location", None))
        self.changeLocationButton.setText(QCoreApplication.translate("MainWindow", u"Change\u2026", None))
        self.refreshCaption.setProperty(u"role", QCoreApplication.translate("MainWindow", u"sub", None))
        self.refreshCaption.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.refreshValueLabel.setText(QCoreApplication.translate("MainWindow", u"Every hour (matches the cache expiry) \u00b7 F5 to force it", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_View.setTitle(QCoreApplication.translate("MainWindow", u"&View", None))
        self.menu_Settings.setTitle(QCoreApplication.translate("MainWindow", u"&Settings", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
    # retranslateUi

