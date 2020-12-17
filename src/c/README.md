gcc test.c -I ../../run/include/libhackrf/ ../../run/lib/libhackrf.a -lusb-1.0 -lpthread
gcc main.c -I ../../run/include/libhackrf/ ../../run/lib/libhackrf.a -lusb-1.0 -lpthread


# 测试
tr '\000' '\377' < /dev/zero | dd of=tt.iq bs=1024 count=100
hackrf_transfer -t /dev/zero -f 100000000 -s 10000000
