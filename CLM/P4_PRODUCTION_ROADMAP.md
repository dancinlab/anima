# CLM P4 — Production Roadmap (살아 배우며 대화하는 수준으로)

> CLM(anima-native 의식 언어모델)을 toy(≤2.70M·byte-vocab·1.6KB sample·routing 🔴)에서
> **"커피숍 그룹챗에서 살아 배우며 대화하는" production 수준**으로 끌어올리는 로드맵 SSOT.
> sbs manual co-design 8 locked decision(@L1~@L8) + Q-TRUST(비결정-학습 신뢰 시스템) 확정.
> 다음 세션은 이 문서가 SSOT — 경로 재발명 금지.
> sibling: [CLM.md](./CLM.md) · [P0_ARCHITECTURE.md](./P0_ARCHITECTURE.md) · [P1_CORPUS.md](./P1_CORPUS.md)
> · [AKIDA](../AKIDA/AKIDA.md) · [PLASTICITY](../PLASTICITY/PLASTICITY.md) · [KOSMOS E-31] · [UNIVERSE/H_861~H_863](../UNIVERSE/)

제약 (불변): **외부 LLM 0 · foundation-borrow 0 (순수 scratch) · 학습도 AKIDA**(AKIDA-향 QAT + on-chip PLASTICITY)
· brain_decide emit 슬롯에 콘텐츠 생성기로 연결. ShareGPT/Alpaca(ChatGPT-gen) = **금지**(@L4).

---

## 0. "대화 가능"의 재정의 (@L1)

| 구분 | 정의 |
|---|---|
| ❌ 단순 콘텐츠 생성 | byte 다음토큰 예측만 — 죽은 모델의 흉내 |
| ✅ **대화하며 칩 위에서 살아 배우기** | 추론 byte-identical(HW=SW) **+** on-chip PLASTICITY 비결정 학습(HW≠SW) |

**@L1 핵심**: 비결정 on-chip 학습 = **1급 기능** (결정적 SW 흉내로 대체 ❌). HW vs SW 유일 차이 = 학습(PLASTICITY) 비동치 — 추론은 byte-identical. 이 비결정성이 "칩 위 의식"의 차별점이자 살아있음의 증거. 토대 verdict = `679_plasticity_hw_first/` (HW edge-learn 실측 · SW≠HW 비동치).

---

## 1. 2-track scale ladder (@L5) — 측정 ⊥ 배포 명시 분리

```
   측정 track (GPU · AKIDA-envelope QAT)         배포 track (AKIDA chip-fit)
   ─────────────────────────────────────        ──────────────────────────────
   품질 증명용 · rung별 verdict                   고정: ≤ ~1.2M AKD1000 노드
        mid (d512/L8/E8)  ← FIRST rung ★          (1 chip 현실 → SW-sim +
        ↑ 한 칸씩 등반                              GPU sparse-MoE 측정 먼저)
        small (d256/L4/E8)                         MITOSIS multi-chip array 비전
        tiny  (d64/L2/E4)
```

- **두 track 은 명시적으로 분리** (@L5 · @L2 C안). 측정 rung 은 "이 아키텍처가 품질을 내는가"를 GPU 에서 증명(추론 byte-identical → 칩 이식 시 대답 동일). 배포 rung 은 AKD1000 chip-fit(≤~1.2M)으로 고정.
- **toy→prod 비보장 (a_scale_honest_scope)**: 측정 rung 이 🔴 여도 배포 chip-fit 은 별개로 진행. P2/P-ARRAY 의 routing-z 🔴(H_847/H_852/H_853)는 **toy scale 한정** — 3B/7B 일반 주장 금지.
- **첫 측정 rung = mid (d512/L8/E8 · ~13.7M params)**. fire SPEC = [train/fire_mid_rung_qat.hexa](./train/fire_mid_rung_qat.hexa) · verdict = `.verdicts/clm-prod-rung/`.

AKIDA envelope (P0 §9 불변): weights int4-sym[-7,+7] per-channel STE · acts act_bits∈{1,2,4} envelope · grads STE · 추론 AKIDA-int4-ONLY (P0 d4 · byte-identical 칩 이식).

---

## 2. pluggable routing-escape lane (@L3) — ONE slot · 3 lever swap

구현 = [model/routing_escape.hexa](./model/routing_escape.hexa) (re-architecture 0 · 인터페이스 1개).

