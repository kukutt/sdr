C_FLAG := -I $(PWD)/../../run/include/libhackrf/ -Wno-strict-aliasing
LD_FLAG := -lm $(PWD)/../../run/lib/libhackrf.a -lusb-1.0 -lpthread

all:
	gcc $(C_FLAG) -o wav2iq wav2iq.c $(LD_FLAG)
	gcc $(C_FLAG) -o test main.c $(LD_FLAG)
clean:
	rm fm_send

