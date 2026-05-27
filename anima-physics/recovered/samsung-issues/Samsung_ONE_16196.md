https://github.com/Samsung/ONE/issues/16196
# [compiler] end of life of python3.10 for focal

`ppa:deadsnakes` has dropped python3.10 (and all other versions too) for `focal` and removed those packages,
as `focal` has reached end-of-life.

we'll get errors like this when we try to install;
```
E: Package 'python3.10' has no installation candidate
E: Package 'python3.10-venv' has no installation candidate
E: Unable to locate package python3.10-dev
E: Couldn't find any package by glob 'python3.10-dev'
```

---

We have alternate method to install python3.10 on focal: https://github.com/astral-sh/uv

---

TODO
- [x] disable `focal` test for push commit, for the moment
- [x] update `docs/howto/how-to-build-compiler.md`
- [x] after python3.10 is available again,
   - [x] update `docs/howto/how-to-build-compiler.md` again
   - [x] update `circle-mlir/infra/docker/focal/Dockerfile`

