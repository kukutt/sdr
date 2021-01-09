#from thinkdsp import CosSignal, SinSignal
import matplotlib.pyplot as plt
import thinkdsp

def test1():
    cos_sig = thinkdsp.CosSignal(freq=440, amp=1.0, offset=0)
    sin_sig = thinkdsp.SinSignal(freq=880, amp=0.5, offset=0)

    mix = cos_sig + sin_sig;

    wave = mix.make_wave(duration=10, start=0, framerate=16000)
    wave.normalize() # 归一化
    wave.apodize() # 渐入渐出
    wave.plot()
    plt.show()
    wave.write(filename='output.wav')

    # 显示原波形
    violin_wave = thinkdsp.read_wave('output.wav')
    segment = violin_wave.segment(start=0, duration=2/440)
    segment.plot()
    plt.show()

    # 频谱
    spectrum = violin_wave.make_spectrum()
    spectrum.plot()
    plt.show()

    # 低通

    spectrumlow=spectrum.copy()
    spectrumlow.low_pass(cutoff=600, factor=0.01)
    spectrumlow.plot()
    plt.show()

    violin_wave = spectrumlow.make_wave()
    segment = violin_wave.segment(start=0, duration=2/440)
    segment.plot()
    plt.show()



    # 高通
    spectrumhigh=spectrum.copy()
    spectrumhigh.high_pass(cutoff=600, factor=0.01)
    spectrumhigh.plot()
    plt.show()

    violin_wave = spectrumhigh.make_wave()
    segment = violin_wave.segment(start=0, duration=2/440)
    segment.plot()
    plt.show()


def test2():
    cos_sig = thinkdsp.CosSignal(freq=440, amp=1.0, offset=0)
    sin_sig = thinkdsp.SinSignal(freq=800, amp=0.5, offset=0)

    mix = cos_sig + sin_sig;

    wave = mix.make_wave(duration=2, start=0, framerate=16000)
    wave.normalize() # 归一化
    wave.write(filename='play3.wav')
    wave.apodize() # 渐入渐出
    wave.write(filename='play4.wav')

def test3():
    wave = thinkdsp.read_wave("ThinkDSP-master/code/170255__dublie__trumpet.wav")
    wave.plot()
    plt.show()


    spectrum = wave.make_spectrum()
    spectrum.plot(high=1000)
    print(spectrum.peaks()[:30]);
    plt.show()

if __name__=="__main__":
    test3()