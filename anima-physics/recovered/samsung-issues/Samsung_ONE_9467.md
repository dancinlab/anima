https://github.com/Samsung/ONE/issues/9467
# [luci-micro] Remove C++ runtime from micro interpreter

## Goal

- Investigate how C++ library affects flash footprint of luci-micro interpreter
- Verify that licu-interpreter could run without C++ runtime
- Modify luci-micro and/or it's CMakeListst.txt accordingly

## Motivation

C++ libraries could add significant overhead on binary size.
This could be an issue for MCU based applications.
