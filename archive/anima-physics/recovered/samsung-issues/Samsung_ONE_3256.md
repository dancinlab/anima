https://github.com/Samsung/ONE/issues/3256
# [docs] Broken links in compiled sphinx pages

For example, in the page https://nnfw.readthedocs.io/en/latest/runtime/heterogeneous-execution.html ,

When you click on "Lowering", the link is broken. The link address is `./core.md#1-lowering` which works on github view(https://github.com/Samsung/ONE/blob/master/docs/runtime/heterogeneous-execution.md) however it looks like Sphinx does not convert the link correctly.

cc: @lemmaa 
