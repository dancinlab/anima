https://github.com/Samsung/ONE/issues/12526
# Compiler FE: Sometimes tests failed

# What
- If I run `./nncc test` after configure and build, test failures always occur in two modules.
```
The following tests FAILED:
         64 - pota_quantization_test_with_config (Failed)
         76 - circle-interpreter-test (Failed)
```
- After that, if `./nncc test` is executed again, the test was successful without any problems.


# Related Log
```
leeseunghui@leeseunghui-400TEA-400SEA:~/workspace2/ONE$ ./nncc test -j8
Test project /home/leeseunghui/workspace2/ONE/build
      Start 59: pota_fake_wquant_test
      Start 62: pota_fake_wquant_test_with_config
      Start 57: record_minmax_conversion_test
      Start 44: luci_unit_readtest
      Start 24: tflchef_test
      Start 45: luci_unit_writetest
      Start 72: circle_quantizer_dredd_recipe_test
      Start 58: q-implant-qparam-test
 1/76 Test #72: circle_quantizer_dredd_recipe_test .....   Passed    2.16 sec
      Start 71: circle2circle_dredd_recipe_test
 2/76 Test #71: circle2circle_dredd_recipe_test ........   Passed    2.35 sec
      Start 56: tflite2circle_conversion_test
 3/76 Test #44: luci_unit_readtest .....................   Passed    5.52 sec
      Start 69: embedded_import_value_test
 4/76 Test #24: tflchef_test ...........................   Passed    6.07 sec
      Start 70: dalgona_single_op_test
 5/76 Test #45: luci_unit_writetest ....................   Passed    6.16 sec
      Start 65: pota_wo_quantization_test
 6/76 Test #65: pota_wo_quantization_test ..............   Passed    0.90 sec
      Start 32: luci_lang_test
 7/76 Test #59: pota_fake_wquant_test ..................   Passed    7.14 sec
      Start 60: pota_record_minmax_test
 8/76 Test #62: pota_fake_wquant_test_with_config ......   Passed    7.14 sec
      Start 64: pota_quantization_test_with_config
 9/76 Test #32: luci_lang_test .........................   Passed    0.54 sec
      Start 66: minmax_embedder_value_test
10/76 Test #66: minmax_embedder_value_test .............   Passed    0.38 sec
      Start 75: visq_unittest
11/76 Test #69: embedded_import_value_test .............   Passed    3.21 sec
      Start 28: circlechef_test
12/76 Test #70: dalgona_single_op_test .................   Passed    2.90 sec
      Start 36: luci_pass_test
13/76 Test #28: circlechef_test ........................   Passed    0.34 sec
      Start  4: hermes_test
14/76 Test #36: luci_pass_test .........................   Passed    0.11 sec
      Start 76: circle-interpreter-test
15/76 Test  #4: hermes_test ............................   Passed    0.08 sec
      Start 74: circle-operator-test
16/76 Test #74: circle-operator-test ...................   Passed    0.01 sec
      Start 17: hermes_std_test
17/76 Test #17: hermes_std_test ........................   Passed    0.00 sec
      Start 13: locomotiv_test
18/76 Test #13: locomotiv_test .........................   Passed    0.01 sec
      Start 14: loco_test
19/76 Test #14: loco_test ..............................   Passed    0.00 sec
      Start 21: dio_hdf5_test
20/76 Test #21: dio_hdf5_test ..........................   Passed    0.00 sec
      Start 12: morph_test
21/76 Test #12: morph_test .............................   Passed    0.00 sec
      Start 54: circle_mpqsolver_test
22/76 Test #54: circle_mpqsolver_test ..................   Passed    0.05 sec
      Start  1: angkor_test
23/76 Test  #1: angkor_test ............................   Passed    0.01 sec
      Start 48: luci_interpreter_kernels_test
24/76 Test #48: luci_interpreter_kernels_test ..........   Passed    0.05 sec
      Start  2: arser_test
25/76 Test  #2: arser_test .............................   Passed    0.00 sec
      Start 39: luci_partition_test
26/76 Test #39: luci_partition_test ....................   Passed    0.01 sec
      Start 15: crew_test
27/76 Test #15: crew_test ..............................   Passed    0.01 sec
      Start  9: pepper_strcast_test
28/76 Test  #9: pepper_strcast_test ....................   Passed    0.00 sec
      Start 55: circle_eval_diff_test
29/76 Test #55: circle_eval_diff_test ..................   Passed    0.00 sec
      Start 37: luci_profile_test
30/76 Test #37: luci_profile_test ......................   Passed    0.00 sec
      Start 22: tfinfo_test
31/76 Test #22: tfinfo_test ............................   Passed    0.00 sec
      Start 33: luci_logex_test
32/76 Test #33: luci_logex_test ........................   Passed    0.00 sec
      Start 25: locoex_customop_test
33/76 Test #75: visq_unittest ..........................   Passed    1.27 sec
      Start 40: luci_import_test
34/76 Test #25: locoex_customop_test ...................   Passed    0.00 sec
      Start 18: locop_test
35/76 Test #18: locop_test .............................   Passed    0.00 sec
      Start 46: minmax_embedder_test
36/76 Test #40: luci_import_test .......................   Passed    0.01 sec
      Start 50: circle2circle_test
37/76 Test #46: minmax_embedder_test ...................   Passed    0.01 sec
      Start 35: luci_service_test
38/76 Test #50: circle2circle_test .....................   Passed    0.01 sec
      Start 42: luci_readtester_test
39/76 Test #35: luci_service_test ......................   Passed    0.01 sec
      Start 29: logo_test
40/76 Test #29: logo_test ..............................   Passed    0.00 sec
      Start 51: circle-opselector-test
41/76 Test #42: luci_readtester_test ...................   Passed    0.01 sec
      Start 11: vconone_test
42/76 Test #11: vconone_test ...........................   Passed    0.00 sec
      Start 53: dalgona_unit_test
43/76 Test #53: dalgona_unit_test ......................   Passed    0.00 sec
      Start  6: mio_tflite2121_helper_test
44/76 Test  #6: mio_tflite2121_helper_test .............   Passed    0.00 sec
      Start 38: luci_plan_test
45/76 Test #38: luci_plan_test .........................   Passed    0.00 sec
      Start 30: logo_ex_test
46/76 Test #51: circle-opselector-test .................   Passed    0.01 sec
      Start 41: luci_export_test
47/76 Test #30: logo_ex_test ...........................   Passed    0.00 sec
      Start 49: luci_interpreter_loader_test
48/76 Test #49: luci_interpreter_loader_test ...........   Passed    0.00 sec
      Start  8: pepper_str_test
49/76 Test  #8: pepper_str_test ........................   Passed    0.00 sec
      Start  3: cwrap_test
50/76 Test #41: luci_export_test .......................   Passed    0.01 sec
      Start 16: oops_test
51/76 Test  #3: cwrap_test .............................   Passed    0.00 sec
      Start 43: luci_writetester_test
52/76 Test #16: oops_test ..............................   Passed    0.00 sec
      Start 31: luci_env_test
53/76 Test #31: luci_env_test ..........................   Passed    0.00 sec
      Start 34: luci_testhelper_test
54/76 Test #34: luci_testhelper_test ...................   Passed    0.00 sec
      Start  7: pepper_csv2vec_test
55/76 Test  #7: pepper_csv2vec_test ....................   Passed    0.00 sec
      Start 10: pp_test
56/76 Test #10: pp_test ................................   Passed    0.00 sec
      Start 47: luci_interpreter_memory_manager_test
57/76 Test #43: luci_writetester_test ..................   Passed    0.01 sec
      Start 26: circlechef_core_test
58/76 Test #26: circlechef_core_test ...................   Passed    0.00 sec
      Start 52: record_minmax_function_test
59/76 Test #47: luci_interpreter_memory_manager_test ...   Passed    0.00 sec
      Start 20: logo_core_test
60/76 Test #52: record_minmax_function_test ............   Passed    0.00 sec
      Start  5: mio_circle07_helper_test
61/76 Test #20: logo_core_test .........................   Passed    0.00 sec
      Start 19: luci_compute_test
62/76 Test  #5: mio_circle07_helper_test ...............   Passed    0.00 sec
      Start 23: tflchef_test
63/76 Test #19: luci_compute_test ......................   Passed    0.00 sec
      Start 27: circlechef_test
64/76 Test #23: tflchef_test ...........................   Passed    0.00 sec
      Start 67: luci_value_py_test
65/76 Test #27: circlechef_test ........................   Passed    0.00 sec
      Start 68: luci_pass_value_py_test
66/76 Test #76: circle-interpreter-test ................***Failed    0.39 sec
Running main() from /home/leeseunghui/workspace2/ONE/externals/GTEST/googletest/src/gtest_main.cc
[==========] Running 5 tests from 1 test suite.
[----------] Global test environment set-up.
[----------] 5 tests from circle_interpreter_test
[ RUN      ] circle_interpreter_test.show_help_msg
What circle-interpreter does: Interpreter driver for circle models

Usage: ./circle-interpreter [-h] [--version] model_path input_prefix output_prefix 

[Positional argument]
model_path      Circle model filepath
input_prefix    Input data filepath for circle model. n-th input data is rea
                d from ${input_prefix}n, for example, Add.circle.input0, Add
                .circle.input1
output_prefix   Output data filepath for circle model. Output data is writte
                n in ${output_file}n, for example, Add.circle.output0

[Optional argument]
-h, --help      Show help message and exit
--version       Show version information and exit


[       OK ] circle_interpreter_test.show_help_msg (3 ms)
[ RUN      ] circle_interpreter_test.valid_command

/home/leeseunghui/workspace2/ONE/compiler/circle-interpreter-test/src/circle-interpreter.test.cpp:170: Failure
Failed
[  FAILED  ] circle_interpreter_test.valid_command (254 ms)
[ RUN      ] circle_interpreter_test.invalid_option_NEG
Invalid argument. You must have missed some argument.
What circle-interpreter does: Interpreter driver for circle models

Usage: ./circle-interpreter [-h] [--version] model_path input_prefix output_prefix 

[Positional argument]
model_path      Circle model filepath
input_prefix    Input data filepath for circle model. n-th input data is rea
                d from ${input_prefix}n, for example, Add.circle.input0, Add
                .circle.input1
output_prefix   Output data filepath for circle model. Output data is writte
                n in ${output_file}n, for example, Add.circle.output0

[Optional argument]
-h, --help      Show help message and exit
--version       Show version information and exit


[       OK ] circle_interpreter_test.invalid_option_NEG (4 ms)
[ RUN      ] circle_interpreter_test.not_existing_model_NEG
Failed to open file: /home/leeseunghui/workspace2/ONE/build/compiler/common-artifacts/non_exist_file.foo
ERROR: Failed to load '/home/leeseunghui/workspace2/ONE/build/compiler/common-artifacts/non_exist_file.foo'

[       OK ] circle_interpreter_test.not_existing_model_NEG (4 ms)
[ RUN      ] circle_interpreter_test.invalid_input_prefix_NEG
terminate called after throwing an instance of 'std::runtime_error'
  what():  Cannot open file "/home/leeseunghui/workspace2/ONE/build/compiler/common-artifacts/non_exist_file.foo0".

Aborted (core dumped)

[       OK ] circle_interpreter_test.invalid_input_prefix_NEG (118 ms)
[----------] 5 tests from circle_interpreter_test (384 ms total)

[----------] Global test environment tear-down
[==========] 5 tests from 1 test suite ran. (384 ms total)
[  PASSED  ] 4 tests.
[  FAILED  ] 1 test, listed below:
[  FAILED  ] circle_interpreter_test.valid_command

 1 FAILED TEST

      Start 73: circle_part_value_py_test
67/76 Test #56: tflite2circle_conversion_test ..........   Passed    5.94 sec
68/76 Test #60: pota_record_minmax_test ................   Passed    3.51 sec
      Start 63: pota_parallel_record_minmax_test
      Start 61: pota_quantization_test
69/76 Test #64: pota_quantization_test_with_config .....***Failed    4.13 sec
-- Found CIRCLE_QUANTIZER: /home/leeseunghui/workspace2/ONE/build/compiler/circle-quantizer/circle-quantizer
-- Found CIRCLE_TENSORDUMP: /home/leeseunghui/workspace2/ONE/build/compiler/circle-tensordump/circle-tensordump
-- Found workdir: /home/leeseunghui/workspace2/ONE/build/compiler/common-artifacts
~/workspace2/ONE/build/compiler/common-artifacts ~/workspace2/ONE/build/compiler/pota-quantization-value-test
~/workspace2/ONE/build/compiler/pota-quantization-value-test
Traceback (most recent call last):
  File "/home/leeseunghui/workspace2/ONE/compiler/pota-quantization-value-test/compare_tensors_all.py", line 165, in <module>
    with h5.File(input_h5, 'r') as input:
  File "/home/leeseunghui/workspace2/ONE/build/overlay/venv_2_12_1/lib/python3.8/site-packages/h5py/_hl/files.py", line 562, in __init__
    fid = make_fid(name, mode, userblock_size, fapl, fcpl, swmr=swmr)
  File "/home/leeseunghui/workspace2/ONE/build/overlay/venv_2_12_1/lib/python3.8/site-packages/h5py/_hl/files.py", line 235, in make_fid
    fid = h5f.open(name, flags, fapl=fapl)
  File "h5py/_objects.pyx", line 54, in h5py._objects.with_phil.wrapper
  File "h5py/_objects.pyx", line 55, in h5py._objects.with_phil.wrapper
  File "h5py/h5f.pyx", line 102, in h5py.h5f.open
OSError: Unable to synchronously open file (file signature not found)

70/76 Test #61: pota_quantization_test .................   Passed    1.17 sec
71/76 Test #63: pota_parallel_record_minmax_test .......   Passed    1.24 sec
72/76 Test #58: q-implant-qparam-test ..................   Passed   12.36 sec
73/76 Test #73: circle_part_value_py_test ..............   Passed   11.24 sec
74/76 Test #68: luci_pass_value_py_test ................   Passed   11.72 sec
75/76 Test #57: record_minmax_conversion_test ..........   Passed   21.14 sec
76/76 Test #67: luci_value_py_test .....................   Passed   12.91 sec

97% tests passed, 2 tests failed out of 76

Total Test time (real) =  22.31 sec

The following tests FAILED:
         64 - pota_quantization_test_with_config (Failed)
         76 - circle-interpreter-test (Failed)
Errors while running CTest
```
