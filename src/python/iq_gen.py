import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft,fftfreq,hilbert,ihilbert
from scipy import signal
import sys
import time
import datetime
import wave
import os
import iq as iqfns

def showjd(iii, arr):
    if (0 == (iii % 1000000)):
        print(iii, len(arr), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

# ## ffmpeg 生成pcm数据
# ffmpeg -i sin.wav -acodec pcm_s16le -ac 1 -ar 2000000 -f f32le  output2.pcm
# ffmpeg -i canon.mp3 -acodec pcm_s16le -ac 1 -ar 2000000 -f f32le -ss 00:00:10 -to 00:00:20 output2.pcm
# ## pcm 转 wav
# ffmpeg -acodec pcm_s16le -ac 1 -ar 2000000 -f f32le -i output2.pcm  output2.wav
# ## MP3 转 wav
# ffmpeg -i canon.mp3 -ac 1 -ar 2000000 -ss 00:00:10 -to 00:00:20 output2.wav
# 生成iq格式的fm
# hackrf_transfer -f 73300000 -s 2000000 -x 20 -R -t test.iq
def iq_gen(mode):
    infile=sys.argv[3]
    outfile=sys.argv[4]
    sample = 2000000        # 采样率
    totalsample = 0         # 总样本

    # wav 音频数据
    if infile.endswith(".wav"):
        arr = iqfns.readwav(infile, sample)
    else:    
        arr= np.fromfile(infile, dtype=np.int16)
    totalsample = len(arr)
    x=np.linspace(0, totalsample/sample, totalsample)

    arr = arr.astype(np.float64);
    iq = np.ones(len(arr)*2).astype(np.float64)
    arr = iqfns.normalize(arr, 1);
    arr = arr * 0.8
    
    '''
    arr = np.ones(20000000).astype(np.float64) * 0.9;
    iq = np.ones(len(arr)*2).astype(np.float64)
    '''

    print("mode =", mode);
    modeok = 0;
    # FM
    if (mode == "fm"):
        modeok = 1;
        fs = 75000;
        devation = (2 * np.pi * (fs)) / sample;
        ph = 0.0;
        for iii in range(0, len(arr)):
            showjd(iii, arr)
            ph = ph + (devation * arr[iii]);
            while ph > 2 * np.pi :
                ph = ph - 2 * np.pi;
            while ph < 2 * np.pi * (-1) :
                ph = ph + 2 * np.pi;
            iq[int(iii*2)] = 127 * np.cos(ph)
            iq[int(iii*2)+1] = 127 * np.sin(ph)
    # AM
    if (mode == "am"):
        modeok = 1;
        amtmp = 0.0
        for iii in range(0,len(arr)):
            showjd(iii, arr)
            amtmp =(arr[iii] + 1) * 0.5
            iq[int(iii*2)] = 127 * amtmp;
            iq[int(iii*2)+1] = 0
    # usb/lsb/dsb
    if (mode == "usb") or (mode == "lsb") or (mode == "dsb"):
        modeok = 1;
        harr = hilbert(arr) * (-1)
        print(arr.min(), arr.max(), harr.min(), harr.max())

        
        plt.subplot(211)
        plt.plot(arr[0:50000], label=u"arr")
        plt.subplot(212)
        plt.plot(harr[0:50000], label=u"harr")
        plt.show()
        

        for iii in range(0,len(arr)):
            showjd(iii, arr)
            iq[int(iii*2)] = 127 * arr[iii]
            if (mode == "usb"):
                iq[int(iii*2)+1] = -127 * harr[iii]
            elif (mode == "lsb"):
                iq[int(iii*2)+1] = 127 * harr[iii]
            else:
                iq[int(iii*2)+1] = 0;

    if (modeok == 1):
        file = open(outfile, "wb")
        y_data=iq.astype(np.int8).tobytes()
        file.write(y_data)
        file.close()
        print("hackrf_transfer -f 73300000 -s 2000000 -x 20 -R -t %s" % (outfile))
    else:
        print("mode error", mode)

def iq_see():
    filename="lsb_cos_880.iq"
    sample = 2000000        # 采样率
    totalsample = 0         # 总样本
    arr= np.fromfile(filename, dtype=np.int8)
    i = arr[0::2]
    q = arr[1::2]
    totalsample = len(i)
    x=np.linspace(0, totalsample/sample, totalsample)

    plt.plot(x[0:10000], i[0:10000]);
    plt.show()
    plt.plot(x[0:10000], q[0:10000]);
    plt.show()

    iqfns.showfft(sample, i)
    iqfns.showfft(sample, q)

def hilbert_test():
    arr,sample_rate = iqfns.readwav("output3.wav", 48000)
    arr_h = hilbert(arr)
    print(arr.dtype, arr_h.dtype, arr.min(), arr.max(), arr_h.min(), arr_h.max())
    iqfns.writewav("arr.wav", sample_rate, arr)
    iqfns.writewav("arr_h.wav", sample_rate, arr_h)


# 单音单边带测
def ssb_test():
    sample = 200000           # 采样率
    totalsample = 200000      # 总样本
    carrier_freq = 20000      # 载波频率
    signal_freq = 200         # 信号
    duration = 3 * int(sample/signal_freq)  # 一个周期多少个点
    x=np.linspace(0, totalsample/sample, totalsample)


    carrier_I =   np.cos(2 * np.pi * x * carrier_freq);
    carrier_Q =   np.sin(2 * np.pi * x * carrier_freq);
    signal_I =    np.cos(2 * np.pi * x * signal_freq);

    # signal_Q =    np.cos(2 * np.pi * x * signal_freq) * 0;
    signal_Q = hilbert(signal_I) * (-1)
    # signal_Q = hilbert(signal_I) * (-1) * (-1)
    output = carrier_I * signal_I + carrier_Q * signal_Q;

    plt.subplot(411)
    plt.plot(x[0:duration], carrier_I[0:duration]);
    plt.subplot(412)
    plt.plot(x[0:duration], signal_I[0:duration]);
    plt.subplot(413)
    plt.plot(x[0:duration], signal_Q[0:duration]);
    plt.subplot(414)
    plt.plot(x[0:duration], output[0:duration]);
    plt.show()

    iqfns.showfft(sample, output)

def make_cos():
    filename="cos.wav"
    sample = 2000000           # 采样率
    totalsample = 20000000     # 总样本
    signal_freq = 880          # 信号
    x=np.linspace(0, totalsample/sample, totalsample)
    signal = 30000 * np.cos(2 * np.pi * x * signal_freq);
    iqfns.showfft(sample,signal)
    iqfns.writewav(filename, sample, signal)

def show_cos():
    filename="F:\\ram\\rtl_sdr\\test.wav"
    sample = 48000           # 采样率
    signal = iqfns.readwav(filename, sample)
    iqfns.showfft(sample,signal)

if __name__=="__main__":
    if (2 > len(sys.argv)):
        print("iq_see [iqfile]")
        print("iq_gen [am/fm/dsb/usb/lsb] [wavfile] [iqfile]")
        print("hilbert_test")
        sys.exit()
    print(sys.argv[1])
    try:
        sys.argv[2]
    except:
        eval(sys.argv[1])()
    else:
        eval(sys.argv[1])(sys.argv[2])
