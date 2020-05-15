# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
from tkinter import *
import matplotlib.ticker as ticker
from . import dataGetter
from tkinter import ttk
from tkinter.messagebox import *
import tkinter.filedialog
from .data import Data
import sys


def get_data(offline=True):
    return dataGetter.get_data(offline)


class Gui:
    """ GUI类，控制交互
    """

    def __init__(self, master):
        self.master = master
        # 这一部分是进行跨平台优化
        self.plt_font = fm.FontProperties(fname="./font/wqy-microhei.ttc")
        if sys.platform == 'darwin':
            self.size = "600x700"
            self.ctrl_width=21
            self.title_font = ("PingFang SC", 40, 'bold')
            self.ctrl_font = ("PingFang SC", 14)
            self.info_font = ("PingFang SC", 15)
            self.help_font = ("PingFang SC", 13)
            self.plt_dpi=120
            self.plt_height=2.9
        elif sys.platform == 'win32':
            self.size = "600x580"
            self.ctrl_width=15
            self.title_font = ("Microsoft YaHei UI", 30, 'bold')
            self.ctrl_font = ("Microsoft YaHei UI", 12)
            self.info_font = ("Microsoft YaHei UI", 13)
            self.help_font = ("Microsoft YaHei UI", 10)
            self.plt_dpi=100
            self.plt_height=2.2
        # 数据设置
        self.data_new, self.data_accum, self.data_now = get_data()
        # 界面的设置
        master.geometry(self.size)
        master.config(bg='#F0F0F0')
        master.title("疫情数据展示")
        # 标题的设置
        self.title_Frame = Frame(master)
        self.title_Frame.config(bg='#F0F0F0')
        self.title_Frame.pack()
        self.title = Label(self.title_Frame,
                           text="        疫情数据展示",
                           bg='#F0F0F0',
                           fg='blue',
                           font=self.title_font,
                           height=0,
                           width=15
                           )
        self.title.pack(side=LEFT)
        # 获取数据按钮的设计

        def update_data():
            self.data_new, self.data_accum, self.data_now = get_data(
                offline=False)
            self.start.config(value=self.data_now.get_date())
            self.end.config(value=self.data_now.get_date())

        get_data_button = Button(
            self.title_Frame, font=self.ctrl_font, text="重新获取数据", command=update_data)
        get_data_button.pack(side=LEFT)
        # 勾选框的设置
        self.choice = {'new': IntVar(
            value=1), 'accum': IntVar(), 'now': IntVar(), 'log': IntVar()}
        test = IntVar()
        self.checker_frame = Frame(master, width=20)
        self.checker_frame.pack(fill=X)
        self.checker_frame.config(bg='#F0F0F0')
        self.c_new = Checkbutton(self.checker_frame, text='新增人数', font=self.ctrl_font,
                                 width= self.ctrl_width, variable=self.choice['new'], command=self.re_plot)
        self.c_new.pack(side=LEFT, expand=YES, fill=X)
        self.c_accum = Checkbutton(self.checker_frame, text='累计人数', font=self.ctrl_font,
                                   width= self.ctrl_width, variable=self.choice['accum'], command=self.re_plot)
        self.c_accum.pack(side=LEFT, expand=YES, fill=X)
        self.c_now = Checkbutton(self.checker_frame, text='现有人数', font=self.ctrl_font,
                                 width= self.ctrl_width, variable=self.choice['now'], command=self.re_plot)
        self.c_now.pack(side=LEFT, expand=YES, fill=X)
        # 插入matplotlib的图片
        self.canvas_frame = Frame()
        self.canvas_frame.pack()
        self.canvas = self.plot(choice=self.choice)
        self.canvas.pack(side=TOP, fill=BOTH)
        # 写下一行，包含开始时间，结束时间和是否以log显示
        self.choice_frame = Frame(master, bg='#F0F0F0')
        self.choice_frame.pack(fill=X)

        # 写选择逻辑
        def re_gen(*args):
            if self.data_now.get_index(self.start.get()) > self.data_now.get_index(self.end.get()):
                showerror('ValueError', '开始天数应至少早于结束天数1天')
            else:
                self.re_plot()
                self.change_text(choice='new')
                self.change_text(choice='accum')
                self.change_text(choice='now')

        Label(self.choice_frame, text='  开始日期：',
              bg='#F0F0F0', bd=0, width=10).pack(side=LEFT)
        self.start = ttk.Combobox(
            self.choice_frame, value=self.data_now.get_date(), width=7)
        self.start.current(self.data_now.get_date().index('02/01'))
        self.start.pack(side=LEFT, expand=YES, fill=X)
        self.start.bind("<<ComboboxSelected>>", re_gen)
        Label(self.choice_frame, text='   结束日期：',
              bg='#F0F0F0', bd=0, width=10).pack(side=LEFT)
        self.end = ttk.Combobox(
            self.choice_frame, value=self.data_now.get_date(), width=7)
        self.end.current(self.data_now.get_date().index('02/29'))
        self.end.pack(side=LEFT, expand=YES, fill=X)
        self.end.bind("<<ComboboxSelected>>", re_gen)
        self.c_log = Checkbutton(self.choice_frame, text='Log  ',
                                 width=16, variable=self.choice['log'], command=self.re_plot, bg='#F0F0F0')
        self.c_log.pack(side=LEFT, expand=YES, fill=X)
        # 最下端的文字展示栏
        # 3个listbox，分别展示...的最大最小平均中位
        show_frame = Frame(master)
        show_frame.pack(fill=X)
        self.new_case = Text(show_frame, font=self.info_font, height=6, width=19)
        self.change_text(choice='new')
        self.new_case.pack(side=LEFT)
        self.accum_case = Text(show_frame, font=self.info_font, height=6, width=20)
        self.change_text(choice='accum')
        self.accum_case.pack(side=LEFT)
        self.now_case = Text(show_frame, font=self.info_font, height=6, width=19)
        self.change_text(choice='now')
        self.now_case.pack(side=LEFT)
        # 这是最下方的文字
        help_text = Label(self.master, text="因本人水平有限，有以下几点需要使用者注意:\n"
                          + "1.请尽量不要使用重新获取数据，本软件的数据来源于科研数据API，请将该API留给真正需要的人\n"
                          + "2.窗口的大小调整功能仍不是很完善，请尽量保持在原窗口大小\n"
                          "3.欢迎发邮件到19307130251@fudan.edu.cn与我讨论", font=self.help_font,justify=LEFT, bg='#F0F0F0')
        help_text.pack(side=TOP)

    def change_text(self, choice):
        """
        改变下方数据显示框的内容
        """
        if choice == 'new':
            textbox = self.new_case
            data = self.data_new.part_data(self.start.get(), self.end.get())
        if choice == 'accum':
            textbox = self.accum_case
            data = self.data_accum.part_data(self.start.get(), self.end.get())
        if choice == 'now':
            textbox = self.now_case
            data = self.data_now.part_data(self.start.get(), self.end.get())
        textbox.delete(0.0, END)
        if choice == 'new':
            textbox.insert(END, '新增感染统计\n')
        if choice == 'accum':
            textbox.insert(END, '累计感染统计\n')
        if choice == 'now':
            textbox.insert(END, '现有感染统计\n')
        textbox.insert(END, '最大值: ' + str(
            data.max()[0][0]) + '->' + str(
            data.max()[0][1]) + '人\n')
        textbox.insert(END, '最小值: ' + str(
            data.min()[0][0]) + '->' + str(
            data.min()[0][1]) + '人\n')
        textbox.insert(END, '平均值: ' + str(int(data.mean())) + '人\n')
        textbox.insert(END, '中位值: ' + str(int(data.median())) + '人\n')

    def re_plot(self):
        """
        调用plot函数，重新绘制图像
        """
        self.canvas = self.plot(start=self.start.get(),
                                end=self.end.get(),
                                original=self.canvas,
                                choice=self.choice)
        self.canvas.pack(side=TOP, fill=BOTH)

    def plot(self, start='02/01', end='02/29', original=None, choice=None):
        """
        返回所用的均为fig_file, 但实际绘图的是fig_file的子图
        :param end: 结束
        :param start: 开始
        :param choice: 选项
        :param original: 原来的canvas,方便删除
        :return: 被封装好的tk图片
        """
        fig_file = plt.Figure(figsize=(6.4, self.plt_height), dpi=self.plt_dpi)
        fig = fig_file.add_subplot(111)
        legend = []
        if choice['log'].get():
            fig.set_yscale('log')
        if choice['new'].get():
            self.data_new.plot(fig, start, end)
            legend.append("新增病例")
        if choice['accum'].get():
            self.data_accum.plot(fig, start, end)
            legend.append("累计病例")
        if choice['now'].get():
            self.data_now.plot(fig, start, end)
            legend.append("现有病例")
        fig.legend(legend, prop=self.plt_font, loc='upper left')
        if self.data_now.get_index(end)-self.data_now.get_index(start) > 6:
            fig.xaxis.set_major_locator(
                ticker.MultipleLocator((self.data_now.get_index(end)-self.data_now.get_index(start)) // 6))  # 设置X轴的刻度
            fig.xaxis.set_minor_locator(ticker.MultipleLocator(1))
        if original is None:
            return FigureCanvasTkAgg(fig_file, self.canvas_frame).get_tk_widget()
        else:
            original.destroy()
            return FigureCanvasTkAgg(fig_file, self.canvas_frame).get_tk_widget()
