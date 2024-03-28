# SuperFastPython.com
# example of logging from multiple processes with multiprocessing logging
from multiprocessing import get_logger
import logging
import time
import io
import sys



class TqdmToLogger(io.StringIO):
    logger = None
    level = None
    buf = ""

    def __init__(self, logger, level=None, mininterval=5):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO
        self.mininterval = mininterval
        self.last_time = 0

    def write(self, buf):
        self.buf = buf.strip("\r\n\t ")

    def flush(self):
        if len(self.buf) > 0 and time.time() - self.last_time > self.mininterval:
            self.logger.log(self.level, self.buf)
            self.last_time = time.time()

'''
Thread를 이용하지 않음 `while True:` 없음
로그 유실 가능
'''
class Logger():
    logger = get_logger()
    handler = None
    handler2 = logging.StreamHandler(sys.stdout)
    _file_path = None
 
    def __init__(self, file_path):
        '''
        이 부분이 한번이라도 실행되면 로그를 파일에 저장한다.
        '''
        Logger.logger.removeHandler(Logger.handler)
        Logger._file_path = file_path
        Logger.handler = logging.FileHandler(Logger._file_path, mode='a', encoding='utf-8')
        # configure a stream handler
        Logger.logger.addHandler(Logger.handler)
        # log all messages, debug and up
        Logger.logger.setLevel(logging.INFO)
    
    @staticmethod
    def getTqdmLogger():
        if Logger._file_path == None:
            return None # 파일에 로깅을 하지 않는 경우는 console 로깅의 퀄리티를 위해서 None을 리턴한다. 왜냐면 StreamHandler를 적용하면 너무 구림.
        return TqdmToLogger(Logger.logger)

#if Logger.logger.hasHandlers() == False:
#    Logger.logger.addHandler(Logger.handler2)
#    Logger.logger.setLevel(logging.INFO)
