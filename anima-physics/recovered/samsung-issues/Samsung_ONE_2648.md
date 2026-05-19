https://github.com/Samsung/ONE/issues/2648
# [onert] StridedSlice op with wrong(?) inputs does not fail

During testing a _large test_ model, StridedSlice was called like the follow:

`StridedSlice(input_shape = [1, 111, 512], begin_shape = [2], end_shape = [2], stride_shape = [3])`
where buf of begin = (0, 0), end = (0, 1), stride = (1, 1, 1)
and the output shape of StridedSlice is [1, 1, 0].

From the shape inference code, I believed that some error should occur since the code iterates `begin` and `end` from 0 to the rank of input. So I guess this should throw an error.

Also kernel of strided_slice ran without error. I wonder if this is correct behavior.

Could someone check this?

BTW, @seanshpark also told me that
`tensorflow/lite/toco/graph_transformations/propagate_fixed_sizes.cc` has the following code, where start, stop, strided could be equal to or smaller than input rank. 
```
  CHECK_LE(op->start_indices.size(), num_input_axes)
      << "StridedSlice op with output \"" << op->outputs[0]
      << "\", requires no more than " << num_input_axes << " start indices";
  CHECK_LE(op->stop_indices.size(), num_input_axes)
      << "StridedSlice op with output \"" << op->outputs[0]
      << "\", requires no more than " << num_input_axes << " stop indices";
  CHECK_LE(op->strides.size(), num_input_axes)
      << "StridedSlice op with output \"" << op->outputs[0]
      << "\", requires no more than " << num_input_axes << " strides";
```



