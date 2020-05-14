import requests
import json
import time
from tkinter.messagebox import showerror,showinfo
from .data import Data

ADDRESS = "https://github.com/BlankerL/DXY-COVID-19-Data/raw/master/json/DXYOverall-TimeSeries.json"
DEFAULT_LIST = [{'time': '02/01', 'new': 2090, 'accum': 11901, 'now': 11367},
                {'time': '02/02', 'new': 2589, 'accum': 14490, 'now': 13752},
                {'time': '02/03', 'new': 2851, 'accum': 17341, 'now': 16453},
                {'time': '02/04', 'new': 3189, 'accum': 20530, 'now': 19386},
                {'time': '02/05', 'new': 3904, 'accum': 24434, 'now': 22923},
                {'time': '02/06', 'new': 3704, 'accum': 28138, 'now': 26201},
                {'time': '02/07', 'new': 3126, 'accum': 31264, 'now': 28874},
                {'time': '02/08', 'new': 3409, 'accum': 34673, 'now': 31574},
                {'time': '02/09', 'new': 2616, 'accum': 37289, 'now': 33576},
                {'time': '02/10', 'new': 2973, 'accum': 40262, 'now': 35802},
                {'time': '02/11', 'new': 2485, 'accum': 42747, 'now': 37429},
                {'time': '02/12', 'new': 2018, 'accum': 44765, 'now': 38583},
                {'time': '02/13', 'new': 15142, 'accum': 59907, 'now': 52324},
                {'time': '02/14', 'new': 4043, 'accum': 63950, 'now': 55476},
                {'time': '02/15', 'new': 2631, 'accum': 66581, 'now': 56563},
                {'time': '02/16', 'new': 2014, 'accum': 68595, 'now': 57165},
                {'time': '02/17', 'new': 2049, 'accum': 70644, 'now': 57594},
                {'time': '02/18', 'new': 1888, 'accum': 72532, 'now': 57657},
                {'time': '02/19', 'new': 1752, 'accum': 74284, 'now': 57337},
                {'time': '02/20', 'new': 396, 'accum': 74680, 'now': 55837},
                {'time': '02/21', 'new': 891, 'accum': 75571, 'now': 54645},
                {'time': '02/22', 'new': 825, 'accum': 76396, 'now': 52973},
                {'time': '02/23', 'new': 652, 'accum': 77048, 'now': 51420},
                {'time': '02/24', 'new': 221, 'accum': 77269, 'now': 49666},
                {'time': '02/25', 'new': 516, 'accum': 77785, 'now': 47464},
                {'time': '02/26', 'new': 410, 'accum': 78195, 'now': 45399},
                {'time': '02/27', 'new': 436, 'accum': 78631, 'now': 42968},
                {'time': '02/28', 'new': 331, 'accum': 78962, 'now': 39859},
                {'time': '02/29', 'new': 432, 'accum': 79394, 'now': 37248}]


def get_time(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000))


def get_raw_data():
    try:
        r = requests.get(ADDRESS)
    except requests.exceptions.RequestException as e:
        showerror("网络错误", "无法连接github,请更换网络环境或稍后再试\n悄悄说最近github好像被墙了，可以搭个梯子就能访问成功了qwq\n"+str(e))
        return None
    json_data = r.content.decode()
    dict_data_list = json.loads(json_data)
    temp = ''
    res = []
    ans = []
    for each_dict in dict_data_list:
        time_str = get_time(each_dict['updateTime'])
        if time_str[:11] != temp[:11]:
            temp = time_str
            res.append(each_dict)
    res = list(reversed(res))
    for i in range(len(res)):
        time_str = get_time(res[i]['updateTime'])
        if i == 0:
            new = 444
        else:
            new = res[i]['confirmedCount'] - res[i - 1]['confirmedCount']
        accum = res[i]['confirmedCount']
        now = res[i]['confirmedCount'] - res[i]['curedCount'] - res[i]['deadCount']
        ans.append({'time': time_str[5:7] + '/' + time_str[8:10], 'new': new, 'accum': accum, 'now': now})
    return ans


def get_data(offline=True):
    new = {}
    accum = {}
    now = {}
    if offline is True:
        raw_data = DEFAULT_LIST
    else:
        raw_data = get_raw_data()
        if raw_data is None:
            raw_data = DEFAULT_LIST
        else:
            showinfo("成功","获取数据成功")
    for v in raw_data:
        new[v['time']] = v['new']
        accum[v['time']] = v['accum']
        now[v['time']] = v['now']
    return Data(new), Data(accum), Data(now)


if __name__ == '__main__':
    get_data(offline=False)
