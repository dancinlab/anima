# H_1631 CPU smoke log (summer pool, CUDA_VISIBLE_DEVICES="" = CPU, tiny d32/L2/3step)
# date: 2026-06-28  host: summer (RTX5070 box, run on CPU)  torch: 2.11.0+cu130

## arm=ctrl summary.json:
{
 "arm": "ctrl",
 "levers": {
  "tlora": false,
  "tlora_rank": 8,
  "tlora_base": true,
  "dict_aux": false,
  "jamo_aux": false,
  "wd_floor": -1.0,
  "dropout_floor": -1.0
 },
 "n_params": 35555,
 "loss0": 5.63872,
 "lossF": 5.47802,
 "dbes_final": {
  "expert_div": 0.57688,
  "router_entropy": 1.0214,
  "usage_gini": 0.09636,
  "usage": [
   0.28491,
   0.42944,
   0.28565
  ],
  "n_experts": 3
 },
 "tier": "engine-native-eligible (.clm additive, TLoRA materialized); torch probe DIRECTIONAL"
}

## arm=tlora summary.json:
{
 "arm": "tlora",
 "levers": {
  "tlora": true,
  "tlora_rank": 4,
  "tlora_base": true,
  "dict_aux": false,
  "jamo_aux": false,
  "wd_floor": -1.0,
  "dropout_floor": -1.0
 },
 "n_params": 36359,
 "loss0": 5.68361,
 "lossF": 5.59278,
 "dbes_final": {
  "expert_div": 0.6524,
  "router_entropy": 1.02797,
  "usage_gini": 0.09174,
  "usage": [
   0.28721,
   0.42481,
   0.28798
  ],
  "n_experts": 3
 },
 "tier": "engine-native-eligible (.clm additive, TLoRA materialized); torch probe DIRECTIONAL"
}

## arm=tlora_dict summary.json:
{
 "arm": "tlora_dict",
 "levers": {
  "tlora": true,
  "tlora_rank": 4,
  "tlora_base": true,
  "dict_aux": true,
  "jamo_aux": false,
  "wd_floor": -1.0,
  "dropout_floor": -1.0
 },
 "n_params": 36359,
 "loss0": 5.68361,
 "lossF": 5.56669,
 "dbes_final": {
  "expert_div": 0.65387,
  "router_entropy": 1.02979,
  "usage_gini": 0.08433,
  "usage": [
   0.29079,
   0.41729,
   0.29192
  ],
  "n_experts": 3
 },
 "tier": "engine-native-eligible (.clm additive, TLoRA materialized); torch probe DIRECTIONAL"
}

## arm=tlora_jamo summary.json:
{
 "arm": "tlora_jamo",
 "levers": {
  "tlora": true,
  "tlora_rank": 4,
  "tlora_base": true,
  "dict_aux": false,
  "jamo_aux": true,
  "wd_floor": -1.0,
  "dropout_floor": -1.0
 },
 "n_params": 36359,
 "loss0": 5.74512,
 "lossF": 5.63696,
 "dbes_final": {
  "expert_div": 0.64881,
  "router_entropy": 1.0198,
  "usage_gini": 0.10175,
  "usage": [
   0.28233,
   0.43496,
   0.28271
  ],
  "n_experts": 3
 },
 "tier": "engine-native-eligible (.clm additive, TLoRA materialized); torch probe DIRECTIONAL"
}

## g_gates engine-native pipe (tlora .clm):
clm_decodable=True; g_gates G0-G6 all measured; mouth=clm; detector 10/10 (see smoke run)
