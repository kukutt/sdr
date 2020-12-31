@echo off
echo conda env list
echo conda activate xxx 
echo conda deactivate
echo conda create -n xxxx python=3.7.5
echo conda remove -n xxxx --all
echo conda list
echo "pip --proxy=http://10.12.32.20:7777/ install -i https://mirrors.aliyun.com/pypi/simple/"
echo "pip  install -i https://mirrors.aliyun.com/pypi/simple/"
@echo on
call d:\Users\admin\anaconda3\Scripts\activate.bat
call conda activate dsp
cmd
