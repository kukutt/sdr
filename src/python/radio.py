import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft
import copy
#import wave

#from sympy import *

def gen(t, fc, sample_rate):
    x = np.arange(0, t, 1/sample_rate) 
    zb = 2 * np.pi * x * fc
    signal = x
    y = 0.5*np.sin(zb+signal)
    return (x,y);

def gen_iqtest2(t, fc, sample_rate):

    x = np.arange(0, t, 1/sample_rate) 
    
    Ac = 1
    fc = 50
    i = np.ones(len(x));
    q = np.ones(len(x));

    c = (Ac*np.cos(2*np.pi*fc*x));
    cc = (Ac*np.sin(2*np.pi*fc*x));

    
    for ii in range(len(x)):
        if (ii < int((len(x)/4)*1)):
            i[ii] = 1;
            q[ii] = 1;
        elif (ii < int((len(x)/4)*2)):
            i[ii] = 1;
            q[ii] = -1;
        elif (ii < int((len(x)/4)*3)):
            i[ii] = 0.5;
            q[ii] = 1;
        else:
            i[ii] = 0.5;
            q[ii] = 0.5;
    

    y = ((c) * (i)) - ((cc) * (q));


    plt.subplot(311)
    plt.plot(x,c)   
    plt.subplot(312)
    plt.plot(x,y)   


    fft_y=fft(y)
    fft_y=abs(fft_y)
    fft_y=fft_y/len(x)
    print(sample_rate, len(x))
    fft_x=np.linspace(0, sample_rate-1, len(x))

    plt.subplot(313)
    plt.plot(fft_x,fft_y)

    plt.show()
    return (x,y)

def gen_iqtest(t, fc, sample_rate):

    x = np.arange(0, t, 1/sample_rate) 
    
    Ac = 1
    fc = 50

    Ai = 1
    fi = 5
    Aq = 1
    fq = 5

    c = (Ac*np.cos(2*np.pi*fc*x));
    i = (Ai*np.cos(2*np.pi*fi*x));


    cc = (Ac*np.sin(2*np.pi*fc*x));
    q = (Aq*np.sin(2*np.pi*fq*x));

    y = ((c) * (i)) + ((cc) * (q));


    plt.subplot(411)
    plt.plot(x,c)   
    plt.subplot(412)
    plt.plot(x,q)   
    plt.subplot(413)
    plt.plot(x,y)   


    fft_y=fft(y)
    fft_y=abs(fft_y)
    fft_y=fft_y/len(x)
    print(sample_rate, len(x))
    fft_x=np.linspace(0, sample_rate-1, len(x))

    plt.subplot(414)
    plt.plot(fft_x,fft_y)

    plt.show()
    return (x,y)

def gen_am(t, fc, sample_rate):
    x = np.arange(0, t, 1/sample_rate) 
    
    A0 = 0;
    Am = 1;
    fm = 5;

    Ac = 1;
    fc = 2000;

    m = (Am*np.cos(2*np.pi*fm*x));

    
    for ii in range(len(m)):
        if (m[ii] > 0):
            m[ii] = Am;
        else:
            m[ii] = 0;
    

    c = (Ac*np.cos(2*np.pi*fc*x));
    y = (A0+m)*c;

    plt.subplot(611)
    plt.plot(x,m)   
    plt.subplot(612)
    plt.plot(x,c)   
    plt.subplot(613)
    plt.plot(x,y)   


    fft_y=fft(y)
    fft_y=abs(fft_y)
    fft_y=fft_y/len(x)
    print(sample_rate, len(x))
    fft_x=np.linspace(0, sample_rate-1, len(x))

    plt.subplot(614)
    plt.plot(fft_x,fft_y)

    # 解调

    yj = y * c
    plt.subplot(615)
    plt.plot(x,yj)   

    fft_yj=fft(yj)
    fft_yj=abs(fft_yj)
    fft_yj=fft_yj/len(x)
    plt.subplot(616)
    plt.plot(fft_x,fft_yj)

    plt.show();

    return (x,y);



