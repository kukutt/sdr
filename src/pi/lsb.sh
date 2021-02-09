#!/bin/sh

(while true; do cat $1; done) | csdr convert_i16_f \
  | csdr fir_interpolate_cc 4 | csdr dsb_fc \
  | csdr bandpass_fir_fft_cc -0.06 -0.002 0.01 | csdr fastagc_ff \
  | sudo sendiq -i /dev/stdin -s 192000 -f "434e6" -t float

