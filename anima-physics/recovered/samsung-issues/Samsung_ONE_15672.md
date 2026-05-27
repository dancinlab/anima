https://github.com/Samsung/ONE/issues/15672
# [compiler] Experiment AArch64 build on Raspberry Pi 4

Experiment build on RPi4
- 8GB RAM
- 10GB swap
- 256G SSD.
- Ubuntu 22.04

```
$ uname -a
Linux seanrpi64 5.15.0-1077-raspi #80-Ubuntu SMP PREEMPT Thu Apr 17 03:17:35 UTC 2025 aarch64 aarch64 aarch64 GNU/Linux
```

To do
- [x] normal configure, build and test
- [x] build setup
- [x] onnx2circle for AArch64
   - [x] externals for AArch64
- [x] in setup, run `one-prepare-venv`
- [x] in setup, run `test`
- [x] `test` with working `one-import-onnx` with success
- [x] remove `one-cmds/one-prepare-venv.aarch64` 