# am ssb dsb 测试
def gen_am_lb(t, fc, sample_rate):
    x = np.arange(0, t, 1/sample_rate) 
    
    A0 = 1;
    Am = 1;
    fm = 5;

    Ac = 1;
    fc = 2000;

    m = (Am*np.cos(2*np.pi*fm*x));

    '''
    for ii in range(len(m)):
        if (m[ii] > 0):
            m[ii] = Am;
        else:
            m[ii] = -Am;
    '''

    c = (Ac*np.cos(2*np.pi*fc*x));
    y = (A0+m)*c;

    plt.subplot(611)
    plt.plot(x,m)   
    plt.subplot(612)
    plt.plot(x,c)   
    plt.subplot(613)
    plt.plot(x,y)   


    fft_y=fft(y)
    fft_y=abs(fft_y)
    fft_y=fft_y/len(x)
    print(sample_rate, len(x))
    fft_x=np.linspace(0, sample_rate-1, len(x))

    plt.subplot(614)
    plt.plot(fft_x,fft_y)

    # 滤波 fft方式
    filter_y1 = copy.deepcopy(fft_y)
    filter_y1 = filter_y1 * len(x)

    for i in range(len(x)):
        if (i >= 8000):
            filter_y1[i] = 0;
    
    for i in range(int(len(x)/2)):
        if (i > 1998):
            filter_y1[i] = 0;
    


    filter_y1_src = ifft(filter_y1);
    filter_y1_src = filter_y1_src.real * 2;


    print(filter_y1_src[0:5])
    plt.subplot(615)
    plt.plot(x,filter_y1_src)


    fft_y=fft(filter_y1_src)
    fft_y=abs(fft_y)
    fft_y=fft_y/len(x)

    plt.subplot(616)
    plt.plot(fft_x,fft_y)


    plt.show();

    return (x,y);


# 解调 + 滤波
def gen_am_jt(t, fc, sample_rate):
    x = np.arange(0, t, 1/sample_rate) 
    
    A0 = 1;
    Am = 1;
    fm = 5;

    Ac = 1;
    fc = 2000;

    m = (Am*np.cos(2*np.pi*fm*x));

    '''
    for ii in range(len(m)):
        if (m[ii] > 0):
            m[ii] = Am;
        else:
            m[ii] = -Am;
    '''

    c = (Ac*np.cos(2*np.pi*fc*x));
    y = (A0+m)*c;

    plt.subplot(611)
    plt.plot(x,m)   
    plt.subplot(612)
    plt.plot(x,c)   
    plt.subplot(613)
    plt.plot(x,y)   


    fft_y=fft(y)
    fft_y=abs(fft_y)
    fft_y=fft_y/len(x)
    print(sample_rate, len(x))
    fft_x=np.linspace(0, sample_rate-1, len(x))

    plt.subplot(614)
    plt.plot(fft_x,fft_y)


    yj = y * c

    fft_yj=fft(yj)
    fft_yj=abs(fft_yj)
    fft_yj=fft_yj/len(x)

    # 滤波 fft方式
    filter_y1 = copy.deepcopy(fft_yj)
    filter_y1 = filter_y1 * len(x)

    for i in range(len(x)):
        if (i >= 8000):
            filter_y1[i] = 0;
    
    for i in range(int(len(x)/2)):
        if (i > 50):
            filter_y1[i] = 0;
    


    filter_y1_src = ifft(filter_y1);
    filter_y1_src = filter_y1_src.real * 2;

    plt.subplot(615)
    plt.plot(x,filter_y1_src)


    fft_y=fft(filter_y1_src)
    fft_y=abs(fft_y)
    fft_y=fft_y/len(x)

    plt.subplot(616)
    plt.plot(fft_x,fft_y)


    plt.show();

    return (x,y);

# 采样率
if __name__=="__main__":
    #x,y = gen_iqtest2(1,1,16000)
    x,y = gen_am(1,1,16000)