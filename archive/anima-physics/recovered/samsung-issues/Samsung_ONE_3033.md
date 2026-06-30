https://github.com/Samsung/ONE/issues/3033
# Failure for building benchmark_model_plus_flex.

I faced a build error for benchmark_model_plus_flex.
(benchmark_model was succeed to build.)

If you have an experience, Could you please let me share. 

**Configuration**. 

```bash
$ ./configure
WARNING: --batch mode is deprecated. Please instead explicitly shut down your Bazel server using the command "bazel shutdown".
INFO: Invocation ID: f11887f3-a0ac-4886-99b4-bd647ffdfbae
You have bazel 0.21.0 installed.
Please specify the location of python. [Default is /usr/bin/python]: 

Found possible Python library paths:
  /usr/lib/python3/dist-packages
  /usr/local/lib/python3.6/dist-packages
Please input the desired Python library path to use.  Default is [/usr/lib/python3/dist-packages]

Do you wish to build TensorFlow with XLA JIT support? [Y/n]: n
No XLA JIT support will be enabled for TensorFlow.

Do you wish to build TensorFlow with OpenCL SYCL support? [y/N]: n
No OpenCL SYCL support will be enabled for TensorFlow.

Do you wish to build TensorFlow with ROCm support? [y/N]: n
No ROCm support will be enabled for TensorFlow.

Do you wish to build TensorFlow with CUDA support? [y/N]: n
No CUDA support will be enabled for TensorFlow.

Do you wish to download a fresh release of clang? (Experimental) [y/N]: n
Clang will not be downloaded.

Do you wish to build TensorFlow with MPI support? [y/N]: n
No MPI support will be enabled for TensorFlow.

Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -march=native -Wno-sign-compare]: 

Would you like to interactively configure ./WORKSPACE for Android builds? [y/N]: y
Searching for NDK and SDK installations.

Please specify the home path of the Android NDK to use. [Default is /home/tizenrt/Android/Sdk/ndk-bundle]: /home/tizenrt/Android/Sdk/ndk/17.2.4988734

Please specify the home path of the Android SDK to use. [Default is /home/tizenrt/Android/Sdk]: 

Please specify the Android SDK API level to use. [Available levels: ['30']] [Default is 30]: 

Please specify an Android build tools version to use. [Available versions: ['30.0.0']] [Default is 30.0.0]: 

Preconfigured Bazel build configs. You can use any of the below by adding "--config=<>" to your build command. See .bazelrc for more details.
	--config=mkl         	# Build with MKL support.
	--config=monolithic  	# Config for mostly static monolithic build.
	--config=gdr         	# Build with GDR support.
	--config=verbs       	# Build with libverbs support.
	--config=ngraph      	# Build with Intel nGraph support.
	--config=dynamic_kernels	# (Experimental) Build kernels into separate shared objects.
Preconfigured Bazel build configs to DISABLE default on features:
	--config=noaws       	# Disable AWS S3 filesystem support.
	--config=nogcp       	# Disable GCP support.
	--config=nohdfs      	# Disable HDFS support.
	--config=noignite    	# Disable Apacha Ignite support.
	--config=nokafka     	# Disable Apache Kafka support.
	--config=nonccl      	# Disable NVIDIA NCCL support.
Configuration finished

```


**Build**

```bash
$bazel build --config=monolithic --config=android_arm64 -c opt --cxxopt='--std=c++14' tensorflow/lite/tools/benchmark:benchmark_model_plus_flex

...

8 warnings generated.
ERROR: /home/tizenrt/ws/private/one/externals/tensorflow/tensorflow/core/BUILD:1709:1: C++ compilation of rule '//tensorflow/core:android_tensorflow_lib_lite' failed (Exit 1)
In file included from tensorflow/core/common_runtime/constant_folding.cc:41:
In file included from ./tensorflow/core/platform/setround.h:19:
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:68:9: error: no member named 'feclearexcept' in the global namespace
using ::feclearexcept;
      ~~^
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:69:9: error: no member named 'fegetexceptflag' in the global namespace
using ::fegetexceptflag;
      ~~^
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:70:9: error: no member named 'feraiseexcept' in the global namespace
using ::feraiseexcept;
      ~~^
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:71:9: error: no member named 'fesetexceptflag' in the global namespace
using ::fesetexceptflag;
      ~~^
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:72:9: error: no member named 'fetestexcept' in the global namespace
using ::fetestexcept;
      ~~^
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:73:9: error: no member named 'fegetround' in the global namespace
using ::fegetround;
      ~~^
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:74:9: error: no member named 'fesetround' in the global namespace
using ::fesetround;
      ~~^
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:75:9: error: no member named 'fegetenv' in the global namespace; did you mean 'getenv'?
using ::fegetenv;
      ~~^
external/androidndk/ndk/sysroot/usr/include/stdlib.h:61:7: note: 'getenv' declared here
char* getenv(const char* __name);
      ^
In file included from tensorflow/core/common_runtime/constant_folding.cc:41:
In file included from ./tensorflow/core/platform/setround.h:19:
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:76:9: error: no member named 'feholdexcept' in the global namespace
using ::feholdexcept;
      ~~^
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:77:9: error: no member named 'fesetenv' in the global namespace
using ::fesetenv;
      ~~^
external/androidndk/ndk/sources/cxx-stl/llvm-libc++/include/cfenv:78:9: error: no member named 'feupdateenv' in the global namespace
using ::feupdateenv;
      ~~^
11 errors generated.
Target //tensorflow/lite/tools/benchmark:benchmark_model_plus_flex failed to build
Use --verbose_failures to see the command lines of failed build steps.
INFO: Elapsed time: 663.675s, Critical Path: 144.80s
INFO: 342 processes: 342 local.
FAILED: Build did NOT complete successfully
```
