#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import os
import numpy as np
import matplotlib.pyplot as plt
#import scipy

from scipy.fftpack import fft,ifft,fftfreq,hilbert,ihilbert

#from matplotlib.font_manager import fontManager
def plot_dft(x,y,z,Fs,N):
    fig,axes = plt.subplots(nrows=4,ncols=1,figsize=(12,18))
    line1, = axes[0].plot(x,'b')  #the source signal
    line2, = axes[1].plot([Fs/N*i for i in range(int(N/2))],[abs(com_y) for com_y in y[0:int(N/2)]],'r')
    line3, = axes[2].plot([Fs/N*i for i in range(int(N/2))],[-math.atan(com_y.imag/com_y.real) if abs(com_y)>0.1 else 0 for com_y in y[0:int(N/2)]],'r')
    line4, = axes[3].plot([aaa.real for aaa in z[0:len(z)]],'b')  #the source signal
    #fig.savefig('DFT_simulation.png',dpi=500,bbox_inches='tight')
    plt.show()
    plt.close()

def dft(x):
    y = []
    N = len(x)
    for k in range(N):
        #contain the basis exp(-j*2*pi/N*k*n) and the projection weight
        basis = [complex(math.cos(2*math.pi/N*k*n), math.sin(2*math.pi/N*k*n*(-1))) for n in range(N)]
        y.append(np.dot(x,np.transpose(basis)))
    return y

def idft(y):
    z = []  #the result of IDFT
    N = len(y)
    for k in range(N):
        #contain the basis exp(j*2*pi/N*k*n) and the projection weight
        basis = [complex(math.cos(2*math.pi/N*k*n),math.sin(2*math.pi/N*k*n)) for n in range(N)]
        z.append(np.dot(y,np.transpose(basis))/N)
    return z

def dft_test1():
    Fs = 8000#sample rate
    N = 800 #sample dots' number
    f1 = 1000  #1st component in signal
    x1 = [np.cos(2*math.pi*f1/Fs*n+math.pi/8) for n in range(200)]
    f2 = 2000  #2nd component in signal
    x2 = [np.cos(2*math.pi*f2/Fs*n-math.pi/4)*2 for n in range(300)]
    f3 = 3000  #3rd component in signal
    x3 = [np.cos(2*math.pi*f3/Fs*n+math.pi/2)*3 for n in range(300)]
    x = x1+x2+x3
    y = dft(x)
    z = idft(y)
    plot_dft(x,y,z,Fs,N)


def dft_test2():
    Fs = 8000#sample rate
    N = 800 #sample dots' number
    f1 = 1000  #1st component in signal
    x1 = [np.cos(2*math.pi*f1/Fs*n+math.pi/8) for n in range(N)]
    f2 = 2000  #2nd component in signal
    x2 = [np.cos(2*math.pi*f2/Fs*n-math.pi/4)*2 for n in range(N)]
    f3 = 3000  #3rd component in signal
    x3 = [np.cos(2*math.pi*f3/Fs*n+math.pi/2)*3 for n in range(N)]
    x = [x1[n]+x2[n]+x3[n] for n in range(N)]
    y = dft(x)
    z = idft(y)
    plot_dft(x,y,z,Fs,N)


def dft_test3():
    src1 = [complex(1,0),complex(3,0),complex(2,0),complex(5,0),complex(8,0),complex(4,0),complex(1,0),complex(3,0),\
    complex(2,0),complex(5,0),complex(8,0),complex(4,0),complex(1,0),complex(3,0),complex(2,0),complex(5,0)]
    dst = dft(src1)
    src2 = idft(dst)
    print(src1)
    print(dst)
    print(src2)

def fft_test():
    for ttt in range(100):
        try:
            os.remove("src.cp")
            os.remove("dst.cp")
            print("文件删除完毕")
        except(FileNotFoundError):
            print("文件不存在")
        os.system("./ft")


        src = np.fromfile("src.cp", dtype=np.complex64) #np.int8 np.float32 np.float64
        dstc = np.fromfile("dst.cp", dtype=np.complex64)
        dstpy = fft(src)
        #print(dstpy)
        #print(dstc)
        for i in range(len(dstc)):
            if (np.abs(np.abs(dstc[i]) - np.abs(dstpy[i])) > 0.002):
                print("error abs", ttt, i, np.abs(dstc[i]), np.abs(dstpy[i]))
                os._exit(-1);
            if (np.abs(np.angle(dstc[i]) - np.angle(dstpy[i])) > 0.001):
                print("error angle", ttt, i, np.angle(dstc[i]) , np.angle(dstpy[i]))
                os._exit(-1);

    print("test ok\r\n")

def fft_test1():
    for ttt in range(100):
        src = 100 * np.random.random(4096) + np.random.random(4096) * 100j
        src = src.astype(np.complex64)
        src.tofile("src.bin")
        try:
            os.remove("dst.bin")
        except:
            pass
        os.system("./ft")
        dstfft = np.fromfile("dst_fft.bin", dtype=np.complex64)
        dstdft = np.fromfile("dst_dft.bin", dtype=np.complex64)
        dstpy = fft(src)
        #print(ttt, src[0], dstpy[0])

        for i in range(len(dstfft)):
            if (np.abs(np.abs(dstfft[i]) - np.abs(dstpy[i])) > 0.002):
                print("error abs", ttt, i, np.abs(dstfft[i]), np.abs(dstpy[i]))
                os._exit(-1);
            if (np.abs(np.angle(dstfft[i]) - np.angle(dstpy[i])) > 0.001):
                print("error angle", ttt, i, np.angle(dstfft[i]) , np.angle(dstpy[i]))
                os._exit(-1);

        for i in range(len(dstdft)):
            if (np.abs(dstdft[i]) > 100):
                difffff = 1;
            elif (np.abs(dstdft[i]) > 1):
                difffff = 0.1;
            else:
                difffff = 0.001
            if (np.abs(np.abs(dstdft[i]) - np.abs(dstpy[i])) > difffff):
                print("error abs", ttt, i, np.abs(dstdft[i]), np.abs(dstpy[i]))
                os._exit(-1);
            if (np.abs(np.angle(dstdft[i]) - np.angle(dstpy[i])) > 0.005):
                print("error angle", ttt, i, np.angle(dstdft[i]) , np.angle(dstpy[i]))
                os._exit(-1);
    print("test ok\r\n")


def iq_sim():
    filename="./haa.iq"
    sample = 1000           # 采样率 192000
    totalsample = 0         # 总样本
    arr= np.fromfile(filename, dtype=np.float64) #np.int8 np.float32 np.float64
    i = arr[0::2]
    q = arr[1::2]
    totalsample = len(i)
    x=np.linspace(0, totalsample/sample, totalsample)
    plt.plot(x, i);
    plt.show()
    plt.plot(x, q);
    plt.show()

if __name__ == "__main__":
    #iq_sim()
    #dft_test1()
    #dft_test2()
    #dft_test3()
    #fft_test()
    fft_test1()