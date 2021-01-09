import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft
import copy
#import wave

#from sympy import *

# 测试积分
def test(t, fc, sample_rate):
    x = np.arange(0, t, 1/sample_rate) 
    zb = 2 * np.pi * x * fc
    y = (0.5*np.sin(zb))
    jf = y.copy()
    jf = jf+1;
    jf[0] = 0;
    for i in range(1, y.size):
        jf[i] = ((y[i] * (1/sample_rate)) + jf[i-1])
    plt.subplot(211)
    plt.plot(x,y)   
    plt.subplot(212)
    plt.plot(x,jf)   
    plt.show()
    return

# 求面积
def test1(t, fc, sample_rate):
    jd = 0.001
    x = np.arange(1.5, 3.5, jd) 
    y = 2*x-3
    jf = y.copy()
    jf[0] = 0;
    for i in range(1, y.size):
        jf[i] = ((y[i] * (jd)) + jf[i-1])
    plt.subplot(211)
    plt.plot(x,y)   
    plt.subplot(212)
    plt.plot(x,jf)   
    print(jf[-1])
    plt.show()
    return

# 角调制 自己认为调频
def test2(t, fc, sample_rate):
    x = np.arange(0, t, 1/sample_rate) 
    #zb = 2 * np.pi * x * 100 # 载波
    signal = 2 * np.pi * x * 5


    
    
    y2 = (0.5*np.sin(signal))

    for iii in range(0, y2.size):
        if (y2[iii] > 0):
            y2[iii] = 0.5
        else:
            y2[iii] = -0.5


    y1 = (0.5*np.sin(2 * np.pi * x * 100))
    y3 = (0.5*np.sin(2 * np.pi * x * (100+(15*y2))))

    plt.subplot(311)
    plt.plot(x,y1) 
    plt.subplot(312)
    plt.plot(x,y2)   
    plt.subplot(313)
    plt.plot(x,y3)   
    plt.show()
    return


# 角调制 
# PM 信号和线性变化
def test3(t, fc, sample_rate):
    x = np.arange(0, t, 1/sample_rate) 
    zb = 2 * np.pi * x * 100 # 载波
    signal = 2 * np.pi * x * 5

    y2 = (0.5*np.cos(signal))
    
    '''
    for iii in range(1, y2.size):
        if (y2[iii]>0):
            y2[iii] = 0.5;
        else:
            y2[iii] = -0.5;
    '''

    
    y2fm = y2.copy()

    
    for iii in range(1, y2fm.size):
        y2fm[iii] = y2fm[iii-1] + y2fm[iii] 
    
    y2fm = y2fm * 0.05;
    

    y1 = (0.5*np.cos(zb))
    y3 = (0.5*np.cos(zb+y2fm))

    plt.subplot(411)
    plt.plot(x,y1) 
    plt.subplot(412)
    plt.plot(x,y2)   
    plt.subplot(413)
    plt.plot(x,y3)  



    fft_y=fft(y3)
    fft_y=abs(fft_y)
    fft_y=fft_y/len(x)
    print(sample_rate, len(x))
    fft_x=np.linspace(0, sample_rate-1, len(x))
    plt.subplot(414)
    plt.plot(fft_x,fft_y)  


    plt.show()
    return


# 网上抄的
def test4(t, fc, sample_rate):
    dt = 0.001;
    t = np.arange(0, 1.5, dt)
    am = 5; # 调制信号幅度
    fm = 2; # 调制信号频率
    mt = am * np.cos(2 * np.pi * fm * t)

    fc = 50; # 载波
    ct = np.cos(2 * np.pi * fc * t)

    kf = 6; # 调频指数

    int_mt = mt.copy()
    int_mt[0] = 0;

    for iii in range (1, int_mt.size):
        int_mt[iii] = int_mt[iii]*dt + int_mt[iii-1];


    sfm= am * np.cos((2 * np.pi * fc * t) + (2 * np.pi * int_mt * kf))

    plt.subplot(311)
    plt.plot(t,mt) 
    plt.subplot(312)
    plt.plot(t,ct) 
    plt.subplot(313)
    plt.plot(t,sfm) 
    plt.show()
    return

# 采样率
if __name__=="__main__":
    #x,y = gen_iqtest2(1,1,16000)
    test4(1,5,16000)