https://github.com/Samsung/ONE/issues/14391
# [onert] Series run of unittest fail on ubuntu 24.04 arm device

Run all unittests (release build) on xu4 ubuntu 24.04

```
$ ./Product/armv7l-linux.release/out/test/onert-test unittest

...

[       OK ] GenModelTest.neg_OneOp_FullyConnected_NoBias (1 ms)
[ RUN      ] GenModelTest.OneOp_Gather_Q4_0
/home/nfs/git/ONE/Product/armv7l-linux.release/out/test/command/unittest: line 78:  1563 Illegal instruction     $TEST_BIN $(get_gtest_option)
/home/nfs/git/ONE/Product/armv7l-linux.release/out/unittest/nnfw_api_gtest failed... return code: 132
============================================
Finishing set 6: /home/nfs/git/ONE/Product/armv7l-linux.release/out/unittest/nnfw_api_gtest...
============================================

```

But `nnfw_api_gtest` run passed

```
$ ./Product/out/unittest/nnfw_api_gtest

...

[       OK ] GenModelTest/WhileWrongSubgraphIndex.neg_Test/4 (0 ms)
[----------] 5 tests from GenModelTest/WhileWrongSubgraphIndex (3 ms total)

[----------] Global test environment tear-down
[==========] 650 tests from 35 test suites ran. (12359 ms total)
[  PASSED  ] 650 tests.
```

This issue is found on release build only (not on debug build)
