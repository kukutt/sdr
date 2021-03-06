import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft,fftfreq
from scipy import signal
import sys
import time
import thinkdsp
import wave
import os


def normalize(arr, val):
    amin, amax = arr.min(), arr.max()
    print("min=", amin, "max=", amax)
    if (amin == amax):
        a = arr * 0;
    else:
        a = ((arr-amin)/(amax-amin)) - 0.5
        a = a * val * 2;
    return a;

def readwav(filename, sample):
    file=wave.open(filename,'rb')
    num_frame = file.getnframes()
    num_channel=file.getnchannels()
    framerate=file.getframerate()
    num_sample_width=file.getsampwidth()
    print('帧数',num_frame,'  声道数',num_channel,'  帧速率',framerate,'  实例的比特宽度，即每一帧的字节数', num_sample_width)
    str_data = file.readframes(num_frame)
    file.close()
    wave_data = np.fromstring(str_data, dtype = np.short)
    wave_data = wave_data.astype(np.float64)
    print(len(wave_data))
    repeatcount = sample/framerate;
    wave_data = wave_data.repeat(repeatcount)
    print(len(wave_data))
    return wave_data

def writewav(filename, sample_rate, arr):
    file=wave.open(filename,'wb')
    file.setnchannels(1)#设置通道数
    file.setsampwidth(2)#设置采样宽
    file.setframerate(sample_rate)#设置采样
    file.setcomptype('NONE','not compressed')#设置采样格式  无压缩

    y_data=arr.astype(np.int16).tobytes()#将类型转为字节
    file.writeframes(y_data)
    file.close()

def showfft(sample_rate, arr):
    fft_y=fft(arr)
    fft_y=abs(fft_y)
    fft_y=fft_y/len(arr)
    fft_x=np.linspace(0, sample_rate, len(arr)) 
    print(len(fft_x), len(fft_y), len(arr))
    plt.plot(fft_x, fft_y)
    plt.show()

def filter_data(data, highcut, fs):
    fft_y = fft(data)
    freq = np.linspace(0, fs, len(data)) 
    x = freq[:int(len(data)/2)] 
    for i in range(len(x)):
        if x[i] > highcut: # cut off all frequencies higher than 0.005
            fft_y[i] = 0.0
            fft_y[int(len(data)) - i - 1] = 0.0
    return ifft(fft_y).real

# 模拟iq调制解调
# 调制:s(t) = a*cos(wt) - b*sin(wt)
# 解调:a = 积分(s(t)cos(wt), 载波周期)
# 解调:b = 积分(-s(t)sin(wt), 载波周期)
# 解调:低通滤波器
# https://wenku.baidu.com/view/7f2633764935eefdc8d376eeaeaad1f34793111b
def iq_test():
    sample = 20000000        # 采样率
    totalsample = 20000000  # 总样本
    carrier_freq = 2000000   # 载波频率
    duration = int(sample/carrier_freq)  # 一个周期多少个点
    x=np.linspace(0, totalsample/sample, totalsample)

    # 信号生成
    '''
    ## 固定常数信号
    signal_I = 5
    signal_Q = 9
    '''
    
    ## 正弦波信号
    '''
    signal_I = np.cos(2 * np.pi * x * 440);
    signal_Q = np.cos(2 * np.pi * x * 700);
    '''

    ## 音频信号
    
    arr= np.fromfile(sys.argv[1], dtype=np.int16)#按8位数据读取iq数据
    signal_I = arr[0:20000000]
    signal_Q = arr[10000000:30000000]
    signal_I = signal_I.astype(np.float64)
    signal_Q = signal_Q.astype(np.float64)
    print(signal_I.dtype, x.dtype)
    signal_I = normalize(signal_I, 30000)
    signal_Q = normalize(signal_Q, 30000)
    #writewav("signal_I_src.wav", 160000, signal_I)
    #writewav("signal_Q_src.wav", 160000, signal_Q)
    

    ## 载波生成
    rf_cos = 10 * np.cos(2 * np.pi * x * carrier_freq)
    rf_sin = 10 * np.sin(2 * np.pi * x * carrier_freq)

    # 调制
    wave = (signal_I * rf_cos) + (signal_Q * rf_sin);

    # 解调
    new_I = wave * rf_cos
    new_Q = wave * (-1) * rf_sin

    #showfft(sample, new_I)
    #showfft(sample, new_Q)

    '''
    resize_x=np.linspace(0, totalsample/sample, int(totalsample/duration))
    resize_I = np.zeros(int(len(new_I)/duration)) 
    resize_Q = np.zeros(int(len(new_I)/duration)) 
    print(duration, len(new_I), len(resize_I))
    for iii in range(len(resize_I)):
        resize_I[iii] = np.sum(new_I[int(iii*duration):int((iii+1)*duration)])
    for iii in range(len(resize_Q)):
        resize_Q[iii] = np.sum(new_Q[int(iii*duration):int((iii+1)*duration)])

    resize_I = resize_I / 500;
    resize_Q = resize_Q / 500;

    writewav("signal_I_dst.wav", 16000, resize_I)
    writewav("signal_Q_dst.wav", 16000, resize_Q)
    '''

    resize_x = x
    resize_I = filter_data(new_I, 2000000, sample)
    resize_Q = filter_data(new_Q, 2000000, sample)
    #showfft(sample, resize_I)
    #showfft(sample, resize_Q)

    resize_I = normalize(resize_I, 30000)
    resize_Q = normalize(resize_Q, 30000)

    writewav("signal_I_dst.wav", 160000, resize_I)
    writewav("signal_Q_dst.wav", 160000, resize_Q)

    print(resize_Q.dtype,new_I.dtype)

    '''
    plt.plot(resize_x, resize_I)
    plt.show()

    plt.plot(resize_x, resize_Q)
    plt.show()
    '''


