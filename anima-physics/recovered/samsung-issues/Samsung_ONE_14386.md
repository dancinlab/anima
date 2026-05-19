https://github.com/Samsung/ONE/issues/14386
# [luci/pass] FuseInstanceNormPass with 3D causes shape inference failure

`FuseInstanceNormPass` with 3D (as GroupNorm from ONNX) causes shape inference failure
- related #13778

> circle2circle: ERROR: Internal Exception. Cannot produce expand_dimension of two shapes [/home/jenkins/jenkins_agent/workspace/nnfw/master/daily-publish-package/code/compiler/luci/service/src/CircleShapeInferenceHelper.cpp:90]
