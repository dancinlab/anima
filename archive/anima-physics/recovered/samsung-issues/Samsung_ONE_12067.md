https://github.com/Samsung/ONE/issues/12067
# [onert] Revisit Loss operation

### What

Now, we implemented the basic loss pass and it worked well.
However, there are many things left to consider about.
To list it up,

- [x] Separate LossInformation from TrainingInfo (#12073)
- [x] Consider ReductionType
   - Need to change every process that Loss goes through must be modified
   - [x] #12105
   - [x] #12106
   - [x] #12135
   - [x] #12164
- [ ] #12362 
- [ ] Design Parameters related to Loss
   - [x] MeanSquaredError: x
   - [x] CategoricalCrossentropy: axis, label_smoothing
      - #12141 
   - SparseCrossentropy: ignore_class