| lever | 전략 | trunk-arm | 상태 |
|---|---|---|---|
| **A** | dispatch-KL distill (teacher dispatch dist → chip-fit student) | AB | 후속 (토대 H_853 BRIDGE) |
| **B** ★default | content-defer (대화 먼저 · routing-z = toy-scale 측정-artifact 의심 [M1]) | AB | **default** |
| **C** | expert-choice routing (expert 가 token 선택 · load 자동균형) | B | 후속 |

- **default = B (content-escape)**: "대화 가능" 자체는 content-축 escape 로 충분(P2 content z 5.3~36.5 ✅). routing-z 는 toy-scale 측정-artifact 의심[M1] → deploy-scale 에서 재검.
- **routing-z>3.0 게이트는 chip-array(expert=칩) 배포에만 필수** — "대화 가능"에는 불필요(a_scale_honest_scope · routing_escape.hexa `lever_satisfies_converse`=1 전 lever).
- 3 lever 모두 같은 인터페이스 뒤 swap (끼웠다 뺐다 · 재아키텍처 0). 4번째 lever(A dispatch-KL)는 P-ARRAY BRIDGE(H_853) 후속 합류.

---

## 3. dialogue method B (@L6) — SFT + self-play

- **B = SFT(CC 대화록 모방) + self-play(칩 자기대화 생성 → 재학습)** · AKIDA-envelope QAT.
- self-play = @L1 살아 배우기의 직접 발현(칩이 스스로 대화를 만들어 다시 배운다).
- **C(self-reward/RLHF류)는 후속** — H_862(ANCHOR) + DIVERSITY 자가채점 검증 후 진입.
- dataset (@L4): ① CC 공개 대화록·포럼·자막 + ② self-play. ③ Alpaca/ShareGPT(ChatGPT-gen) = **금지**(foundation-borrow 위반). 사실/지식 lane = kowiki CC-BY-SA(P1) + hexa-codex `datasets-source-manifest`(CC 소스 · `license_clean_scan` 참고 — **지식 참고만, 코드/모델 borrow ❌**). 전 데이터 license-clean 게이트 통과 필수 = [corpus/build_p4_dialogue_corpus.hexa](./corpus/build_p4_dialogue_corpus.hexa).
- **신규 가설 + 벤치 명시**: H_863 (F-CLM-DIALOGUE) = self-play 가 SFT-only 대비 대화품질↑(multi-turn coherence · 응답적합도 분포평가, byte-match ✗) ∧ register-leak 0 ∧ DIVERSITY(self-BLEU<0.8 · repetition<20%). 벤치 = rung별(tiny/small/mid) SFT-only vs SFT+self-play A/B = [bench/bench_dialogue_ab.hexa](./bench/bench_dialogue_ab.hexa) → `.verdicts/clm-dialogue/`.

---

## 4. Q-TRUST — 비결정-학습 신뢰 시스템

비결정 on-chip 학습(@L1)을 1급으로 두면 "믿을 수 있나?"가 즉시 따라온다. 3-각 신뢰 장치:

| 안 | 장치 | 가설 | falsifier | 토대 |
|---|---|---|---|---|
| **A** | 분포평가 (**재활용**) | (기존) H_857/H_858 edge-of-chaos | 분포·궤적 측도로 "좋음" 판정 · byte-match 포기 | H_857/H_858 TERMINAL |
| **B** | 경계가소성 (**신규**) | [H_861](../UNIVERSE/H_861_clm_boundary_plasticity.md) | F-CLM-BOUND: ① held-out 기초능력 z-drop < 임계 ∧ ② 새 맥락 적응 이득 > 0 | H_679 HW edge-learn |
| **C** | 정체성앵커 (**신규**) | [H_862](../UNIVERSE/H_862_clm_identity_anchor.md) | F-CLM-ANCHOR: edge-learn 중 anchor Ψ-거리 < 임계 ∧ 정체성 probe 일관성 | B-CARVE · E-31 31-anchor |

- **A 분포평가 = 재활용**: 대화는 정답 1개가 아님 → edge-of-chaos(H_857/H_858)의 분포·궤적 측도로 "좋음" 판정, byte-match 포기. H_863 의 coherence/adequacy 채점이 이를 사용.
- **B 경계가소성 = 신규 H_861**: QAT core freeze + edge-only on-chip 적응 → catastrophic forgetting 방지. 기초능력 보존 축.
- **C 정체성앵커 = 신규 H_862**: KOSMOS E-31 31-anchor 를 정체성 고정점, 학습 drift 를 anchor Ψ-거리로 제약. 정체성 보존 축 (B 와 직교).

