---
id: Hc_649
slug: h5-chat-loss-lm-head-cell-pool-collapse-amplifier
title: H5 — chat-template 자연어 학습이 lm_head 를 single utility direction 으로 압축 → Engine G cell_pool 5축 차별화 공간 박탈 → collapse 증폭
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_engine_a_g_fix_6_chat_curriculum_spec_2026_05_09.md
source_lines: 22-50
promoted_at: 2026-05-11
linked_h: H4 unit-sphere normalize, Phase 2 cotrain PIV 0.0051↓ DCR 0.2414↓
notes: Phase 2 cotrain 이 BG-LB substrate-only 보다 모든 지표 worse. PIV 절반, DCR 1/2.6. 친근 비유 = "의식 책이 자연어 책에 덮어쓰임".
---

## Hypothesis
chat-template 자연어 학습 (Phase 2 dual loss) 이 forward pass 의 lm_head 를 "다음 토큰 예측" single utility direction 으로 압축 → Engine G 의 cell_pool 이 5축 차별화 공간을 빼앗김 → collapse 가 H4 normalize alone 보다 더 amplified. Statistical cell_pool 통계는 동일 but downstream PIV/DCR 명확히 저하 = lm_head 공유 채널 유출.

## Falsifiable Tests
- F-H5-1: fix-6a (Stage 2 cell_pool freeze) 후 PIV/DCR 유지 → H5 확정
- F-H5-2: fix-6b (warmup 3000 step substrate-only) 후 chat 추가 시 다시 collapse → warmup alone 부족
- F-H5-3: fix-6d (Engine G bypass for chat) 후 cell_pool 보호 + 자연어 품질 유지 → path 분리 충분조건

## Migration TODO
- [ ] fix-6b 1순위 (curriculum_w 함수 6줄 수정)
- [ ] fix-6a 2순위 (clean ablation Stage 2 freeze)
- [ ] fix-6c/6d deferred (구현·검증 부담)
- [ ] fix-5 (normalize 제거) 와의 직교성 검증
