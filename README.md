# 电子系统导论第一次作业 —— 疫情统计图

## 该如何运行该作业？

已经为windows和MacOSX系统打包exe和app文件，直接运行即可。
如果想使用源码运行，请确保安装了numpy, matplotlib, tk（推荐使用anaconda环境)，在主目录下`python main.py`即可。如果出现网络错误，可能是因为防火长城，科学上网绕过即可。
下附全部包和版本:

```
# Name                    Version                   Build 
asn1crypto                1.3.0                    py37_0  
blas                      1.0                         mkl  
ca-certificates           2020.1.1                      0  
certifi                   2019.11.28               py37_0  
cffi                      1.14.0           py37hb5b8e2f_0  
chardet                   3.0.4                 py37_1003  
cryptography              2.8              py37ha12b0ac_0  
cycler                    0.10.0                   py37_0  
freetype                  2.9.1                hb4e5f40_0  
idna                      2.9                        py_1  
intel-openmp              2019.4                      233  
kiwisolver                1.1.0            py37h0a44026_0  
libcxx                    4.0.1                hcfea43d_1  
libcxxabi                 4.0.1                hcfea43d_1  
libedit                   3.1.20181209         hb402a30_0  
libffi                    3.2.1                h475c297_4  
libgfortran               3.0.1                h93005f0_2  
libpng                    1.6.37               ha441bb4_0  
matplotlib                3.1.3                    py37_0  
matplotlib-base           3.1.3            py37h9aa3819_0  
mkl                       2019.4                      233  
mkl-service               2.3.0            py37hfbe908c_0  
mkl_fft                   1.0.15           py37h5e564d8_0  
mkl_random                1.1.0            py37ha771720_0  
ncurses                   6.2                  h0a44026_0  
numpy                     1.18.1           py37h7241aed_0  
numpy-base                1.18.1           py37h6575580_1  
openssl                   1.1.1e               h1de35cc_0  
pip                       20.0.2                   py37_1  
pycparser                 2.20                       py_0  
pyopenssl                 19.1.0                   py37_0  
pyparsing                 2.4.6                      py_0  
pysocks                   1.7.1                    py37_0  
python                    3.7.6                h359304d_2  
python-dateutil           2.8.1                      py_0  
readline                  7.0                  h1de35cc_5  
requests                  2.23.0                   py37_0  
setuptools                46.0.0                   py37_0  
six                       1.14.0                   py37_0  
sqlite                    3.31.1               ha441bb4_0  
tk                        8.6.8                ha441bb4_0  
tornado                   6.0.4            py37h1de35cc_1  
urllib3                   1.25.8                   py37_0  
wheel                     0.34.2                   py37_0  
xz                        5.2.4                h1de35cc_4  
zlib                      1.2.11               h1de35cc_3  

```

## 该如何阅读这份作业的源代码？

架构如下：
```
.
├── README.md(说明文件)
├── font
│   └── wqy-microhei.ttc(字体文件)
├── main.py(主函数)
└── src
    ├── data.py(数据的处理和操作)
    ├── dataGetter.py(自动从网络获取数据)
    └── gui.py(图形界面)


```

## 作者和License

作者: 王少文
License: GPLv3, Apache2, 详见license文件夹(主要是开源字体的要求)
