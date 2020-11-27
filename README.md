# hackrf-host
sudo apt-get install build-essential libusb-1.0-0-dev pkg-config libfftw3-dev
git clone https://github.com/mossmann/hackrf
wget https://github.com/mossmann/hackrf/releases/download/v2018.01.1/hackrf-2018.01.1.tar.xz
cmake -DCMAKE_INSTALL_PREFIX=$PWD/../../../run -DUDEV_RULES_PATH=$PWD/../../../etc/udev/rules.d/ ../

# gnuradio
sudo apt install git cmake g++ libboost-all-dev libgmp-dev swig python3-numpy python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins python3-zmq python3-scipy
wget https://www.gnuradio.org/releases/gnuradio/gnuradio-3.8.0.0.tar.gz
cmake -DCMAKE_INSTALL_PREFIX=$PWD/../../run ../
