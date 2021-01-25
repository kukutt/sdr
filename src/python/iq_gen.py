import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft,fftfreq,hilbert
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
# 生成iq格式的fm
# hackrf_transfer -f 73300000 -s 2000000 -x 20 -R -t test.iq
def iq_gen(mode):
    infile=sys.argv[3]
    outfile=sys.argv[4]
    sample = 2000000        # 采样率
    totalsample = 0         # 总样本

    # wav 音频数据
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
        harr = hilbert(arr)
        print(arr.min(), arr.max(), harr.min(), harr.max())

        '''
        plt.subplot(211)
        plt.plot(arr[20000:50000], label=u"arr")
        plt.subplot(212)
        plt.plot(harr[20000:50000], label=u"harr")
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
        print("hackrf_transfer -f 73300000 -s 2000000 -x 20 -R -t %s" % (outfile))
    else:
        print("mode error", mode)

def iq_see():
    infile=sys.argv[2]
    sample = 2000000        # 采样率
    totalsample = 0         # 总样本
    arr= np.fromfile(infile, dtype=np.int8)
    i = arr[0::2]
    q = arr[1::2]
    totalsample = len(i)
    x=np.linspace(0, totalsample/sample, totalsample)

    plt.plot(x, i);
    plt.show()
    plt.plot(x, q);
    plt.show()

    iqfns.showfft(sample, i)
    iqfns.showfft(sample, q)

def test():
    # wav 音频数据
    arr = np.fromfile("output2.pcm", dtype=np.int16)
    arr = arr.astype(np.float64)
    harr = hilbert(arr)

    file = open("arr.pcm", "wb")
    y_data=arr.astype(np.int16).tobytes()
    file.write(y_data)
    file.close()

    file = open("harr.pcm", "wb")
    y_data=harr.astype(np.int16).tobytes()
    file.write(y_data)
    file.close()

if __name__=="__main__":
    if (2 > len(sys.argv)):
        print("iq_see [iqfile]")
        print("iq_gen [am/fm/dsb/usb/lsb] [wavfile] [iqfile]")
        print("test")
        sys.exit()
    print(sys.argv[1])
    try:
        sys.argv[2]
    except:
        eval(sys.argv[1])()
    else:
        eval(sys.argv[1])(sys.argv[2])