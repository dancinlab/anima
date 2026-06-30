https://github.com/Samsung/ONE/issues/1937
# [onert] Try to write a draft to testing large pb file 

- Testing a large pb file is scary. :fearful: 
    - We'd better split it into small test graphs.
- Two approaches are possible:
    - option 1. convert it to tfilte file. Then split small tflite graph files and test
        - cons: it's hard to get expected input and output. We may want to compare values from TFLite inpterpreter and onert and check if they are same. However when TFLite inpterpreter does not support all ops, it is hard.
    - option 2. split pb file intp small pb files. Then convert them into tflite files.
       - better go get expected data with TF.
       - cons: control flow handling is tricky :open_mouth: + if we optimize [op 1 .. op n]  by one compiler, we should have a way to put [op 1 .. op n] in a test graph.

Let's try option 2 here.

How to tackle:

- [x] step 0) study how to modify graphdef to add placeholder as an input of a certain op
- [x] step 1) run TF with specific input data and dump shape of all tensors
- [x] step 2) write code to select ops that will be used as a input and outputs of test graphs
- [x] step 3) write a pb graph splitter(?) using starting/ending ops at step 2
- [ ] step 4) run TFLC to convert graphs (step 3) to tfl files
- [x] step 5) run TF with specific input data/shape (found at step 1) and dump value of input/outputs for ops selected at step 2. (maybe skipped since it's done at 2)
- [ ] step 6) write test driver

<sub>(moved from https://github.sec.samsung.net/STAR/nnfw/issues/11439)</sub>

