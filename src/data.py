import numpy as np
import matplotlib.pyplot as plt
class Data:
    """ 核心数据类,包含了计算和绘图的功能,使用numpy数组保留后期推断的功能
    :Attributes:
        date: list[日期-str],日期表,日期格式03/25
        value: numpy.array[数据-float],数据,与date一一对应
        __mean: tuple[tuple[日期-str,数据-float]]
        __max: tuple[tuple[日期-str,数据-float]]
        __min: tuple[tuple[日期-str,数据-float]]
        __median: tuple[tuple[日期-str,数据-float]]
    """

    def __init__(self, data_chart: dict) -> None:
        """ 核心数据类,计算所需的所有数据
        :arg data_chart: dict[每天的日期-str:数据-float]
        """
        self.__date = []
        value = []
        for i, j in data_chart.items():
            self.__date.append(i)
            value.append(j)
        self.__value = np.array(value)
        self.length = len(self.__value)
        self.__mean = self.__value.mean()
        self.__max = self.get(value=self.__value.max())
        self.__min = self.get(value=self.__value.min())
        self.__median = np.median(self.__value)

    def get(self, index=None, date=None, value=None):
        """
        返回由索引，日期或数据的信息，注意：返回值为tuple的tuple
        :param index: 第几个-int
        :param date: 日期-str,日期格式"03/25"
        :param value: 值,value
        :return: tuple[tuple[日期-str,数据-float]]
        :exception: ValueError
        """
        if index is not None:
            return (self.__date[index], self.__value[index]),
        elif date is not None:
            temp = self.__date.index(date)
            return (date, self.__value[temp]),
        elif value is not None:
            temp = (np.where(self.__value == value))[0]
            res = []
            for i in temp:
                res.append((self.__date[i], self.__value[i]))
            return tuple(res)
        else:
            raise ValueError

    def get_date(self):
        return self.__date

    def get_index(self, date):
        return self.__date.index(date)

    def mean(self):
        """
        :return:平均数-float
        """
        return self.__mean

    def max(self):
        """
        :return: 最大值的坐标组,tuple[tuple[日期-str,数据-float]]
        """
        return self.__max

    def min(self):
        """
        :return: 最小值的坐标组,tuple[tuple[日期-str,数据-float]]
        """
        return self.__min

    def median(self):
        """
        :return: 中位数的坐标组,tuple[tuple[日期-str,数据-float]]
        """
        return self.__median

    def plot(self, fig, start, end):
        """
        绘制曲线
        :param start: 开始绘制的天数(包括）
        :param end: 结束绘制的天数(含）
        :param fig: 绘制的区域
        :return:
        """
        date = self.__date[self.get_index(start):self.get_index(end) + 1]
        value = self.__value[self.get_index(start):self.get_index(end) + 1]
        fig.plot(date, value)

    def part_data(self, start, end):
        """
        data的
        """
        date = self.__date[self.get_index(start):self.get_index(end) + 1]
        value = self.__value[self.get_index(start):self.get_index(end) + 1]
        res = {}
        for i in range(len(date)):
            res[date[i]] = value[i]
        return Data(res)
