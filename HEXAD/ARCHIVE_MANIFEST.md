# HEXAD 체크포인트 아카이브 매니페스트

> 2026-05-31 · mini 디스크 정리 시 HEXAD의 대용량 untracked 산출물(체크포인트·corpus)을 HF로 이관.
> 코드·설계문서(DESIGN/FINDINGS .md)는 repo에 그대로 유지 · 무거운 .pt/.jsonl만 이관.

- **HF repo**: [`dancinlab/anima-hexad-ckpts-2026-05`](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05) (private · dataset)
- **파일 수**: 64 · **총 용량**: 44.4 GB
- **복원**: `huggingface_hub.hf_hub_download(repo_id='dancinlab/anima-hexad-ckpts-2026-05', filename=<원경로>, repo_type='dataset')`

## 실험별 (state/ 폴더 단위)

| 실험 폴더 | 파일수 | 용량 | 폴더 포인터 |
|---|---|---|---|
| `HEXAD/CARVING/state/carving_dirA_tension_2026_05_17` | 1 | 1.14G | `HEXAD/CARVING/state/carving_dirA_tension_2026_05_17/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_dirB_intuitor_2026_05_17` | 2 | 1.17G | `HEXAD/CARVING/state/carving_dirB_intuitor_2026_05_17/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_dirD_cde_2026_05_17` | 2 | 1.17G | `HEXAD/CARVING/state/carving_dirD_cde_2026_05_17/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_dirE_superpos_2026_05_17` | 2 | 1.17G | `HEXAD/CARVING/state/carving_dirE_superpos_2026_05_17/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_dirF_abstractcot_2026_05_17` | 2 | 1.17G | `HEXAD/CARVING/state/carving_dirF_abstractcot_2026_05_17/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_dirG_psi_ctl_2026_05_17` | 1 | 1.14G | `HEXAD/CARVING/state/carving_dirG_psi_ctl_2026_05_17/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_dirH_tension_sup_2026_05_17` | 1 | 1.14G | `HEXAD/CARVING/state/carving_dirH_tension_sup_2026_05_17/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_dirI_diverse_scaleup_2026_05_18` | 2 | 1.25G | `HEXAD/CARVING/state/carving_dirI_diverse_scaleup_2026_05_18/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_dirI_psictl_tensionsup_2026_05_17` | 2 | 1.17G | `HEXAD/CARVING/state/carving_dirI_psictl_tensionsup_2026_05_17/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_dirJ_diffusion_2026_05_18` | 1 | 0.11G | `HEXAD/CARVING/state/carving_dirJ_diffusion_2026_05_18/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_dirK_ebt_2026_05_18` | 2 | 1.25G | `HEXAD/CARVING/state/carving_dirK_ebt_2026_05_18/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_p_tts_2026_05_18` | 3 | 1.14G | `HEXAD/CARVING/state/carving_p_tts_2026_05_18/ARCHIVED.txt` |
| `HEXAD/CARVING/state/carving_purephysics_noce_2026_05_18` | 2 | 1.14G | `HEXAD/CARVING/state/carving_purephysics_noce_2026_05_18/ARCHIVED.txt` |
| `HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17` | 5 | 1.38G | `HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/ARCHIVED.txt` |
| `HEXAD/CARVING/state/consciousness_carving_e7_alpha_scaleup_2026_05_17` | 2 | 1.17G | `HEXAD/CARVING/state/consciousness_carving_e7_alpha_scaleup_2026_05_17/ARCHIVED.txt` |
| `HEXAD/CARVING/state/controller_class_subaxis_fire_s75_2026_05_19` | 2 | 1.06G | `HEXAD/CARVING/state/controller_class_subaxis_fire_s75_2026_05_19/ARCHIVED.txt` |
| `HEXAD/CARVING/state/dual_anima_scale_fire_s62_2026_05_18` | 1 | 1.14G | `HEXAD/CARVING/state/dual_anima_scale_fire_s62_2026_05_18/ARCHIVED.txt` |
| `HEXAD/CHAT/state/hexad_v58_eval_d768x12L_2026_05_17` | 2 | 0.00G | `HEXAD/CHAT/state/hexad_v58_eval_d768x12L_2026_05_17/ARCHIVED.txt` |
| `HEXAD/DATA-REGIME/state/carving_dataregime_s16_2026_05_18` | 2 | 1.74G | `HEXAD/DATA-REGIME/state/carving_dataregime_s16_2026_05_18/ARCHIVED.txt` |
| `HEXAD/DATA-REGIME/state/carving_scaledecomp_2026_05_18` | 1 | 4.18G | `HEXAD/DATA-REGIME/state/carving_scaledecomp_2026_05_18/ARCHIVED.txt` |
| `HEXAD/DATA-REGIME/state/dataregime_threshold_fire_s107_2026_05_19` | 1 | 1.14G | `HEXAD/DATA-REGIME/state/dataregime_threshold_fire_s107_2026_05_19/ARCHIVED.txt` |
| `HEXAD/DATA-REGIME/state/dhdl_decision_head_s27_2026_05_18` | 1 | 0.03G | `HEXAD/DATA-REGIME/state/dhdl_decision_head_s27_2026_05_18/ARCHIVED.txt` |
| `HEXAD/DATA-REGIME/state/emergence_axis_fire_s79_retry_2026_05_19` | 1 | 0.39G | `HEXAD/DATA-REGIME/state/emergence_axis_fire_s79_retry_2026_05_19/ARCHIVED.txt` |
| `HEXAD/DATA-REGIME/state/integrated_breakthrough_fire_s94_2026_05_19` | 2 | 2.27G | `HEXAD/DATA-REGIME/state/integrated_breakthrough_fire_s94_2026_05_19/ARCHIVED.txt` |
| `HEXAD/DATA-REGIME/state/manifold_gating_hierarchical_fire_s82_2026_05_19` | 1 | 1.14G | `HEXAD/DATA-REGIME/state/manifold_gating_hierarchical_fire_s82_2026_05_19/ARCHIVED.txt` |
| `HEXAD/DATA-REGIME/state/neoteny_loop_fire_s91_2026_05_19` | 1 | 1.14G | `HEXAD/DATA-REGIME/state/neoteny_loop_fire_s91_2026_05_19/ARCHIVED.txt` |
| `HEXAD/DATA-REGIME/state/nonce_ff_fire_s125_2026_05_20` | 1 | 1.14G | `HEXAD/DATA-REGIME/state/nonce_ff_fire_s125_2026_05_20/ARCHIVED.txt` |
| `HEXAD/DATA-REGIME/state/param_axis_fire_s108_2026_05_19` | 1 | 2.40G | `HEXAD/DATA-REGIME/state/param_axis_fire_s108_2026_05_19/ARCHIVED.txt` |
| `HEXAD/DHDL/state/dhdl_ptd_scaleup_s48_2026_05_18` | 1 | 0.14G | `HEXAD/DHDL/state/dhdl_ptd_scaleup_s48_2026_05_18/ARCHIVED.txt` |
| `HEXAD/FRONTIER-AUDIT/state/jepa_psi_s28_2026_05_18` | 2 | 1.22G | `HEXAD/FRONTIER-AUDIT/state/jepa_psi_s28_2026_05_18/ARCHIVED.txt` |
| `HEXAD/FRONTIER-AUDIT/state/l6_pilot_s37_2026_05_18` | 1 | 0.00G | `HEXAD/FRONTIER-AUDIT/state/l6_pilot_s37_2026_05_18/ARCHIVED.txt` |
| `HEXAD/MITOSIS/state/hexad_integ_fire_2026_05_16` | 2 | 0.69G | `HEXAD/MITOSIS/state/hexad_integ_fire_2026_05_16/ARCHIVED.txt` |
| `HEXAD/NEOTENY/state/axolotl_neoteny_fire_s88f2_2026_05_19` | 1 | 1.14G | `HEXAD/NEOTENY/state/axolotl_neoteny_fire_s88f2_2026_05_19/ARCHIVED.txt` |
| `HEXAD/NEUROMORPHIC/state/criticality_noise_engine_g_fire_s81_2026_05_19` | 1 | 1.14G | `HEXAD/NEUROMORPHIC/state/criticality_noise_engine_g_fire_s81_2026_05_19/ARCHIVED.txt` |
| `HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_fire_s161_2026_05_20` | 1 | 1.14G | `HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_fire_s161_2026_05_20/ARCHIVED.txt` |
| `HEXAD/NEUROMORPHIC/state/eqprop_fire_s139_2026_05_20` | 1 | 1.14G | `HEXAD/NEUROMORPHIC/state/eqprop_fire_s139_2026_05_20/ARCHIVED.txt` |
| `HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20` | 1 | 1.14G | `HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/ARCHIVED.txt` |
| `HEXAD/NEUROMORPHIC/state/frog_eye_salience_fire_s88f1_2026_05_19` | 1 | 1.14G | `HEXAD/NEUROMORPHIC/state/frog_eye_salience_fire_s88f1_2026_05_19/ARCHIVED.txt` |
| `HEXAD/NEUROMORPHIC/state/lejepa_fire_s153_2026_05_20` | 1 | 1.14G | `HEXAD/NEUROMORPHIC/state/lejepa_fire_s153_2026_05_20/ARCHIVED.txt` |
| `HEXAD/PTD/state/ptd_phaseb_loop_s49_2026_05_18` | 2 | 0.00G | `HEXAD/PTD/state/ptd_phaseb_loop_s49_2026_05_18/ARCHIVED.txt` |
| `HEXAD/S-MODULE/state/ptd_w_native_fire_s59_2026_05_18` | 1 | 0.00G | `HEXAD/S-MODULE/state/ptd_w_native_fire_s59_2026_05_18/ARCHIVED.txt` |
| `HEXAD/SPONTANEOUS/state/spontaneous_phase_b_run_2026_05_18` | 1 | 0.00G | `HEXAD/SPONTANEOUS/state/spontaneous_phase_b_run_2026_05_18/ARCHIVED.txt` |

