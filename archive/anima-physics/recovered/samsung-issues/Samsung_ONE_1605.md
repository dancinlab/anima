https://github.com/Samsung/ONE/issues/1605
# Introduce record-minmax for post-training quantization

This issue tracks the status of `record-minmax` #1537, a tool to embed min/max values of activation tensors to the circle model, for post-training quantization #696 .

What record-minmax does is described below (copied from #696).

> **Record min-max value of each tensor while running the representative dataset**
**Input**: circle model (fp32), representative dataset (format is hdf5)
**Output**: circle model (fp32) where min-max values of tensors are saved in QuantizationParameters.
**Details**: Users run executable named record-minmax, which invokes luci-interpreter to perform inference on the given dataset. Whenever performing inference on each data, record-minmax records the moving average of min and the moving average of max for each tensor. After the whole dataset is fed to the interpreter, the recorded average min-max values are saved in the QuantizationParameters of each tensor in the circle model.

This issue tracks the following items.

**1. Pre-processing of input data**
- [x] Script for pre-processing representative dataset [internal link](https://github.sec.samsung.net/AIP/models/blob/master/official/vision/image_classification/tfrecord2hdf5.py)

**2. Driver to run luci-interpreter and record min/max values (record-minmax)**

- [x] Import circle model #1607
- [x] Read representative dataset #1750
- [x] Collect tensor data while luci-interpreter runs with the representative dataset #1867
- [x] Determine min/max values from the collected data (using clipping or averaging ..) #2091
- [x] Save the min/max values to the loco graph #2005
- [x] Export the circle model #1607
- [x] Test #1948

Any suggestions and comments are welcome.
