https://github.com/Samsung/ONE/issues/4869
# [onert] Discussion : Introduce option to select kernel type in cpu backend

### Issue

In most cases, `onert` uses one fastest kernel for each operation in cpu backend. For example, Conv2D (FP32) uses `Eigen` and FullyConnected operation with weight quantize uses `ruy` library.

This policy fits well until now, but I found a counter-example. When I tried to use ruy library for FullyConnected (FP32) layer, a benchmark shows that ruy library is faster than current kernel only in some cases. https://github.com/Samsung/ONE/issues/4482#issuecomment-704798829

> Some models become 3x faster, while others become 3x slower. 

- Internal issue for profile result : https://github.sec.samsung.net/STAR/nnfw/issues/11818

I think it is better to support multiple kernels for one operation in onert and use one of them depending on each model.

### Suggestion

- Introduce `OP_KERNEL_MAP` environmental variable to select kernel type
  - This variable is for testing only and its format is the same as `OP_BACKEND_TYPE`
  - ex) `OP_KERNEL_MAP="2=ruy;5=neon"`
    - Operation 2 uses ruy library and operation 5 uses neon library
- onert uses selected kernel type if it is given by `OP_KERNEL_MAP`

Any suggestions are welcome!

/cc @Samsung/nnfw 
