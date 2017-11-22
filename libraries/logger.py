"""
Created on Nov 22, 2017

@author: nhan.nguyen
"""

import sys
import os
import time
import errno
import logging
from .result import Status


class Printer(object):
    """
    Class that write content to several file.
    Use this class when you want to write log
    not only on console but only on some other files.
    """
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        """
        Write a content into several files.
        :param obj: content you want to write.
        """
        for f in self.files:
            f.write(obj)
            f.flush()  # Want this content is displayed immediately on file

    def flush(self):
        """
        Make the content in buffer display immediately on files
        """
        for f in self.files:
            f.flush()


class Logger:
    __log_dir = os.path.join(os.path.dirname(__file__), "..") + "/test output/log files/"
    __KEEP_LOG_FLAG = "-keeplog"
    __LOG_LVL = logging.DEBUG

    def __init__(self, test_name: str):
        Logger.__init_log_folder()
        self.__log_file_path = "{}{}_{}.log".format(Logger.__log_dir, test_name,
                                                    str(time.strftime("%Y-%m-%d_%H-%M-%S")))
        self.__log = open(self.__log_file_path, "w")
        self.__original_stdout = sys.stdout
        sys.stdout = Printer(sys.stdout, self.__log)
        logging.basicConfig(stream=sys.stdout, level=Logger.__LOG_LVL)

    def save_log(self, test_status: str):
        """
        If "-keeplog" is exist in sys.argv or test_status is Failed then keeping the log file.
        If test_status is Passed and missing "-keeplog" from sys.argv then deleting log file.
        :param test_status: Passed of Failed
        """
        self.__log.close()
        if test_status == Status.PASSED and Logger.__KEEP_LOG_FLAG not in sys.argv:
            if os.path.isfile(self.__log_file_path):
                os.remove(self.__log_file_path)
        sys.stdout = self.__original_stdout

    @staticmethod
    def __init_log_folder():
        try:
            os.makedirs(Logger.__log_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e