https://github.com/Samsung/ONE/issues/10617
# [onert] always run in tracing mode

During #10610, I've found our `LinearExecutor` always run in tracing mode.

Without profiling enabled, it should run `else` code, which has no overhead due to profiling.

https://github.com/Samsung/ONE/blob/e289e63b764e3296e3726726b45a687eaf442ac8/runtime/onert/core/src/exec/LinearExecutor.cc#L56-L72

But, current code always run in tracing mode.

https://github.com/Samsung/ONE/blob/e289e63b764e3296e3726726b45a687eaf442ac8/runtime/onert/core/src/exec/LinearExecutor.cc#L29-L41

Maybe, `tracing_ctx` is always created while it was created conditionally.

We need to fix it.
