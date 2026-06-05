@V := "tape" :: spec [active]
  version = "1.0"

# M13 7B-undertrained ConvMoE ENGINE rung — takeover of an orphaned fire.
# Sub-agent agent-af33b2b70770d3ecd, dispatched by anima session PID 1752.

@D CONVMOE_7B_OOM_GRADCKPT := "7B d6208/L30/E30 ConvMoE OOMs an 80GB H100 — root cause = grad-checkpoint flag was a no-op; WIRED + MERGED in PR#1864 (origin/main ad39cb7b3)" :: discovery [d=2026-06-06 active]
  seed   = "M13 발사가 첫 forward conv1d 에서 CUDA OOM (78.28GB allocated, 222MiB 추가 실패 @ 80GB H100)"
  claim  = "trainer --grad-checkpoint 가 help='(reserved)' no-op + model.py 에 torch.utils.checkpoint 호출 전무 → 30개 trunk layer activation 전부 retained → 80GB 초과. FIX = torch.utils.checkpoint 로 trunk backward-recompute (use_reentrant=False), CLMConfig.grad_checkpoint default False, trainer 가 --grad-checkpoint→cfg 전달. byte-eq PRESERVED (RUNTIME-only, recompute 동일출력, serialized byte 무변경 = dilation cap 동일논리). 실측 maxmem_GB=76.0 @ H200 (grad_accum8 batch4 seq512 bf16 AdamW8bit) → 80GB H100 fit. 🟢 numerical, PR#1864 merged."
  honest = "fix 자체는 closed; 그러나 이것은 OOM 인프라 수정이며 M13 3-axis GREEN closure 가 아님"

@D CONVMOE_7B_DESCENT_LIVE := "7.0568B ConvMoE descends on GPU @ STEP0 — params + leak-check + CE-start 실측, 그러나 완주는 orchestrator-deadlock 으로 미완 🟠" :: discovery [d=2026-06-06 active]
  seed   = "M13 fire 가 H200(141GB)에서 실제 step 진입 + descent 하는지 확인"
  claim  = "PARAMS n_params=7,056,813,918 (7.0568B) d=6208 E=30 L=30 K=3 V=256; STEP 0 ce=5.64211 (uniform ln256=5.54518 근처, init 정상); GPU util 64-68% mem 76-87GB resident, AdamW8bit 활성, LEAK_CHECK pass (held-out disjoint). GPU-resident 정상, CPU fallback 아님."
  scope  = "5GB corpus 로 fetch 가 잘림 → tokens_per_param=0.7085 (deeply undertrained vs Chinchilla 20). NO production-7B claim (a_scale_honest_scope). Lane-P torch (a_lane_akida_gpu_split)."
  falsifier = "3500-step 완주 후 val_ce<0.5*uniform AND rel_gap<=1.0 AND val_ce<shuffle 이면 M13 GREEN; 미완이면 INCOMPLETE (현재 상태)"
  honest = "🟠 INCOMPLETE — 부모 세션(PID1752) 의 중복 re-fire orchestrator loop 가 convmoe7b-refire* H200 pod 를 ~8분마다 새로 rent → 매 train 을 STEP0 에서 wipe. 7B(3500step,~수시간) 가 pod 수명(~8분) 초과 → 물리적으로 완주 불가. infra deadlock, NOT a science result. handoff b347a393(anima)."

@N STORM_POD_ID_ROTATION := "rate-limit storm 중 vast instance id 가 회전 — 같은 task pod 가 39616560→39618015→39620539→…→39625512 로 매번 새 id" :: note [d=2026-06-06 active]
  clarify = "SSH Connection-refused = old endpoint 사망 신호; label(convmoe*refire*) 로 추적, id 로 추적 금지. runpod-orphan-pod-on-ratelimit-storm memory 의 vast 판본."
  note    = "sub-agent 의 SSH babysit 이 부모 orchestrator loop 를 재발화시켜 pod recreation 유발 의심 — read-only API 모니터링이 덜 파괴적 (잠시 9분 stable). 다만 read-only 중에도 pod 가 결국 destroy 됨 → 부모 loop 가 주원인."