def show_raw_wav():
    sample = 2000000        # 采样率
    totalsample = 0         # 总样本
    carrier_freq = 138000  # 载波频率 通过fft测量


    arr = np.fromfile(sys.argv[1], dtype=np.int8)#按8位数据读取iq数据
    arr = arr[1::2]

    totalsample = len(arr)
    x=np.linspace(0, totalsample/sample, totalsample)


    plt.plot(x, arr)
    plt.show()
    showfft(sample, arr)



# timeout 10 rtl_fm -M raw -s 1008000 -f 73300000 test.iq
# timeout 10 rtl_fm -M am -s 1008000 -f 73300000 iqsingnal_am.iq
def iq_2_signal_rtl_fm_raw():
    sample = 2000000        # 采样率
    totalsample = 0         # 总样本
    carrier_freq = 138000  # 载波频率 通过fft测量
    duration = int(sample/carrier_freq)  # 一个周期多少个点


    arr = np.fromfile(sys.argv[1], dtype=np.int8)#按8位数据读取iq数据

    signal_I=arr[0::2];
    signal_Q=arr[1::2];
    totalsample = len(signal_I)
    x=np.linspace(0, totalsample/sample, totalsample)

    plt.plot(x, signal_I)
    plt.show()

    plt.plot(x, signal_Q)
    plt.show()

    signal_I = normalize(signal_I, 30000)
    signal_Q = normalize(signal_Q, 30000)
    showfft(sample, signal_I)
    showfft(sample, signal_Q)

    resize_I = filter_data(signal_I, carrier_freq, sample)
    resize_Q = filter_data(signal_Q, carrier_freq, sample)

    showfft(sample, resize_I)
    showfft(sample, resize_Q)


    plt.plot(x, resize_I)
    plt.show()

    plt.plot(x, resize_Q)
    plt.show()

# 生成iq数据
# hackrf_transfer -f 73300000 -s 2000000 -x 20 -R -t test.iq
def signal_2_iq_raw():
    sample = 2000000        # 采样率
    totalsample = 20000000  # 总样本

    x=np.linspace(0, totalsample/sample, totalsample)

    # 信号生成
    '''
    ## 固定常数信号
    signal_I = 5.0 * np.ones(len(x));
    signal_Q = -7.0 * np.ones(len(x));
    '''
    
    ## 正弦波信号
    
    signal_I = np.cos(2 * np.pi * x * 440);
    signal_Q = np.sin(2 * np.pi * x * 700) * 0;
    

    ## 音频信号
    '''
    arr= np.fromfile(sys.argv[1], dtype=np.int16)#按8位数据读取iq数据
    signal_I = arr[0:20000000]
    signal_Q = arr[10000000:30000000]
    '''

    plt.plot(signal_I[:10000])
    plt.show()
    plt.plot(signal_Q[:10000])
    plt.show()
    signal_I = normalize(signal_I, 127)
    signal_Q = normalize(signal_Q, 127)
    plt.plot(signal_I[:10000])
    plt.show()
    plt.plot(signal_Q[:10000])
    plt.show()
    iq = np.ones(len(x)*2)
    for i in range(int(len(iq)/2)):
        iq[(i*2)] = signal_I[i];
        iq[(i*2)+1] = signal_Q[i];
    y_data=iq.astype(np.uint8).tobytes()
    fo = open(sys.argv[2], "wb")
    fo.write(y_data)
    fo.close()


