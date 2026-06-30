https://github.com/Samsung/ONE/issues/1398
# [onert] fp16 doesn't work

tip commit af40105fa73bc952767b9bf41a1a543256484d43
```
odroid@odroid:/home/dragon/Works/github/ONE$ FP16_ENABLE=1 ./Product/out/bin/nnapi_test benchmark_nnpkg_models/mobilenet_v2_1.0_224/mobilenet_v2_1.0_224.tflite
[NNAPI TEST] Run T/F Lite Interpreter without NNAPI
[NNAPI TEST] Run T/F Lite Interpreter with NNAPI
nnapi function 'ANeuralNetworksModel_create' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_addOperand' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_setOperandValue' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_addOperation' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_identifyInputsAndOutputs' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_finish' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksCompilation_create' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksCompilation_finish' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksExecution_create' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksExecution_setInput' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksExecution_setOutput' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksExecution_startCompute' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksEvent_wait' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksEvent_free' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksExecution_free' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksCompilation_free' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_free' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
[NNAPI TEST] Compare the result
  Tensor #62: MATCHED
    Max absolute diff at [0, 491]
       expected: 0.0834395
       obtained: 0.0834387
       absolute diff: 7.37607e-07
    Max relative diff at [0, 598]
       expected: 1.12795e-06
       obtained: 1.12796e-06
       relative diff: 1.51184e-05
         (tolerance level = 126.823)
[NNAPI TEST] PASSED

odroid@odroid:/home/dragon/Works/github/ONE$ FP16_ENABLE=1 ./Product/out/bin/nnapi_test benchmark_nnpkg_models/inception_v3/inception_v3.tflite
[NNAPI TEST] Run T/F Lite Interpreter without NNAPI
[NNAPI TEST] Run T/F Lite Interpreter with NNAPI
nnapi function 'ANeuralNetworksModel_create' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_addOperand' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_setOperandValue' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_addOperation' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_identifyInputsAndOutputs' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_finish' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksCompilation_create' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksCompilation_finish' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksExecution_create' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksExecution_setInput' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksExecution_setOutput' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksExecution_startCompute' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksEvent_wait' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksEvent_free' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksExecution_free' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksCompilation_free' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
nnapi function 'ANeuralNetworksModel_free' is loaded from '/home/dragon/Works/github/ONE/Product/armv7l-linux.release/out/bin/../lib/libneuralnetworks.so'
[NNAPI TEST] Compare the result
  Tensor #316: MATCHED
    Max absolute diff at [0, 490]
       expected: 0.159873
       obtained: 0.159869
       absolute diff: 3.50177e-06
    Max relative diff at [0, 490]
       expected: 0.159873
       obtained: 0.159869
       relative diff: 2.19035e-05
         (tolerance level = 183.74)
[NNAPI TEST] PASSED
```

The diff cannot be such that. (https://github.com/Samsung/ONE/pull/200#issuecomment-618270894)

I guess the config `FP16_ENABLE` doesn't work. or anything to know for setting config?
