#!/bin/sh

(while true; do cat $1; done) | csdr convert_i16_f \
  | csdr fir_interpolate_cc 2 | csdr dsb_fc | csdr fastagc_ff \
  | sudo sendiq -i /dev/stdin -s 96000 -f "434e6" -t float

