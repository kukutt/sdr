C_FLAG := -I $(PWD)/../../run/include/ -Wno-strict-aliasing
LD_FLAG := -lm $(PWD)/../../run/lib/libhackrf.a -lusb-1.0 -lpthread

all:
	gcc $(C_FLAG) -o fm_send hackrf_WBFM_Transmit/HackRF_WBFM_Transmit.c $(LD_FLAG)
clean:
	rm fm_send

