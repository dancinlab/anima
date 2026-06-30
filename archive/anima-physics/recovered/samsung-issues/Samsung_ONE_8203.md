https://github.com/Samsung/ONE/issues/8203
# Enable SVDF Op

## What?
Let's support svdf operation.
## Why?
One of the benchmarks for tflite micro is the following model: 

[model.zip](https://github.com/Samsung/ONE/files/7762412/model.zip)

![keyword_model](https://user-images.githubusercontent.com/43214667/147089001-6e5dc3d7-c091-44e1-89fe-971f25a4f58b.png)

At this moment we cannot run this model on the `luci-interpreter`. One of the problems is the presence of an SVDF operation that needs to be supported. 
To understand better you can see this issue #7598 and this comment https://github.com/Samsung/ONE/issues/7598#issuecomment-916384853

## How?
First of all we need support this parts:
- [x] tflite2circle #8204
- [x] common-artifacts add item to exclude new recipes #8282
- [x] res/TensorFlowLiteRecipes #8285
- [x] tflchef #8284
- [x] tfldump and circledump #8286 #8287
- [x] luci/lang  #8291
- [x] luci/import #8292 
- [x] luci/service
- [ ] luci/pass
- [x] luci/log, luci/logex
- [x] luci/tests addread
- [x] luci/exports
- [x] luci/tests addwrite
- [x] luci-interpreter
- [x] luci-interpreter/pal
- [x] luci/partition
- [ ] common-artifacts remove items added

 