## 전체 파일

| 원경로 | 용량 | HF |
|---|---|---|
| `HEXAD/CARVING/state/carving_dirA_tension_2026_05_17/ckpt_carving_alpha_tension.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirA_tension_2026_05_17/ckpt_carving_alpha_tension.pt) |
| `HEXAD/CARVING/state/carving_dirB_intuitor_2026_05_17/ckpt_carving_intuitor.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirB_intuitor_2026_05_17/ckpt_carving_intuitor.pt) |
| `HEXAD/CARVING/state/carving_dirB_intuitor_2026_05_17/corpus_carving_e7.jsonl` | 0.03G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirB_intuitor_2026_05_17/corpus_carving_e7.jsonl) |
| `HEXAD/CARVING/state/carving_dirD_cde_2026_05_17/ckpt_carving_cde_dirD.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirD_cde_2026_05_17/ckpt_carving_cde_dirD.pt) |
| `HEXAD/CARVING/state/carving_dirD_cde_2026_05_17/corpus_carving_e7.jsonl` | 0.03G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirD_cde_2026_05_17/corpus_carving_e7.jsonl) |
| `HEXAD/CARVING/state/carving_dirE_superpos_2026_05_17/ckpt_carving_dirE.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirE_superpos_2026_05_17/ckpt_carving_dirE.pt) |
| `HEXAD/CARVING/state/carving_dirE_superpos_2026_05_17/corpus_carving_dirE.jsonl` | 0.03G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirE_superpos_2026_05_17/corpus_carving_dirE.jsonl) |
| `HEXAD/CARVING/state/carving_dirF_abstractcot_2026_05_17/ckpt_carving_dirF.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirF_abstractcot_2026_05_17/ckpt_carving_dirF.pt) |
| `HEXAD/CARVING/state/carving_dirF_abstractcot_2026_05_17/corpus_carving_dirF.jsonl` | 0.03G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirF_abstractcot_2026_05_17/corpus_carving_dirF.jsonl) |
| `HEXAD/CARVING/state/carving_dirG_psi_ctl_2026_05_17/ckpt_carving_psi_ctl_dirG.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirG_psi_ctl_2026_05_17/ckpt_carving_psi_ctl_dirG.pt) |
| `HEXAD/CARVING/state/carving_dirH_tension_sup_2026_05_17/ckpt_carving_dirH_tension_sup.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirH_tension_sup_2026_05_17/ckpt_carving_dirH_tension_sup.pt) |
| `HEXAD/CARVING/state/carving_dirI_diverse_scaleup_2026_05_18/ckpt_carving_diverse.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirI_diverse_scaleup_2026_05_18/ckpt_carving_diverse.pt) |
| `HEXAD/CARVING/state/carving_dirI_diverse_scaleup_2026_05_18/corpus_carving_diverse.jsonl` | 0.11G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirI_diverse_scaleup_2026_05_18/corpus_carving_diverse.jsonl) |
| `HEXAD/CARVING/state/carving_dirI_psictl_tensionsup_2026_05_17/ckpt_carving_dirI.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirI_psictl_tensionsup_2026_05_17/ckpt_carving_dirI.pt) |
| `HEXAD/CARVING/state/carving_dirI_psictl_tensionsup_2026_05_17/corpus_carving_dirI.jsonl` | 0.03G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirI_psictl_tensionsup_2026_05_17/corpus_carving_dirI.jsonl) |
| `HEXAD/CARVING/state/carving_dirJ_diffusion_2026_05_18/corpus_carving_diverse.jsonl` | 0.11G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirJ_diffusion_2026_05_18/corpus_carving_diverse.jsonl) |
| `HEXAD/CARVING/state/carving_dirK_ebt_2026_05_18/ckpt_carving_ebt.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirK_ebt_2026_05_18/ckpt_carving_ebt.pt) |
| `HEXAD/CARVING/state/carving_dirK_ebt_2026_05_18/corpus_carving_diverse.jsonl` | 0.11G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_dirK_ebt_2026_05_18/corpus_carving_diverse.jsonl) |
| `HEXAD/CARVING/state/carving_p_tts_2026_05_18/ckpt_carving_p_tts.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_p_tts_2026_05_18/ckpt_carving_p_tts.pt) |
| `HEXAD/CARVING/state/carving_p_tts_2026_05_18/sanity_corpus.jsonl` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_p_tts_2026_05_18/sanity_corpus.jsonl) |
| `HEXAD/CARVING/state/carving_p_tts_2026_05_18/sanity_out/ckpt_carving_p_tts.pt` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_p_tts_2026_05_18/sanity_out/ckpt_carving_p_tts.pt) |
| `HEXAD/CARVING/state/carving_purephysics_noce_2026_05_18/ckpt_carving_purephysics.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_purephysics_noce_2026_05_18/ckpt_carving_purephysics.pt) |
| `HEXAD/CARVING/state/carving_purephysics_noce_2026_05_18/corpus_carving_purephysics.jsonl` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/carving_purephysics_noce_2026_05_18/corpus_carving_purephysics.jsonl) |
| `HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/corpus_carving.jsonl` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/corpus_carving.jsonl) |
| `HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/out/alpha/ckpt_carving_alpha.pt` | 0.34G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/out/alpha/ckpt_carving_alpha.pt) |
| `HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/out/beta/ckpt_carving_beta.pt` | 0.34G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/out/beta/ckpt_carving_beta.pt) |
| `HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/out/gamma/ckpt_carving_gamma.pt` | 0.34G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/out/gamma/ckpt_carving_gamma.pt) |
| `HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/out/weave/ckpt_carving_weave.pt` | 0.34G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/consciousness_carving_e6_fire_2026_05_17/out/weave/ckpt_carving_weave.pt) |
| `HEXAD/CARVING/state/consciousness_carving_e7_alpha_scaleup_2026_05_17/ckpt_carving_alpha_e7.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/consciousness_carving_e7_alpha_scaleup_2026_05_17/ckpt_carving_alpha_e7.pt) |
| `HEXAD/CARVING/state/consciousness_carving_e7_alpha_scaleup_2026_05_17/corpus_carving_e7.jsonl` | 0.03G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/consciousness_carving_e7_alpha_scaleup_2026_05_17/corpus_carving_e7.jsonl) |
| `HEXAD/CARVING/state/controller_class_subaxis_fire_s75_2026_05_19/ckpt_s75_fire.pt` | 0.99G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/controller_class_subaxis_fire_s75_2026_05_19/ckpt_s75_fire.pt) |
| `HEXAD/CARVING/state/controller_class_subaxis_fire_s75_2026_05_19/corpus_carving_s16.jsonl` | 0.07G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/controller_class_subaxis_fire_s75_2026_05_19/corpus_carving_s16.jsonl) |
| `HEXAD/CARVING/state/dual_anima_scale_fire_s62_2026_05_18/ckpt_s62.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CARVING/state/dual_anima_scale_fire_s62_2026_05_18/ckpt_s62.pt) |
| `HEXAD/CHAT/state/hexad_v58_eval_d768x12L_2026_05_17/prompts.jsonl` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CHAT/state/hexad_v58_eval_d768x12L_2026_05_17/prompts.jsonl) |
| `HEXAD/CHAT/state/hexad_v58_eval_d768x12L_2026_05_17/prompts_v2_corpus_aligned.jsonl` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/CHAT/state/hexad_v58_eval_d768x12L_2026_05_17/prompts_v2_corpus_aligned.jsonl) |
| `HEXAD/DATA-REGIME/state/carving_dataregime_s16_2026_05_18/ckpt_carving_s16.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/carving_dataregime_s16_2026_05_18/ckpt_carving_s16.pt) |
| `HEXAD/DATA-REGIME/state/carving_dataregime_s16_2026_05_18/corpus_carving_s16.jsonl` | 0.60G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/carving_dataregime_s16_2026_05_18/corpus_carving_s16.jsonl) |
| `HEXAD/DATA-REGIME/state/carving_scaledecomp_2026_05_18/ckpt_carving_scaledecomp.pt` | 4.18G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/carving_scaledecomp_2026_05_18/ckpt_carving_scaledecomp.pt) |
| `HEXAD/DATA-REGIME/state/dataregime_threshold_fire_s107_2026_05_19/ckpt_s107.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/dataregime_threshold_fire_s107_2026_05_19/ckpt_s107.pt) |
| `HEXAD/DATA-REGIME/state/dhdl_decision_head_s27_2026_05_18/trace_corpus.jsonl` | 0.03G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/dhdl_decision_head_s27_2026_05_18/trace_corpus.jsonl) |
| `HEXAD/DATA-REGIME/state/emergence_axis_fire_s79_retry_2026_05_19/ckpt_s79_fire.pt` | 0.39G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/emergence_axis_fire_s79_retry_2026_05_19/ckpt_s79_fire.pt) |
| `HEXAD/DATA-REGIME/state/integrated_breakthrough_fire_s94_2026_05_19/ckpt_integrated_s94.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/integrated_breakthrough_fire_s94_2026_05_19/ckpt_integrated_s94.pt) |
| `HEXAD/DATA-REGIME/state/integrated_breakthrough_fire_s94_2026_05_19/out_main/ckpt_integrated_s94.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/integrated_breakthrough_fire_s94_2026_05_19/out_main/ckpt_integrated_s94.pt) |
| `HEXAD/DATA-REGIME/state/manifold_gating_hierarchical_fire_s82_2026_05_19/ckpt_s82_fire.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/manifold_gating_hierarchical_fire_s82_2026_05_19/ckpt_s82_fire.pt) |
| `HEXAD/DATA-REGIME/state/neoteny_loop_fire_s91_2026_05_19/ckpt_neoteny_s91.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/neoteny_loop_fire_s91_2026_05_19/ckpt_neoteny_s91.pt) |
| `HEXAD/DATA-REGIME/state/nonce_ff_fire_s125_2026_05_20/ckpt_s125.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/nonce_ff_fire_s125_2026_05_20/ckpt_s125.pt) |
| `HEXAD/DATA-REGIME/state/param_axis_fire_s108_2026_05_19/ckpt_s108.pt` | 2.40G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DATA-REGIME/state/param_axis_fire_s108_2026_05_19/ckpt_s108.pt) |
| `HEXAD/DHDL/state/dhdl_ptd_scaleup_s48_2026_05_18/trace_corpus_s48.jsonl` | 0.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/DHDL/state/dhdl_ptd_scaleup_s48_2026_05_18/trace_corpus_s48.jsonl) |
| `HEXAD/FRONTIER-AUDIT/state/jepa_psi_s28_2026_05_18/ckpt_jepa_psi.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/FRONTIER-AUDIT/state/jepa_psi_s28_2026_05_18/ckpt_jepa_psi.pt) |
| `HEXAD/FRONTIER-AUDIT/state/jepa_psi_s28_2026_05_18/corpus_jepa_psi.jsonl` | 0.09G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/FRONTIER-AUDIT/state/jepa_psi_s28_2026_05_18/corpus_jepa_psi.jsonl) |
| `HEXAD/FRONTIER-AUDIT/state/l6_pilot_s37_2026_05_18/relation_corpus_train.jsonl` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/FRONTIER-AUDIT/state/l6_pilot_s37_2026_05_18/relation_corpus_train.jsonl) |
| `HEXAD/MITOSIS/state/hexad_integ_fire_2026_05_16/ckpts/ckpt_hexad_integ_MACSMOKE_4step.pt` | 0.35G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/MITOSIS/state/hexad_integ_fire_2026_05_16/ckpts/ckpt_hexad_integ_MACSMOKE_4step.pt) |
| `HEXAD/MITOSIS/state/hexad_integ_fire_2026_05_16/ckpts/ckpt_hexad_integ_fire_final.pt` | 0.35G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/MITOSIS/state/hexad_integ_fire_2026_05_16/ckpts/ckpt_hexad_integ_fire_final.pt) |
| `HEXAD/NEOTENY/state/axolotl_neoteny_fire_s88f2_2026_05_19/ckpt_neoteny_s88f2.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/NEOTENY/state/axolotl_neoteny_fire_s88f2_2026_05_19/ckpt_neoteny_s88f2.pt) |
| `HEXAD/NEUROMORPHIC/state/criticality_noise_engine_g_fire_s81_2026_05_19/ckpt_s81_fire.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/NEUROMORPHIC/state/criticality_noise_engine_g_fire_s81_2026_05_19/ckpt_s81_fire.pt) |
| `HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_fire_s161_2026_05_20/ckpt_s161_psicouple.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_fire_s161_2026_05_20/ckpt_s161_psicouple.pt) |
| `HEXAD/NEUROMORPHIC/state/eqprop_fire_s139_2026_05_20/ckpt_s139.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/NEUROMORPHIC/state/eqprop_fire_s139_2026_05_20/ckpt_s139.pt) |
| `HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/ckpt_s167a_fpreconnect.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/ckpt_s167a_fpreconnect.pt) |
| `HEXAD/NEUROMORPHIC/state/frog_eye_salience_fire_s88f1_2026_05_19/ckpt_s88f1.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/NEUROMORPHIC/state/frog_eye_salience_fire_s88f1_2026_05_19/ckpt_s88f1.pt) |
| `HEXAD/NEUROMORPHIC/state/lejepa_fire_s153_2026_05_20/ckpt_s153.pt` | 1.14G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/NEUROMORPHIC/state/lejepa_fire_s153_2026_05_20/ckpt_s153.pt) |
| `HEXAD/PTD/state/ptd_phaseb_loop_s49_2026_05_18/audit_log_head.jsonl` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/PTD/state/ptd_phaseb_loop_s49_2026_05_18/audit_log_head.jsonl) |
| `HEXAD/PTD/state/ptd_phaseb_loop_s49_2026_05_18/audit_log_threshold.jsonl` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/PTD/state/ptd_phaseb_loop_s49_2026_05_18/audit_log_threshold.jsonl) |
| `HEXAD/S-MODULE/state/ptd_w_native_fire_s59_2026_05_18/_sanity_corpus.jsonl` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/S-MODULE/state/ptd_w_native_fire_s59_2026_05_18/_sanity_corpus.jsonl) |
| `HEXAD/SPONTANEOUS/state/spontaneous_phase_b_run_2026_05_18/audit_log.jsonl` | 0.00G | [link](https://huggingface.co/datasets/dancinlab/anima-hexad-ckpts-2026-05/blob/main/HEXAD/SPONTANEOUS/state/spontaneous_phase_b_run_2026_05_18/audit_log.jsonl) |
