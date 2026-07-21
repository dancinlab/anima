# H_9838 — 해마 CA3 의 다단계 전이완성을 학습에 넣는다 — A→B, B→C 로부터 A→C (R12-1 · 🥇)

**status:** 🧭 PROPOSED (R12 · **DIRECTIONAL 설계**, 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측 (카드 작성 전 `origin/main` 에서 직접 읽음)

`core/hippo_lane.py`(133줄 · H_9129 rung-3)는 실재한다: `dg_decorrelate`(center_zscore 화이트닝) →
`hippo_kwta`(치아이랑 kWTA 희소부호화 = 패턴분리) → `hippo_build_store` → `hippo_relatedness`
(CA3 이질연합 저장소의 **다단계 패턴완성** = 전이적 연쇄). numpy 순수 산술 · torch/FFI 없음.

## 왜 이것이 1순위인가

CE(다음 바이트 맞히기)가 **구조적으로 못 주는 연산**을 준다: A→B 와 B→C 만 본 상태에서 A→C 를
복원하는 것 = 재조합이 요구하는 바로 그 연산. 이미 학습되는 CLMS store lane 과 **상보**다 —
store 는 *주소별 값 운반*(H_9775 확증), CA3 는 *주소들 사이의 전이*. 겹치지 않는다.

## ⚠️ 이 카드의 본체는 아이디어가 아니라 설계비용

파일 헤더가 명시한다: **"READ-ONLY relatedness READOUT — it never mutates the emit-drive lane
(Ψ / motivation / recall_thr / generator). Adding/consulting it therefore cannot change
generation bytes (`a_substrate_disjoint`: separation = preservation)."**

⟹ 학습에 넣으려면 **쓰기 경로를 신설**해야 하고, 그 순간 이 모듈이 안전한 이유(분리)가 깨진다.
`a_substrate_disjoint` 는 LAW 다("separation = preservation, overlap = conflict"). 따라서 설계는
**분리를 유지한 채** 학습신호를 뽑는 형태여야 한다 — CA3 완성 결과를 **보조 타깃**으로만 쓰고
emit-drive 경로에는 되먹이지 않는 단방향 배선.

## Intervention (flag 형태 · 미구현)

```
anima-py train --hippo-aux <weight> --hippo-kwta-k <k> --hippo-hops {1,2,3} \
               --hippo-writeback off      # off = 분리 유지(기본·필수) · on = LAW 위반 검사용 팔
```

CA3 가 완성한 A→C 쌍을 보조 CE 타깃으로. `--hippo-hops` 가 조작변인(1홉=직접학습된 것, 2~3홉=전이).

## Arms + controls

| arm | 읽는 법 |
|---|---|
| `--hippo-hops 1` | **양성통제** — 직접 쌍이므로 반드시 올라야. 안 오르면 INSTRUMENT-DEAD |
| `--hippo-hops 2,3` | 주 DV — 전이 완성이 held-out 재조합을 올리는가 |
| kWTA 무력화(k=전체) | 패턴분리 제거 → 붕괴해야 (기전 확증) |
| 값 셔플 store | 붕괴해야 |
| `--hippo-writeback on` | LAW 위반 팔 — 생성 바이트가 바뀌는지 **감시용**, 채택 아님 |

## $0 스크리너

H_9815 토이(4kB·6분)에 A→B,B→C 만 넣고 A→C 를 held-out. `hippo_relatedness` 가 numpy 라
ckpt 없이 바로 돌린다. hp(단항) 유지 ∧ 전이 held-out 상승 ∧ kWTA-off 붕괴 = 통과.

## 판독가능성

토이 = **오늘 (b)** · 303M ρ·weave terminal = **(a) H_9827 패널수리(n=212) 선행**.

**related:** H_9129 · H_9775 · H_9830 · H_9833 · H_9827
