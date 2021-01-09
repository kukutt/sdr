build in Ubuntu 18.04.5 LTS

# hackrf-host
sudo apt-get install build-essential cmake libusb-1.0-0-dev pkg-config libfftw3-dev   
git clone https://github.com/mossmann/hackrf  
wget https://github.com/mossmann/hackrf/releases/download/v2018.01.1/hackrf-2018.01.1.tar.xz  
cmake -DCMAKE_INSTALL_PREFIX=$PWD/../../../run -DUDEV_RULES_PATH=$PWD/../../../run/etc/udev/rules.d/ ../  

# gnuradio

## 3.8
sudo apt install git cmake g++ libboost-all-dev libgmp-dev swig python3-numpy python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins python3-zmq python3-scipy  
wget https://www.gnuradio.org/releases/gnuradio/gnuradio-3.8.0.0.tar.gz  

## 3.7
sudo apt install cmake git g++ libboost-all-dev python-dev python-mako python-numpy python-wxgtk3.0 python-sphinx python-cheetah swig libzmq3-dev libfftw3-dev libgsl-dev libcppunit-dev doxygen libcomedi-dev libqt4-opengl-dev python-qt4 libqwt-dev libsdl1.2-dev libusb-1.0-0-dev python-gtk2 python-lxml pkg-config python-sip-dev  
wget https://www.gnuradio.org/releases/gnuradio/gnuradio-3.7.10.2.tar.gz

cmake -DCMAKE_INSTALL_PREFIX=$PWD/../../run ../  


# gr-osmosdr
git clone git://git.osmocom.org/gr-osmosdr  
wget https://github.com/osmocom/gr-osmosdr/archive/v0.1.5.tar.gz  
wget https://github.com/osmocom/gr-osmosdr/archive/v0.2.2.tar.gz  
cmake -DCMAKE_INSTALL_PREFIX=$PWD/../../run ../  

# gqrx
sudo apt-get install qt5-qmake qtbase5-dev pkg-config libqt5svg5-dev  
git clone https://github.com/csete/gqrx.git  
wget https://github.com/csete/gqrx/archive/v2.14.1.tar.gz  
cmake -DCMAKE_INSTALL_PREFIX=$PWD/../../run ../  


# test
hackrf_transfer -r /dev/stdout -f 315000000 -a 1 -g 16 -l 32 -s 8000000  

# rtl-sdr
sudo apt install build-essential cmake libusb-1.0-0-dev  pkg-config
git clone https://github.com/osmocom/rtl-sdr
git clone git://git.osmocom.org/rtl-sdr
cmake -DCMAKE_INSTALL_PREFIX=$PWD/../../run ../
sudo modprobe -r dvb_usb_rtl28xxu
sudo cp ./pack/blacklist_rtlsdr.conf /etc/modprobe.d/
sudo cp ./rtl-sdr-0.6.0/rtl-sdr.rules /etc/udev/rules.d/
 
## fm test
timeout 2 rtl_fm -d 0 -g 49 -M usb -s 32000  -r 32000 -F 1 -f 50.293M outfile.raw
timeout 2 rtl_fm -M wbfm -s 480000 -r 48000 -f 100.0M outfile.raw
rtl_fm -M wbfm -s 480000 -r 48000 -f 73.3M - | ffplay -f s16le -ar 48000 -i -
rtl_fm -M wbfm -s 480000 -r 48000 -f 73.3M - | hexdump -C

## demo
git clone https://github.com/antirez/dump1090.git
sudo apt install build-essential cmake libusb-1.0-0-dev  pkg-config librtlsdr-dev
./dump1090 --interactive --net
