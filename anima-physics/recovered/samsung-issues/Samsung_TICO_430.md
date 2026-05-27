https://github.com/Samsung/TICO/issues/430
# Need to support conv3d conversion

## What

Some VL models(ex, qwen-vl) use conv3d in their vision encoder,
so tico needs a pass to convert conv3d to other operations, like conv2d
