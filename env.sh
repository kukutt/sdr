#!/bin/bash
# 获取工作路径
homePath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
workPath=$PWD
echo work dir [$homePath] [$workPath]

export PATH=$homePath/run/bin:$PATH
export LD_LIBRARY_PATH=$homePath/run/lib:$LD_LIBRARY_PATH
export PKG_CONFIG_PATH=$homePath/run/lib/pkgconfig:$PKG_CONFIG_PATH
export PYTHONPATH=$PYTHONPATH:$homePath/run/lib/python3/dist-packages/:$homePath/run/lib/python3.6/dist-packages/