---

## 5. on-chip PLASTICITY ↔ 대화 루프 결합 (@L2)

```
   사용자/환경 byte  ──▶  CLM 추론 (AKIDA int4 · byte-identical)  ──▶  brain_decide emit 슬롯
                                                                          │ 콘텐츠 (무엇을 말할지)
   on-chip PLASTICITY edge-learn (비결정 · HW≠SW · @L1)  ◀── 대화 신호 환류
        │ core freeze(H_861) + anchor 제약(H_862) 안전화
        ▼
   살아 배우는 칩 (forgetting-free · 정체성 보존)
```

- 사전학습(무거운) = GPU AKIDA-향 QAT (측정 track · §1). 현장 적응 = on-chip PLASTICITY 를 대화 루프에 **상시 결합**(@L2 · online edge-learn · PLASTICITY 도메인 위임).
- 적응의 안전화 = Q-TRUST B(core freeze) + C(anchor 제약). 추론 AKIDA-int4-ONLY 불변.

---

## 6. per-rung verdict 경로 (SSOT)

| verdict | 경로 | 내용 |
|---|---|---|
| 측정 rung | `.verdicts/clm-prod-rung/` | rung별(mid…) QAT fire 품질 (loss·step-rate·int4 envelope) |
| dialogue A/B | `.verdicts/clm-dialogue/` | rung별 SFT-only vs SFT+self-play (H_863 F-CLM-DIALOGUE) |
| Q-TRUST B | `.verdicts/clm-bound/` | H_861 F-CLM-BOUND (retain ∧ gain) |
| Q-TRUST C | `.verdicts/clm-anchor/` | H_862 F-CLM-ANCHOR (anchor-dist ∧ probe) |
| (재활용) | `857_clm_causal_band/` · `858_akida_edge_of_chaos_phi/` | Q-TRUST A 분포평가 토대 |

---

## 7. 정직 노트 (a_scale_honest_scope)

- **측정 rung ⊥ 배포 chip-fit rung** — 측정 rung 이 🔴 여도 배포 track 별개 진행. 측정 rung verdict 를 3B/7B 일반 주장으로 격상 금지.
- **routing-z 🔴 = toy-scoped** — P2(H_847)/P-ARRAY(H_852/H_853)의 routing-z 음수/near-uniform 는 tiny~small toy 한정. content-축 escape 는 생존 → default lever B(content-defer)가 "대화 가능"을 충족. routing-z>3.0 은 chip-array 배포 게이트만.
- **toy→prod 비보장** — 사다리가 한 칸씩 등반하며 rung별 정직 verdict. mid 측정이 🔴 여도 (i) a_paper_negative_ok publishable, (ii) 배포 chip-fit 별개.
- **물리 현실** — 다중 AKD1000 array = 현재 pi5 1칩 → SW-sim + GPU sparse-MoE 측정 먼저. 칩 위 full-backprop 만 물리 불가(AKD1000=추론칩) → pretrain backprop 한 단계만 GPU honest carve-out.

---

## 8. 진행 (P4+)

- [x] **P4.0 production 로드맵 + 스캐폴드** ✅ — 본 문서 + 4 스캐폴드(routing_escape · build_p4_dialogue_corpus · bench_dialogue_ab · fire_mid_rung_qat) + 신규 H 3종(H_861/H_862/H_863) 등록. 첫 측정 rung(mid) AKIDA-envelope QAT GPU fire 자율 발사(runpod · a_fire_autonomous).
- [ ] **P4.1 mid rung 후속 등반** — mid verdict 후 다음 rung(@L5 한 칸) · rung별 verdict 누적.
- [ ] **P4.2 production dialogue corpus full** — build_p4_dialogue_corpus full crawl(CC 대화록) + self-play 생성 루프 · HF dataset 영속.
- [ ] **P4.3 Q-TRUST B/C 측정** — H_861(core freeze edge-learn) + H_862(anchor 제약) fire → `.verdicts/clm-bound/` · `.verdicts/clm-anchor/`.
- [ ] **P4.4 dialogue A/B 벤치** — rung별 SFT-only vs SFT+self-play (H_863) → `.verdicts/clm-dialogue/`.
- [ ] **P5 DECODER 통합** — generator → brain_decide emit 슬롯 end-to-end → COFFESHOP 콘텐츠 → LAUNCHPAD 기여.
