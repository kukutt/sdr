gcc test.c -I ../../run/include/libhackrf/ ../../run/lib/libhackrf.a -lusb-1.0 -lpthread
gcc main.c -I ../../run/include/libhackrf/ ../../run/lib/libhackrf.a -lusb-1.0 -lpthread

## 测速
hackrf_transfer -r /dev/zero -s 20000000
hackrf_transfer -s /dev/zero -s 20000000

# FM 转 iq例子
git clone https://github.com/aricwang88/hackrf_WBFM_Transmit.git

# 格式转换
ffmpeg -i xx.mp3 -acodec pcm_s16le -ac 2 -ar 2000000 output2.wav
ffmpeg -i xx.mp3 -acodec pcm_s16le -ac 2 -ar 2000000 -ss 00:00:10 -to 00:00:25 output2.wav
ffmpeg -i xx.mp3 -acodec pcm_s16le -ac 1 -ar 2000000 -f f32le  output2.pcm
ffmpeg -i xx.mp3 -acodec pcm_s16le -ac 1 -ar 2000000 output2.wav

# 测试
tr '\000' '\377' < /dev/zero | dd of=tt.iq bs=1024 count=100
hackrf_transfer -t /dev/zero -f 100000000 -s 10000000
