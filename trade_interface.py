from time import sleep

from PyQt5.QAxContainer import QAxWidget
from pythoncom import PumpWaitingMessages

from my_logger import logger
from tr_stock import Opt10081


class TradeInterface(QAxWidget):
    def __init__(self, login_dialog=False):
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.OnEventConnect.connect(self.__handler_login)
        self.OnReceiveTrData.connect(self.__receive_tr_data)

        self.__login_dialog = login_dialog
        self.__active_handle = False

        self.__accounts = list()
        # todo; 실서버 사용시 password 설정, UI 같이 수정, 데이터 저장하기 추가
        self.__pw = '0000'

        self.__receive_handler = dict()

        # TR list =============================
        self.opt10081 = Opt10081(self)

    @staticmethod
    def tr_req_time_delay():
        sleep(0.2)

    @property
    def password(self):
        return self.__pw

    def set_field_data(self, name, value):
        self.dynamicCall("SetInputValue(QString, QString)", name, value)

    def get_field_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)",
                               code, real_type, field_name, index, item_name)
        return ret.strip()

    def get_block_count(self, tr_code, rq_name):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", tr_code, rq_name)
        return ret

    def __waiting_active_handle(self):
        self.__active_handle = False
        while self.__active_handle is False:
            PumpWaitingMessages()
            sleep(0.001)

    def login(self):
        self.dynamicCall("CommConnect()")
        self.__waiting_active_handle()

    def __handler_login(self, err_code):
        logger.info(f"login result; {err_code}")
        if self.__login_dialog is True:
            self.dynamicCall("KOA_Functions(QString, QString)", "ShowAccountWindow", "")
        self.__active_handle = True

        # logger.debug(f"계좌수: {self.GetLoginInfo('ACCOUNT_CNT')}")
        self.__accounts = self.GetLoginInfo('ACCNO').split(';')
        del self.__accounts[-1]
        logger.debug(f"전체 계좌 리스트: {self.__accounts}")
        # logger.debug(f"사용자 ID: {self.GetLoginInfo('USER_ID')}")
        # logger.debug(f"사용자명: {self.GetLoginInfo('USER_NAME')}")

    def add_receive_handler(self, rq_name, handler):
        self.__receive_handler[rq_name] = handler

    def __receive_tr_data(self, screen_no, rq_name, tr_code, record_name, next_, unused1, unused2, unused3, unused4):
        # logger.debug(f"{screen_no, rq_name, tr_code, next_}")
        self.__receive_handler[rq_name](next_)
        self.__active_handle = True

    def comm_rq_data(self, rq_name, tr_code, next_, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rq_name, tr_code, next_, screen_no)
        self.__waiting_active_handle()
