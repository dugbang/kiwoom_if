import sys

from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

from my_logger import logger
from trade_interface import TradeInterface


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 350)

        btn = QPushButton('Test', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.__bt_test)

        # self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        # self.kiwoom.dynamicCall("CommConnect()")

        self.__if = TradeInterface(login_dialog=False)
        self.__if.login()

        logger.debug('end... handler')

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 160, 280, 80)
        self.text_edit.setEnabled(False)
        self.text_edit.append("로그인 정보")

    def __bt_test(self):
        self.__if.opt10081.download(s_date=20210331, code='000660')
        self.__if.opt10081.records_output()

        self.__if.opt10001.download(code='000660')
        self.__if.opt10001.records_output()

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")
        else:
            self.text_edit.append("로그인 실패")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
