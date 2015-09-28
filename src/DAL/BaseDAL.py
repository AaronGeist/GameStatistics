__author__ = 'yzhou7'

import os

class BaseDAL:
    ACCESS_READ_ONLY = "r"
    ACCESS_WRITE_ONLY = "w"

    @staticmethod
    def checkFileExist(file_path):
        return os.path.exists(file_path) and os.path.isfile(file_path)

    @staticmethod
    def loadFile(file_path, access_mode):
        file = open(file_path, access_mode)
        return file

    # return lines in list
    @staticmethod
    def readAll(file_path):
        file = BaseDAL.loadFile(file_path, BaseDAL.ACCESS_READ_ONLY)
        result = list()
        for line in file.readlines():
            line = line.strip()
            result.append(line)
        file.close()

        # result.sort()
        return result

    # TODO maybe use seek?
    @staticmethod
    def readLine(file_path, offset):
        file = BaseDAL.loadFile(file_path, BaseDAL.ACCESS_READ_ONLY)
        result = file.readline()
        return result

    @staticmethod
    def writeAll(file_path, line_list):
        file = BaseDAL.loadFile(file_path, BaseDAL.ACCESS_WRITE_ONLY)
        file.writelines(line_list)
        file.close()
        return
