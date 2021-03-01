import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft,fftfreq,hilbert,ihilbert
from scipy import signal
import scipy
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
    sample = 480000         # 采样率
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
    # tune
    if (mode == "tune"):
        modeok = 1;
        for iii in range(0,len(arr)):
            showjd(iii, arr)
            iq[int(iii*2)] = 127;
            iq[int(iii*2)+1] = 0
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
        harr = hilbert(arr)
        print(arr.min(), arr.max(), harr.min(), harr.max())

        '''
        plt.subplot(211)
        plt.plot(arr[0:50000], label=u"arr")
        plt.subplot(212)
        plt.plot(harr[0:50000], label=u"harr")
        plt.show()
        '''
        

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
        print("hackrf_transfer -f 434000000 -s %d -x 20 -R -t %s" % (sample, outfile))
        #print("sudo sendiq -s %d -f 434e6 -t u8 -l -i %s" % (sample, outfile))
    else:
        print("mode error", mode)

def iq_sim():
    filename="../c/aaa.iq"
    sample = 192000         # 采样率 192000
    totalsample = 0         # 总样本
    carrier_freq = 20000    # 载波频率
    arr= np.fromfile(filename, dtype=np.int8) #np.int8 np.float32 np.float64
    i = arr[0::2]
    q = arr[1::2]
    totalsample = len(i)
    x=np.linspace(0, totalsample/sample, totalsample)


    carrier_I = 500 * np.cos(2 * np.pi * x * carrier_freq);
    carrier_Q = 500 * np.sin(2 * np.pi * x * carrier_freq);


    plt.figure(filename)
    plt.subplot(211)
    plt.plot(x[192000:193000], i[192000:193000]);
    plt.subplot(212)
    plt.plot(x[192000:193000], q[192000:193000]);
    plt.show()

    out = i*carrier_I + q*carrier_Q
    iqfns.showfft(sample, i)
    iqfns.showfft(sample, q)
    iqfns.showfft(sample, out)

def make_cos():
    filename="cos.wav"
    sample = 48000           # 采样率
    totalsample = 480000     # 总样本
    signal_freq = 1000       # 信号
    x=np.linspace(0, totalsample/sample, totalsample)
    signal = 30000 * np.cos(2 * np.pi * x * signal_freq);
    #iqfns.showfft(sample,signal)
    iqfns.writewav(filename, sample, signal)

def show_cos():
    filename="F:\\ram\\rtl_sdr\\test.wav"
    sample = 48000           # 采样率
    signal = iqfns.readwav(filename, sample)
    iqfns.showfft(sample,signal)

def testtest2():
    t = np.arange(2*np.pi,2*np.pi+1,1/1024)
    t = t[1:]
    x = np.cos(10*t*2*np.pi)
    h = (1/(np.pi*t))

    fx = np.array([1,4,3,6,2,3,1,4,5,3,4])
    gx = np.array([0,0,0,0.05,0.8,1,0.2,0.01,0,0,0])
    print(len(fx), len(gx))
    print(np.convolve(fx,gx, 'same'))

    H_conv = np.convolve(x,h,'same')
    plt.subplot(211)
    plt.title('src', y = 0)
    plt.plot(t,x)

    plt.subplot(212)
    plt.title("conv", y = 0)
    plt.plot(t,H_conv)
    plt.show()

def fftlearn():
    fs = 1000
    t = np.arange(0,1+(1/fs),1/fs)
    x = 10*np.sin(2*t*2*np.pi)
    #fftx = np.fft.fftshift(np.fft.fft(x) / t.shape[0])
    fftx = (np.fft.fft(x) / t.shape[0])
    #fftt = np.linspace(-1, 1, t.shape[0]) * (fs / 2)

    #print(t.shape[0], len(t), len(fftt))

    fftt = np.linspace(0,fs,fs+1)
    ffta = np.abs(fftx)
    fftp = np.angle(fftx)

    # 原函数
    plt.subplot(311)
    plt.plot(t, x)
    plt.subplot(312)
    plt.plot(fftt[0:10], ffta[0:10])
    plt.subplot(313)
    plt.plot(fftt[0:10], fftp[0:10])
    plt.show()

    print(ffta[0:10], fftp[0:10])

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
