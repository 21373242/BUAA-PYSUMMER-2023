# coding: utf-8
from typing import List
from PySide6.QtCore import Qt, Signal, QEasingCurve, QUrl, QSize
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget

from qfluentwidgets import NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow, SplashScreen
from qfluentwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface
from .home_page import HomeInterface
from .must_eat_page_holder import BasicInputInterface
from .canting_page import DateTimeInterface
from .dialog_interface import DialogInterface
from .layout_interface import LayoutInterface
from .search_food import IconInterface
from .material_interface import MaterialInterface
from .menu_interface import MenuInterface
from .navigation_view_interface import NavigationViewInterface
from .scroll_interface import ScrollInterface
from .status_info_interface import StatusInfoInterface
from .setting_interface import SettingInterface
from .text_interface import TextInterface
from .view_interface import ViewInterface
from ..common.config import SUPPORT_URL
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource

type(resource)


class MainWindow(FluentWindow):

    def __init__(self, name):
        super().__init__()
        self.initWindow()
        self.user_name = name
        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.iconInterface = IconInterface(self)
        self.basicInputInterface = BasicInputInterface(self)
        self.dateTimeInterface = DateTimeInterface(self)
        self.dialogInterface = DialogInterface(self)
        self.layoutInterface = LayoutInterface(self)
        self.menuInterface = MenuInterface(self)
        self.materialInterface = MaterialInterface(self)
        self.navigationViewInterface = NavigationViewInterface(self)
        self.scrollInterface = ScrollInterface(self)
        self.statusInfoInterface = StatusInfoInterface(self)
        self.settingInterface = SettingInterface(self)
        self.textInterface = TextInterface(self)
        self.viewInterface = ViewInterface(self)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def initLayout(self):
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))
        self.addSubInterface(self.iconInterface, Icon.EMOJI_TAB_SYMBOLS, t.icons)
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.basicInputInterface, FIF.CHECKBOX, t.basicInput, pos)
        self.addSubInterface(self.dateTimeInterface, FIF.DATE_TIME, t.dateTime, pos)
        self.addSubInterface(self.dialogInterface, FIF.MESSAGE, t.dialogs, pos)
        self.addSubInterface(self.layoutInterface, FIF.LAYOUT, t.layout, pos)
        self.addSubInterface(self.materialInterface, FIF.PALETTE, t.material, pos)
        self.addSubInterface(self.menuInterface, Icon.MENU, t.menus, pos)
        self.addSubInterface(self.navigationViewInterface, FIF.MENU, t.navigation, pos)
        self.addSubInterface(self.scrollInterface, FIF.SCROLL, t.scroll, pos)
        self.addSubInterface(self.statusInfoInterface, FIF.CHAT, t.statusInfo, pos)
        self.addSubInterface(self.textInterface, Icon.TEXT, t.text, pos)
        self.addSubInterface(self.viewInterface, Icon.GRID, t.view, pos)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('zhiyiYo', ':/gallery/images/shoko.png'),
            onClick=self.onSupport,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(960, 800)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('航味__吃在北航')

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        w = MessageBox(
            '🥰🥰🥰🥰🥰',
            '🚀🚀🚀🚀🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')
        if w.exec():
            QDesktopServices.openUrl(QUrl(SUPPORT_URL))

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == "dateTimeInterface":
                self.stackedWidget.setCurrentWidget(w, False)
                dic = {1: '学二', 2: '合一', 3: '新北', 4: 'Wings', 5: '美食苑'}
                print(dic[int(index)])
                w.change(dic[int(index)])
                # w.scrollToCard(index)
