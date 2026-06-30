https://github.com/Samsung/ONE/issues/3258
# [gen_golden] error during conversion :unsupported operand type for NoneType and int

I have encounted error during gen_golden. It happens with tf2.2 and tf2.3rc0. Not tested on other tf versions.

```
(tf-2.3-rc0) ~/d/O/t/n/gen_golden> ./gen_golden.py frozen.pb
2020-07-17 13:50:22.235019: W tensorflow/stream_executor/platform/default/dso_loader.cc:59] Could not load dynamic library 'libcudart.so.10.1'; dlerror: libcudart.so.10.1: cannot open shared object file: No such file or directory
2020-07-17 13:50:22.235049: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Traceback (most recent call last):
  File "./gen_golden.py", line 102, in <module>
    input_values.append(np.random.randint(0, 99, this_shape))
  File "mtrand.pyx", line 743, in numpy.random.mtrand.RandomState.randint
  File "_bounded_integers.pyx", line 1239, in numpy.random._bounded_integers._rand_int64
  File "<__array_function__ internals>", line 6, in prod
  File "/home/twoflower/.virtualenvs/tf-2.3-rc0/lib/python3.5/site-packages/numpy/core/fromnumeric.py", line 2962, in prod
    keepdims=keepdims, initial=initial, where=where)
  File "/home/twoflower/.virtualenvs/tf-2.3-rc0/lib/python3.5/site-packages/numpy/core/fromnumeric.py", line 90, in _wrapreduction
    return ufunc.reduce(obj, axis, dtype, out, **passkwargs)
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

Here is a model IO summary by summurize_graph : 

```
Found 2 possible inputs: (name=inputs_0, type=int32(3), shape=[?,32]) (name=inputs_1, type=int32(3), shape=[?]) 
No variables spotted.
Found 2 possible outputs: (name=Identity, op=Identity) (name=Identity_1, op=Identity) 
```
