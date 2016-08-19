from redispider.master import Master
import time


if __name__ == '__main__':
    myMaster = Master('172.31.34.39', password='123456')
    myMaster.start()

