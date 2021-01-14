C_FLAG := -I $(PWD)/../../run/include/libhackrf/
C_FLAG += -I $(PWD)/../../run/include/
C_FLAG += -Wno-strict-aliasing
LD_FLAG := -lm $(PWD)/../../run/lib/libhackrf.a
LD_FLAG += -lm $(PWD)/../../run/lib/librtlsdr.a
LD_FLAG += -lusb-1.0 -lpthread

all:
	gcc $(C_FLAG) -o wav2iq wav2iq.c $(LD_FLAG)
	gcc $(C_FLAG) -o test main.c $(LD_FLAG)
	gcc $(C_FLAG) -o rtl_my rtl_my.c convenience/convenience.c $(LD_FLAG)
clean:
	rm fm_send

