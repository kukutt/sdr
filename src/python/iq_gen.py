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
import iq as iqfns

# ## ffmpeg 生成pcm数据
# ffmpeg -i sin.wav -acodec pcm_s16le -ac 1 -ar 2000000 -f f32le  output2.pcm
# ffmpeg -i canon.mp3 -acodec pcm_s16le -ac 1 -ar 2000000 -f f32le -ss 00:00:10 -to 00:00:20 output2.pcm
# 
# 生成iq格式的fm
# hackrf_transfer -f 73300000 -s 2000000 -x 20 -R -t test.iq
def iq_gen_fm():
    infile=sys.argv[2]
    outfile=sys.argv[3]
    sample = 2000000        # 采样率
    totalsample = 0         # 总样本

    # wav 音频数据
    arr= np.fromfile(infile, dtype=np.int16)
    totalsample = len(arr)
    x=np.linspace(0, totalsample/sample, totalsample)

    arr = arr.astype(np.float64);
    iq = np.ones(len(arr)*2).astype(np.float64)
    arr = iqfns.normalize(arr, 1);
    arr = arr * 0.9
    

    '''
    arr = np.ones(20000000).astype(np.float64) * 0.9;
    iq = np.ones(len(arr)*2).astype(np.float64)
    '''

    '''
    # AM
    i = iqfns.normalize(i, 127)
    q = q * 0
    for iii in range(0,len(arr)):
        iq[int(iii*2)] = i[iii]
        iq[int(iii*2)+1] = q[iii]
    '''

    # FM
    fs = 75000;
    devation = (2 * np.pi * (fs)) / sample;
    ph = 0.0;
    for iii in range(0,len(arr)):
        ph = ph + (devation * arr[iii]);
        while ph > 2 * np.pi :
            ph = ph - 2 * np.pi;
        while ph < 2 * np.pi * (-1) :
            ph = ph + 2 * np.pi;
        iq[int(iii*2)] = 127 * np.cos(ph)
        iq[int(iii*2)+1] = 127 * np.sin(ph)
    file = open(outfile, "wb")
    y_data=iq.astype(np.int8).tobytes()
    file.write(y_data)
    file.close()

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


if __name__=="__main__":
    if (2 > len(sys.argv)):
        print("iq_see [iqfile]")
        print("iq_gen_fm [wavfile] [iqfile]")
        sys.exit()
    print(sys.argv[1])
    eval(sys.argv[1])()