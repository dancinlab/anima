https://github.com/Samsung/ONE/issues/15484
# [CI] check run-onecc-build for dalgona

`run-onecc-build` workflow has
```
      # dalgona uses pybind11, but pybind11 cannot bind packages in virtualenv.
      # So we need to install packages for dalgona-test globally.
      - name: Install required packages
        run: |
          python3 -m pip install numpy h5py==3.11.0 flatbuffers==23.5.26
```
which canbe removed if virtualenv can be used.

let's check if it is possible.
