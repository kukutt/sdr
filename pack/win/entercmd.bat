set PATH=.\rtl-sdr-64bit-20210131\;.\ffmpeg-18639\;%PATH%
echo "rtl_fm -f 73.3e6 -s 200000 -r 48000 - | ffplay -f s16le -ar 48000  -i -"
echo "rtl_fm -M fm -f 73.3e6 -s 200000 -r 48000 - | ffmpeg -f s16le -ar 48000 -y -i - test.wav"
echo "rtl_fm -M am -f 73.3e6 -s 200000 -r 48000 - | ffmpeg -f s16le -ar 48000 -y -i - test.wav"
echo "rtl_fm -M usb -f 73.3e6 -s 200000 -r 48000 - | ffmpeg -f s16le -ar 48000 -y -i - test.wav"
echo "rtl_fm -M lsb -f 73.3e6 -s 200000 -r 48000 - | ffmpeg -f s16le -ar 48000 -y -i - test.wav"
echo "rtl_fm -f 73.3e6 -s 200000 -r 48000 aa.pcm"
cmd