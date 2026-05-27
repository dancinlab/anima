https://github.com/Samsung/TICO/issues/28
# Support dynamic shape inputs for Floerence 2

## What 

`torch.onnx.export` supports exporting ONNX models with dynamic input/output shapes using `dynamic_axes` option. 

<details>

<summary> `torch.onnx.export` with `dynamic_axes` example </summary> 

  ```python 
  import torch
  import torch.nn as nn
  
  # Define a simple model
  class SimpleModel(nn.Module):
      def __init__(self):
          super(SimpleModel, self).__init__()
          self.linear = nn.Linear(2, 2)
  
      def forward(self, x):
          return self.linear(x)
  
  # Instantiate the model
  model = SimpleModel()
  
  # Set model to evaluation mode
  model.eval()
  
  # Create a dummy input tensor (shape must match model input)
  dummy_input = torch.randn(1, 2)
  
  # Export the model
  torch.onnx.export(
      model,                  			# model being run
      dummy_input,            			# model input (or a tuple for multiple inputs)
      "simple_model.onnx",    			# where to save the model (can be a file or file-like object)
      input_names=["input"],  			# the model's input names
      output_names=["output"],			# the model's output names
  	dynamic_axes={
  		"input": {0: "batch_size"},	# Mark axis 0 of input as dynamic
  		"output": {0: "batch_size"},# Mark axis 0 of output as dynamic 
  	}
  )
  
  print("Model exported to simple_model.onnx!")
  
  ``` 

</details> 


As far as I know, TICO doesn't support exporting a model with dynamic signatures. 
Is it possible to export to circle model with dynamic shapes? 
I'm not  familiar with TICO's internal, so I'd like to know how difficult it would be to implement this feature. 


## Why 

When running LLM models on CPU, exporting with a dynamic sequence length would be very useful. ( ONERT also supports circle with dynamic shapes. )

