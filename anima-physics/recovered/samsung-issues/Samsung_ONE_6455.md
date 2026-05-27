https://github.com/Samsung/ONE/issues/6455
# [circle-quantizer] Replace `TestIOGraph.h` with the `testhelper TestIOGraph.h`

Let's use `compiler/luci/testhelper/include/luci/test/TestIOGraph.h` instead of `compiler/luci/pass/src/test/TestIOGraph.h`.

As the module is moved and maintained as a `testhelper`, it's better to remove the staled one.

For #6367 
Related to #6335


