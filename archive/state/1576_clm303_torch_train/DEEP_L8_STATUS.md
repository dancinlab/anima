# 딥-ConvMoE 303M (L8 d2781) 학습 — 진행 status (2026-06-27 ground-truth)

summer(`summer-B650M-K`) `~/anima_train_303m/out_303m/` ground-truth (pool on summer):

- **ckpt**: `clm303_deep_L8_d2781.pt` (1.2GB torch, **L8 deep · E2/MoE · d2781**)
  - sha256 `69ac4e340d3d323a4f340575c67f6dfbc9bf40e18599b7e3b7189d37c3fea01b`
  - 저장 step 12000/15000 (~80%)
- **학습 건강**: CE 1.37 · **val_CE 1.402 · gap +0.035** (val≈train, **overfit 아님** — clm303 L4 암기와 대조). dropout 0.25→0.22 + wd anneal (savant golden-zone inhibition).
- **마지막 로그 step ~12400, 01:16 (≈1h 전) 정지** — 프로세스/tmux 없음, GPU idle. 15000 목표 미달(~83%)에서 중단(summer load 15·11users 경합 또는 크래시 추정).
- **미완 (depth 질문 UNANSWERED)**: `.pt`만 존재 — ❌ `.clm` v0.2 직렬화 · ❌ held-out DESCENT 게이트 · ❌ engine-native G1 multiseed. "L8 깊이가 clm303 L4의 G1(C2 재조합) 벽을 뚫나"는 이 3단계를 해야 답.
- **보존**: summer /home 영구디스크(재부팅 생존). HF 푸시는 summer 외부 DNS 불가로 차단 — 영구 등록 필요 시 (a) summer→로컬망 rsync→mini→HF, 또는 (b) DNS 되는 호스트로 ckpt 이동 후 push.
- **NEXT (finalize)**: serialize `verify_clm_v2.py` → `.clm` → `descent <clm> <ko/en heldout>` DESCENT PASS → `anima eval` G1 multiseed(7/4302/4303) vs L4 frozen bar. summer CPU는 현재 H_1597 G6 corpus-grounded probe(aeea05) 점유 중 → 그 후 또는 별도 호스트.