def gen_wav():
    #cos_sig = thinkdsp.CosSignal(freq=440, amp=1.0, offset=0)
    sin_sig = thinkdsp.SinSignal(freq=880, amp=0.5, offset=0)

    #mix = cos_sig + sin_sig;
    mix = sin_sig

    wave = mix.make_wave(duration=10, start=0, framerate=2000000)
    wave.normalize() # 归一化
    wave.apodize() # 渐入渐出
    #wave.plot()
    #plt.show()

    segment = wave.segment(start=0, duration=2/440)
    segment.plot()
    plt.show()

    # 频谱
    spectrum = wave.make_spectrum()
    spectrum.plot()
    plt.show()
    wave.write(filename=sys.argv[1])


def show_wav():
    wave = thinkdsp.read_wave(sys.argv[1])

    #wave.normalize() # 归一化
    #wave.apodize() # 渐入渐出

    #segment = wave.segment(start=0, duration=2/440)
    #segment.plot()
    wave.plot()
    plt.show()

    # 频谱
    spectrum = wave.make_spectrum()
    spectrum.plot()
    plt.show()

def show_pcm():
    fs = 48000
    arr= np.fromfile(sys.argv[1], dtype=np.int16)#按8位数据读取iq数据

    x=np.linspace(0, len(arr)/fs, len(arr)) 
    print(arr[0:100])
    print(arr.size)

    plt.plot(x[1000:2000], arr[1000:2000])#绘制实部数据
    plt.show()

    aaa=fft(arr)
    fft_y=abs(aaa)
    fft_y=fft_y/len(arr)
    fft_x=np.linspace(0, fs, len(arr)) 
    print(len(fft_x), len(fft_y), len(arr))
    #plt.savefig("%s_%s_arr.jpg" % (time.strftime("%Y%m%d%H%M%S", time.localtime()), sys.argv[0]))
    plt.plot(fft_x, fft_y)
    plt.show()


def show_iq():
    arr= np.fromfile(sys.argv[1], dtype=np.int16)#按8位数据读取iq数据
    print(arr[0:100])
    arr1=arr[0::2];
    print(arr1[0:100])
    arr2=arr[1::2];
    print(arr2[0:100])
    print(arr.size, arr1.size,arr2.size)
    i = thinkdsp.Wave(arr1, framerate=2000000)
    i.plot()
    plt.show()

    q = thinkdsp.Wave(arr1, framerate=2000000)
    q.plot()
    plt.show()


    spectrum = i.make_spectrum()
    spectrum.plot()
    plt.show()

    spectrum.low_pass(cutoff=100000, factor=0.01)
    spectrum.plot()
    plt.show()
    violin_wave = spectrum.make_wave()
    violin_wave.plot()
    plt.show()

    '''
    real=arr[126500:128000:2]#取部分i数据
    imag=arr[126501:128000:2]#取部分q数据
    d_real=real.astype(np.float32)#数据类型转化，不然8位数据只能显示-127到127.卡了我一天不知道哪里错了
    d_imag=imag.astype(np.float32)
    comx=d_real+d_imag*1j#组成复数
    '''
    '''
    plt.plot(arr1)#绘制实部数据
    plt.show()
    plt.plot(arr2)#绘制实部数据
    plt.show()

    
    aaa=fft(arr1)
    fft_y=abs(aaa)
    fft_y=fft_y/len(arr1)
    plt.savefig("%s_%s_arr1.jpg" % (time.strftime("%Y%m%d%H%M%S", time.localtime()), sys.argv[0]))

    plt.plot(fft_y)
    plt.show()


    aaa=fft(arr2)
    fft_y=abs(aaa)
    fft_y=fft_y/len(arr2)
    plt.savefig("%s_%s_arr2.jpg" % (time.strftime("%Y%m%d%H%M%S", time.localtime()), sys.argv[0]))
    plt.plot(fft_y)
    plt.show()
    '''
    

def iq_test11():
    sample = 200        # 采样率
    totalsample = 400  # 总样本
    carrier_freq = 1   # 载波频率
    duration = int(sample/carrier_freq)  # 一个周期多少个点
    x=np.linspace(0, totalsample/sample, totalsample)

    ## 载波生成
    rf_cos = 10 * np.cos(2 * np.pi * x * carrier_freq)
    rf_sin = 10 * np.sin(2 * np.pi * x * carrier_freq)

    y1 = rf_cos - rf_sin;
    y2 = rf_cos - (0.5 * rf_sin);

    plt.plot(x, rf_cos)
    plt.plot(x, rf_sin)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.show()

if __name__=="__main__":
    #iq_test()
    #gen_wav();
    #show_raw_wav()
    #iq_2_signal_rtl_fm_raw()
    #signal_2_iq_raw()
    iq_test11();