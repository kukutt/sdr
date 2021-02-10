#!/bin/sh

(while true; do cat $2; done) | csdr convert_i16_f \
  | csdr fir_interpolate_cc 10 | csdr dsb_fc \
  | csdr bandpass_fir_fft_cc -0.06 -0.002 0.01 | csdr fastagc_ff | csdr convert_f_s8 \
  | hackrf_transfer -f $1 -s 480000 -x 20 -t -

