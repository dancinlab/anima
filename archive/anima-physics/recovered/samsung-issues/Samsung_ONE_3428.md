https://github.com/Samsung/ONE/issues/3428
# [onert] tizen gbd build failed

head commit
```
dragon@loki:~/Works/github/ONE$ git log --oneline -n 1
bb2ee45f (HEAD -> master, upstream/master) [luci-interpreter] Add `KernelBuilder` tests (#3417)
```

build log
```
dragon@loki:~/Works/github/ONE$ gbs -c ~/onert.gbs.conf build -A armv7l --profile=profile.tizen --include-all --define 'test_build 1' --clean   
...
[   48s] /home/abuild/rpmbuild/BUILD/nnfw-1.6.0/compute/ARMComputeEx/src/core/CL/kernels/CLBinaryLogicalOpKernel.cpp:46:10: fatal error: support/StringSupport.h: No such file or directory
[   48s]    46 | #include "support/StringSupport.h" 
[   48s]       |          ^~~~~~~~~~~~~~~~~~~~~~~~~
[   48s] compilation terminated.                               
[   48s] compute/ARMComputeEx/CMakeFiles/arm_compute_ex.dir/build.make:86: recipe for target 'compute/ARMComputeEx/CMakeFiles/arm_compute_ex.dir/src/core/CL/kernels/CLBinaryLogicalOpKernel.cpp.o' failed
[   48s] make[2]: *** [compute/ARMComputeEx/CMakeFiles/arm_compute_ex.dir/src/core/CL/kernels/CLBinaryLogicalOpKernel.cpp.o] Error 1
[   48s] make[2]: *** Waiting for unfinished jobs....
[   48s] [  1%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/block_map.cc.o
[   48s] Scanning dependencies of target jsoncpp                          
[   48s] [  1%] Building CXX object runtime/3rdparty/jsoncpp/CMakeFiles/jsoncpp.dir/jsoncpp.cpp.o
[   48s] [  2%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/blocking_counter.cc.o
[   49s] [  2%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/context.cc.o
[   49s] [  2%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/detect_arm.cc.o
[   49s] [  2%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/detect_x86.cc.o
[   49s] [  3%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/have_built_path_for_avx2.cc.o
[   49s] [  3%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/have_built_path_for_avx512.cc.o
[   49s] [  3%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/have_built_path_for_avxvnni.cc.o
[   49s] [  3%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/have_built_path_for_sse42.cc.o
[   49s] [  3%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/kernel_arm32.cc.o
[   50s] [  4%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/kernel_arm64.cc.o
[   50s] [  4%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/kernel_avx2.cc.o
[   50s] [  4%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/kernel_avx512.cc.o
[   50s] [  4%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/kernel_avxvnni.cc.o
[   50s] [  5%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/kernel_sse42.cc.o
[   50s] [  5%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/pack_arm.cc.o
[   51s] [  5%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/pack_avx2.cc.o
[   51s] [  5%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/pack_avx512.cc.o
[   51s] [  5%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/pack_avxvnni.cc.o
[   51s] [  6%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/pack_sse42.cc.o
[   51s] [  6%] Building CXX object externals/ruy/CMakeFiles/ruy.dir/home/abuild/rpmbuild/BUILD/nnfw-1.6.0/externals/ruy/ruy/prepacked_cache.cc.o
[   51s] CMakeFiles/Makefile2:297: recipe for target 'compute/ARMComputeEx/CMakeFiles/arm_compute_ex.dir/all' failed
[   51s] make[1]: *** [compute/ARMComputeEx/CMakeFiles/arm_compute_ex.dir/all] Error 2
[   51s] make[1]: *** Waiting for unfinished jobs....
```

my config file
```
dragon@loki:~/Works/github/ONE$ cat ~/onert.gbs.conf
[general]
#Current profile name which should match a profile section name
profile = profile.tizen

[profile.tizen]
user=obs_viewer
...
obs = obs.tizen
repos = repo.tizen_base,repo.tizen_mobile
buildroot = /home/dragon/GBS-ROOT-ONERT/

[obs.tizen]
url = http://api.tizen.org

[repo.tizen_mobile]
url = http://download.tizen.org/snapshots/tizen/unified/latest/repos/standard/packages/

[repo.tizen_base]
url =  http://download.tizen.org/snapshots/tizen/base/latest/repos/standard/packages/
```

Hmm.. it causes on my local pc?
