# mp3 to wav
wav head 32 byte
ffmpeg -codecs
ffmpeg -i canon.mp3 -acodec pcm_s16le -ac 2 -ar 36000 output1.wav
ffmpeg -i canon.mp3 -acodec pcm_s16le -ac 2 -ar 36000 -ss 00:00:01 -t 00:00:02 output1.wav
