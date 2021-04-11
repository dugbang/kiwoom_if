from my_logger import logger


class Opt10001:
    """
    주식기본정보요청
    """
    def __init__(self, interface=None):
        self.__rq_name = 'opt10001_req'
        self.__tr_code = 'opt10001'
        self.__screen_no = '1001'
        self.__next = '0'

        self.__if = interface
        self.__if.add_receive_handler(self.__rq_name, self.__receive_data)

        self.records = list()

    @property
    def is_next(self):
        return True if self.__next == '2' else False

    def __receive_data(self, next_):
        logger.debug(f"__receive_data; {self.__class__.__name__}")
        code = self.__if.get_field_data(self.__tr_code, '', self.__rq_name, 0, '종목코드')
        name = self.__if.get_field_data(self.__tr_code, '', self.__rq_name, 0, '종목명')
        # .... 생략
        price = self.__if.get_field_data(self.__tr_code, '', self.__rq_name, 0, '현재가')

        self.records.append((code, name, price))

    def download(self, code):
        self.records = list()
        self.__next = '0'
        self.__if.set_field_data('종목코드', code)
        self.__if.comm_rq_data(self.__rq_name, self.__tr_code, self.__next, self.__screen_no)

    def records_output(self):
        for r in self.records:
            logger.debug(r)


class Opt10081:
    """
    주식일봉차트조회요청
    """
    def __init__(self, interface=None):
        self.__rq_name = 'opt10081_req'
        self.__tr_code = 'opt10081'
        self.__screen_no = '1081'
        self.__next = '0'

        self.__if = interface
        self.__if.add_receive_handler(self.__rq_name, self.__receive_data)

        self.records = list()

    @property
    def is_next(self):
        return True if self.__next == '2' else False

    def __receive_data(self, next_):
        logger.debug(f"__receive_data; {self.__class__.__name__}")
        self.__next = next_
        for i in range(self.__if.get_block_count(self.__tr_code, self.__rq_name)):
            date = int(self.__if.get_field_data(self.__tr_code, "", self.__rq_name, i, "일자"))
            open_ = int(self.__if.get_field_data(self.__tr_code, "", self.__rq_name, i, "시가"))
            high = int(self.__if.get_field_data(self.__tr_code, "", self.__rq_name, i, "고가"))
            low = int(self.__if.get_field_data(self.__tr_code, "", self.__rq_name, i, "저가"))
            close = int(self.__if.get_field_data(self.__tr_code, "", self.__rq_name, i, "현재가"))
            volume = int(self.__if.get_field_data(self.__tr_code, "", self.__rq_name, i, "거래량"))

            self.records.append([date, open_, high, low, close, volume])

    def download(self, s_date, code, modify_price=1):
        logger.debug(f"download; {s_date}, {code}")
        self.records = list()
        self.__next = '0'
        self.__if.set_field_data('종목코드', code)
        self.__if.set_field_data('기준일자', s_date)
        self.__if.set_field_data('수정주가구분', modify_price)
        self.__if.comm_rq_data(self.__rq_name, self.__tr_code, self.__next, self.__screen_no)

        # todo; 계속 받아짐... e_date 등의 별도 종료조건이 필요할 듯
        # while self.is_next:
        #     self.__if.tr_req_time_delay()
        #     self.__if.set_field_data('종목코드', code)
        #     self.__if.set_field_data('기준일자', s_date)
        #     self.__if.set_field_data('수정주가구분', modify_price)
        #     self.__if.comm_rq_data(self.__rq_name, self.__tr_code, self.__next, self.__screen_no)
        #     break

    def records_output(self, length=5):
        for r in self.records[:length]:
            logger.debug(r)
