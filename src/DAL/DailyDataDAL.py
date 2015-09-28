from BaseDAL import BaseDAL
from src.Data.DailyData import DailyData
from src.Exception import FileNotExistException
from src.Constants import Constants

__author__ = 'yzhou7'


# this class is DAL layer to load data for buyer, including
# 1. single date
# 2. all dates

class DailyDataDAL(BaseDAL):
    MATCH_ALL_DATE = '*'
    MATCH_ALL_USER = "*"

    @staticmethod
    def fetchAll():
        return DailyDataDAL.fetchAllByDate(DailyDataDAL.MATCH_ALL_DATE)

    @staticmethod
    def fetchAllByDate(date):
        if not BaseDAL.checkFileExist(Constants.BUYER_FILE_PATH):
            # TODO fix exception
            # raise FileNotExistException(Constants.BUYER_FILE_PATH)
            print "file not exist for: " + Constants.BUYER_FILE_PATH
            return list()

        lines = BaseDAL.readAll(Constants.BUYER_FILE_PATH)
        return DailyDataDAL.parse(lines, date)

    @staticmethod
    def fetchByNameDate(date, userName):
        if not BaseDAL.checkFileExist(Constants.BUYER_FILE_PATH):
            # TODO fix exception
            # raise FileNotExistException(Constants.BUYER_FILE_PATH)
            print "file not exist for: " + Constants.BUYER_FILE_PATH
            return list()

        lines = BaseDAL.readAll(Constants.BUYER_FILE_PATH)
        return DailyDataDAL.parse(lines, date, userName)

    @staticmethod
    def parse(lines, targetDate, targetUserName = '*'):
        dailyScore = dict()

        # parse line into DailyData structure
        for line in lines:
            items = line.strip().split("|")
            if len(items) < 3:
                print "line is invalid: " + line
                break
            userName = items[0]
            date = items[1]
            scores = items[2]

            if targetUserName != DailyDataDAL.MATCH_ALL_USER \
                    and userName != targetUserName:
                continue

            if date != targetDate:
                continue

            if dailyScore.has_key(userName):
                dailyScore[userName].extend(scores.split("#"))
            else:
                dailyScore[userName] = scores.split("#")

        return DailyData(date, dailyScore)


if __name__ == "__main__":
    lines = ['aa|20050901|100#200',
             'aa|20050902|300',
             "bb|20050901|21",
             "bb|20050101|2#2#222"]

    # print "no date filter"
    # print DailyDataDAL.parse(lines, "*").__dict__

    print "filter with date 20050901"
    print DailyDataDAL.parse(lines, "20050901").__dict__

    print "filter with date 20050901 and name aa"
    print DailyDataDAL.parse(lines, "20050901", "aa").__dict__
