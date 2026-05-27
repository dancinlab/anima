https://github.com/Samsung/ONE/issues/5347
# [onert] Building and running errors on macOS

I know `ONE` does not officially support macOS.
However, I have to use macOS at home today.
There are several errors and some workaround I've used.

TL;DR **~Use docker.~** <- It also has its problems.
**Use Linux.**

#### 1. readlink -f
```
[ 11%] Generating runtime nnapi tests
readlink: illegal option -- f
usage: readlink [-n] [file ...]
```

##### Workaround
Install `greadlink` and create a symbolic link from `readlink` to `greadlink`.
You can install `greadlink` using `brew install coreutils`.


#### 2. TEMP_FAILURE_RETRY
```
ONE/tests/nnapi/src/TestValidation.cpp:55:9: error: use of undeclared identifier 'TEMP_FAILURE_RETRY'
    if (TEMP_FAILURE_RETRY(ftruncate(fd, size)) == -1) {
        ^
```

##### Workaround
Comment out the lines.

#### 3. benchmark/Phases
```
$ LD_LIBRARY_PATH=./Product/x86_64-linux.debug/out/lib/ \
ONERT_LOG_ENABLE=1 BACKENDS=cpu \
Product/out/bin/nnpackage_run --nnpackage mobilenet_v1_1.0_224_quant
Package Filename mobilenet_v1_1.0_224_quant
Assertion failed: (prepareVmRSS()), function Phases, file ONE/runtime/libs/benchmark/src/Phases.cpp, line 52.
Abort trap: 6
```

##### Workaround
No simple workaround. It needs to change several lines.
At this stage, I switch to docker desktop with nnfw/nnas image.
