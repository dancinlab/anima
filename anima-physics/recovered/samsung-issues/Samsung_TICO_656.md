https://github.com/Samsung/TICO/issues/656
# [quantization] Instability on `llama` quantization

### What

There is some instability in llama-based models quantization. E.g. 
Running the same command 
```
python tico/quantization/wrapq/examples/quantize_full_qmodel_with_gptq.py --model unsloth/Llama-3.2-3B-Instruct --max_seq_len 2048 --linear_weight_bits 4 --gptq_mse smse --nsamples_for_qcalibration 128 --device cuda --lm_head_weight_bits 4 --save  "ptq_checkpoint"   --no_spinquant  --eval_tasks="mmlu,hellaswag,piqa,truthfulqa" --decode_calibration_steps 8 --sensitivity_path sensitivities_for_unsloth_Llama-3.2-3B-Instruct_wikitext_128_42.pt
```
on two different gpus produced two dirreferent ppl's (`11.86` vs `12.14`).

Running `mse`:
```
python tico/quantization/wrapq/examples/quantize_full_qmodel_with_gptq.py --model unsloth/Llama-3.2-3B-Instruct --max_seq_len 2048 --linear_weight_bits 4 --gptq_mse mse --nsamples_for_qcalibration 128 --device cuda --lm_head_weight_bits 4 --save  "ptq_checkpoint"   --no_spinquant  --eval_tasks="mmlu,hellaswag,piqa,truthfulqa" --decode_calibration_steps 8 
```
also produced two different ppl's (`12.56` vs `12.52`).

Let's make sure that: 
1. this is inevitable
2.  and/or reduce discrepancy of results.
