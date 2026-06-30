https://github.com/Samsung/ONE/issues/2088
# Test for post-training quantization

**Updated 2020/06/24**: The test framework now tests the end-to-end quantization steps (fake quantization, record minmax, quantization).

We are implementing post-training quantization (#696). This issue is about `quantization-value-test`, which tests the quantized values of a circle model.

![image](https://user-images.githubusercontent.com/5449554/85508474-19282180-b62f-11ea-84b4-b2f6b899f00d.png)

Above figure shows the overview of `quantization-value-test`. More details about the test process is described below.

**Step 1. Fake quantization**
Run `circle2circle` with `--quantize_dequantize_weights` option.
Dump the fake-quantized model with `circle-tensordump`.
Compare the dumped model with the expected output in "expected_outputs/<model_name>/fake_quantization/<tensor_name>"
The expected output should include
 (1) values of weights (for conv, transposed_conv, depthwise_conv, fc layers)

**Step 2. Record moving avg of min and moving avg of max for activations**
Run `record-minmax` with the fake-quantized model (input data is saved in "test_inputs/<model_name>/<record_number>")
Dump the minmax-recorded model with `circle-tensordump`.
Compare the dumped model with the expected output in "expected_outputs/<model_name>/record_minmax/<tensor_name>"
The expected output should include
 (1) min/max of activations

**Step 3. Quantization**
Run `circle2circle` with `--quantize_with_minmax` option.
Dump the quantized model with `circle-tensordump`.
Compare the dumped model with the expected output in "expected_outputs/<model_name>/quantization/<tensor_name>"
The expected output should include
 (1) scale, zero point of activations
 (2) scale, zero point, values of weights
 (3) scale, values (weights) of bias
