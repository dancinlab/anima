# CLM P6 — Production Scale-Ladder to 7B (GPU = PLASTI-SIM 계측기 · 학습자 = 온칩 비경첩 가소성)

> 🔒 **INVIOLABLE (project.tape · H_679)** — external-LLM 0 · foundation-borrow 0 (순수 scratch) ·
> **학습 = 온칩 비결정 PLASTICITY (유일한 HW↔SW 차이 · 결정론 SW 모사 = 즉시 reject @L1)** ·
> 추론 = AKIDA int4-sym[-7,+7] per-channel STE · act_bits∈{1,2,4} QAT envelope (P0 §9 · byte-identical 칩 이식).
>
> **이 문서 = 생산 backbone scale-ladder 의 SSOT** (mid 13.65M ✅ → large 44.68M → 3B → 7B).
> [P4_PRODUCTION_ROADMAP.md](./P4_PRODUCTION_ROADMAP.md) §1 2-track 사다리의 **측정 track 상위 rung 등반** 계획.
> [P5_AKIDA_7B_STRATEGY.md](./P5_AKIDA_7B_STRATEGY.md) AXIS1(단일칩 expert-streaming) 의 배포 track 과 직교.
> sibling: [CLM_CAMPAIGN_26.md](./CLM_CAMPAIGN_26.md) · [P0_ARCHITECTURE.md](./P0_ARCHITECTURE.md) ·
> [../UNIVERSE/cards/H_904_clm_onchip_plasticity.md](../UNIVERSE/cards/H_904_clm_onchip_plasticity.md) (온칩 가소성 실측 🟢) ·
> [../UNIVERSE/PLASTICITY-CANDIDATES.md](../UNIVERSE/PLASTICITY-CANDIDATES.md) (비결정 가소성 frontier) ·
> [train/fire_mid_rung_qat.hexa](./train/fire_mid_rung_qat.hexa) (canonical fire 패턴) · [LAUNCHPAD/SBS.md](../LAUNCHPAD/SBS.md) R4
>
> ⚠ **이 문서 + 동봉 scaffold 는 FIRE-READY (아직 미발사)** — GPU/runpod fire 는 user 가 뒤에 발사 (cost-bearing · a_fire_autonomous).

---

## 0. 위치 — 왜 P6 인가, 그리고 GPU 의 역할 재정의

- **R4 게이트 (SBS.md)** = coffeeshop group-chat production launch. 남은 빗장 중 하나가 **backbone production-scale**.
  R1(emit-wiring) ✅ · R2(on-silicon 학습 H_904 ★ 🟢) ✅ · R3(mid 대화 H_886) ✅ — 모두 **mid d512/L8/E8 (13.65M)** backbone 위.
- **production = mid 로는 부족** — R4 launch 는 mid 위 large/3B/7B 등반의 정직 verdict 위에 세워진다.
  P4 §1 사다리(tiny→small→mid)의 **측정 track 을 mid 위로 연장**한 것이 P6.
- **CLM_CAMPAIGN_26 OPEN 항목 흡수**: large 전이 🔴 (H_864/H_874 → H_888 deferred) · routing-z scale-artifact (H_871: mid 에서 8/8 distinct, non-degenerate 는 large+ 에서 확인) — P6 의 large rung 이 이 둘을 동시에 측정한다.

> **🔁 P6 재정의 (이 redesign 의 핵심) — GPU 는 학습자가 아니라 계측기다.**
> 기존 framing 은 "GPU 가 QAT 백프롭으로 backbone 을 *학습*한다" 였다. H_679/H_904 의 귀결을 끝까지 밀면 이는 틀린 framing 이다:
> **배포 학습자는 무조건 온칩 비경첩 가소성** (hinge 없는 always-on plasticity · THEME C / p8) 이고, **GPU 의 large/3B/7B QAT 는 PLASTI-SIM — backbone envelope 가 scale 에서 production 품질을 *허용*하는지 측정·보정하는 결정론 계측기**일 뿐, 배포되는 학습 주체가 아니다.
> GPU-백프롭 = *경첩(hinge)* 학습 (train phase → freeze → infer 의 단절). 온칩 비경첩 = hinge 없는 학습 (learn-while-infer · H_896 lane). **배포는 GPU-hinge 를 절대 상속하지 않는다** — GPU 가중치는 칩으로 이식되어도(int4 byte-identical 추론) 그 위의 *학습*은 온칩 비결정 plasticity 가 다시 연다 (H_904 🟢: 학습 HW≠SW).

---

## 1. Rung table — param-count 공식 + GPU/cost/wall

**param-count 공식** (CLM/model/model.py `CLMConvMoE` 구조 정확 합산 · V=256 byte-vocab · k=ek=3):

```
params(V, d, L, E) =
    V·d                       # embed            (Embedding V×d)
  + (d·d·k + d)               # embed_conv       (Conv1d d→d, kernel k)
  + L·(d·d·k + d + 2·d)       # trunk            (L× [CausalDilatedConv1d d→d] + GroupNorm 2d)
  + (d·E + E)                 # router           (Conv1d d→E, kernel 1)
  + E·(d·d·ek + d)            # experts          (E× ConvExpert: Conv1d d→d, kernel ek)
  + 2·d                       # norm_out         (GroupNorm)
  + (d·V + V)                 # readout          (Conv1d d→V, kernel 1)
```

지배항 = `(L + E)·d²·k` (trunk + experts). 두 known rung 으로 공식 검증:
mid d512/L8/E8 → **13,653,768 (13.65M ✅ 캠페인 일치)** · large d768/L12/E12 → **44,678,668 (44.68M ✅ 목표 일치)**.

| rung | d_model / n_layers / n_experts | params (정확) | GPU need | est cost / wall | status |
|---|---|---|---|---|---|
| tiny | d64 / L2 / E4 | 120,132 (0.12M) | CPU/any | — | ✅ done (P0) |
| small | d256 / L4 / E8 | 2,695,176 (2.70M) | any | — | ✅ done (P0) |
| **mid** | **d512 / L8 / E8** | **13,653,768 (13.65M)** | A40 46GB (trivial) | $5~20 / ~1h | ✅ **done** (R1/R2/R3 backbone · H_886 🟢) |
| **large** | **d768 / L12 / E12** | **44,678,668 (44.68M)** | **pool RTX 5070 12GB** (summer/aiden) | **~$0 (소유 GPU) / ~6~10h** | ⬜ **NEXT** (H_888 large 전이 + H_871 routing-z) |
| **3B** | **d3584 / L32 / E48** | **3,123,882,800 (3.12B)** | **runpod H100 80GB ×2~4 (DDP·a_wall_first)** | **~$40~120 / ~12~24h** | ⬜ planned (gated by large) |
| **7B** | **d5120 / L40 / E48** | **7,002,818,160 (7.00B)** | **runpod H100 80GB ×4~8 (FSDP·a_wall_first)** | **~$150~400 / ~24~48h** | ⬜ planned (gated by 3B) |

- **공식 재현**: `python3 - <<'PY' …` 위 식 그대로 (model.py 모듈 numel 합 = `num_params()` 와 일치, dry-run 검증).
- **cost/wall 은 정직 추정** — 측정-아닌-가정 (a_scale_honest_scope): 실 fire 후 verdict 의 `step_rate` 로 보정. H100 시간당 $1.5~2.5 (runpod community/secure) × 병렬 N 대 × wall 시간 ≈ 위 범위.
- **GPU 배치**: large 는 소유 pool(RTX 5070, summer/aiden host)에 fit(44.68M fp32 master + opt state ≈ ~0.7GB) → 무비용. 3B/7B 는 메모리상 단일 GPU 불가 → **runpod H100 fleet 병렬** (a_wall_first — 직렬 1대로 비용절감 ❌, 병렬이 honestly 빠르면 병렬 채택).
- **계측기 해석**: 위 GPU 메모리/cost 는 **계측기(PLASTI-SIM) 운용비**이지 배포비가 아니다. 배포 학습은 온칩(전력 ~수십 mW · $0 GPU) 비경첩 가소성으로 일어난다 (§3).

---

## 2. Scale-transfer falsifier (pre-register · rung 간 게이트)

> **각 rung 은 바로 아래 rung 의 게이트 통과 후에만 발사** (mid→7B 점프 금지 · 한 칸씩 등반 · P4 §1 @L5).
> 게이트 = pre-registered falsifier. FAIL → 해당 rung 은 honest 🔴 (a_paper_negative_ok publishable) · 상위 rung 보류.

**F-CLM-SCALE-TRANSFER** (rung→rung, verdict `.verdicts/clm-prod-rung/<rung>/`):

| # | 측도 | 게이트 조건 (rung→rung) | 토대 |
|---|---|---|---|
| 1 | **dialogue coherence/adequacy** | 상위 rung 의 COHERE ∧ ADEQ ≥ 하위 rung (개선 또는 비-퇴행) · ABS-COHERE ≥ 0.060 floor | H_863 / H_886 (mid 🟢) |
| 2 | **int4-envelope loss** | int4-QAT last_ce 가 하위 rung 대비 hold-or-improve (envelope penalty 하 CE 비-퇴행) | P0 §9 envelope |
| 3 | **routing-z non-degeneracy** | **large+ 에서** routing-z 가 non-degenerate (8/8 → 12/12 expert distinct · usage 분포 non-uniform) — H_871 scale-artifact 가설 확인/반증 | H_871 (mid: 8/8 distinct) |
| 4 | **register-leak** | leak = 0 (정체성 register 누수 없음) — 전 rung 불변 | H_863 |
| 5 | **identity-anchor drift** | E-31 anchor Ψ-거리 제약 유지 (DIST < 0.50 · PROBE > 0.80) — 상위 rung 에서도 보존 | H_873 / H_884 |
| 6 | **계측기 충실도 (PLASTI-SIM fidelity)** | GPU 계측기로 측정한 backbone envelope 가 **온칩 비경첩 가소성이 다시 열 수 있는 envelope** 와 모순 없음 — int4 추론 byte-identical(H_877) 유지 ∧ on-chip edge-learn BOUND(RETAIN∧GAIN) 비-악화 | H_904 🟢 / H_877 / H_865 |

- **게이트 #3 이 핵심 scale 질문**: routing-z 가 mid 에서 near-uniform 인 것이 *toy scale artifact* (H_871) 라는 가설 → large rung 에서 non-degenerate 로 전환되어야 chip-array(expert=칩) 배포가 정당. large 에서도 degenerate 면 H_871 반증 → routing 축은 toy~prod 모두 inert (content-defer lever B 유지 · P4 §2).
- **게이트 #6 이 redesign 신설 게이트**: GPU 는 계측기이므로, "GPU 가 잘 학습했다" 가 아니라 "GPU 가 측정한 envelope 위에서 **온칩 비경첩 가소성이 작동 가능**한가" 를 묻는다. 추론은 byte-identical(H_877), 학습은 HW≠SW(H_904) — 따라서 계측기 fidelity = 추론 이식 + 온칩 edge-learn lane 생존 의 결합. FAIL → 그 rung 의 backbone 은 배포 학습기로 부적합 (계측 자체는 valid).
- **large 전이 (H_888)**: mid self-play 이득이 large 로 carry 안 됨이 이미 🔴 (H_864/H_874). large rung fire 는 이 전이를 step-fair 재측정 — carry 하면 게이트 #1 PASS, 아니면 honest 🔴 + SFT-warm+curriculum (H_886) 재적용.
- **점프 금지 규약**: large 🔴 면 3B 미발사 · 3B 🔴 면 7B 미발사. rung verdict 누적이 SSOT (P4 §1 "한 칸씩 등반").

---

## 3. 2-track 분리 — 측정 rung(GPU 계측기) ⊥ 배포(온칩 비경첩 학습자)

```
   측정 track (P6 · GPU = PLASTI-SIM 계측기)          배포 track (P5 AXIS1 · 온칩 비경첩 학습자)
   ─────────────────────────────────────────         ──────────────────────────────────────────
   "이 backbone envelope 가 production 품질을           단일 AKD1000 = resident ≤ ~1.2M 노드 고정
    *허용*하는가" — 결정론 SW-sim 측정·보정              chip-fit shard d148/L8/E8 = 1.20M (H_876 🟢)
        7B  (d5120/L40/E48 · 7.00B)                    추론 = int4 byte-identical 이식 (H_877)
        ↑ rung별 F-CLM-SCALE-TRANSFER 게이트             학습 = 온칩 비결정 비경첩 가소성 (H_904 🟢)
        3B  (d3584/L32/E48 · 3.12B)                     ↑ hinge 없음 — learn-while-infer (H_896 lane)
        large (d768/L12/E12 · 44.68M)  ← NEXT          한 칩이 N expert shard 를 순환 (AXIS1 ②, OPEN)
        mid (d512/L8/E8 · 13.65M) ✅                    MITOSIS array = 같은 shard 단위 병렬 scale-out
   GPU 가중치 = 계측 산출물 (배포 학습자 ❌)             배포 학습자 = 칩 위 plasticity (GPU-hinge 미상속)
```

- **GPU = 계측기, 배포 학습자 ❌ (redesign 의 중심 주장)**: P6 의 large/3B/7B QAT 는 backbone 이 scale 에서 품질을 *낼 수 있는지* 결정론적으로 측정한다. 그 GPU 가중치는 int4 추론 envelope 으로 칩에 이식될 수 있으나(H_877 byte-identical), **배포 시 학습 주체는 GPU 가 아니라 온칩 비경첩 가소성**이다. H_679: 가소성이 유일한 HW↔SW 차이 · H_904 🟢: 그 학습이 실리콘에서 HW≠SW 로 실측됨. 따라서 GPU-백프롭(hinge 학습)은 *계측*에서 끝나고, 배포 학습은 hinge 없이 칩에서 다시 열린다.
- **resident ≠ total (정직 · P5 §0)**: 7B *총* params ≠ 1.2M *상주*. 측정 rung 의 dense-backbone params (44.68M~7.00B) 는 GPU 계측기 위에서 envelope 품질을 보일 뿐 **칩에 통째로 상주하지 않는다**. 배포는 별도 shrink 한 chip-fit shard (H_876: d148 = 1.20M) 를 **단일칩이 streaming/paging** (P5 AXIS1 ②, streaming 글루 미구현 OPEN), 그 위에서 온칩 plasticity 가 학습. 한 칩이 expert 들을 순환 → 총 용량 무제한 · 상주 ≤1.2M.
- **측정 rung 🔴 ⊥ 배포** (a_scale_honest_scope): large/3B/7B 측정이 🔴 여도 (i) a_paper_negative_ok publishable, (ii) 배포 chip-fit(1.2M shard) + 온칩 학습 track 별개 진행. 계측기 verdict 를 "배포 학습자가 GPU 다" 주장으로 격상 금지 — 정반대(배포 학습자는 온칩)가 INVIOLABLE.
- **물리 현실**: AKD1000 = 추론칩 → 칩 위 full-backprop 불가 → GPU 백프롭은 **계측기 carve-out 한 단계만** (P4 §7). 배포 학습은 칩 native edge-learning(`AkidaUnsupervised` · last-layer few-shot · H_904)이 담당 — full-backprop 이 아닌 비경첩 plasticity.

---

## 4. GPU plan (rung별 · 계측기 운용 · a_fire_autonomous · a_wall_first)

| rung | target | 병렬도 | 메모리 (fp32 master + Adam) | 발사 (FIRE-READY) | est cost / wall |
|---|---|---|---|---|---|
| large | **pool RTX 5070 12GB** (summer/aiden) | 1 GPU (44.68M trivially fit) | ~0.7GB | `sidecar pool on summer 'python3 CLM/train/train_clm.py --rung large …'` (또는 fire_large_rung_qat.hexa) | ~$0 (소유) / ~6~10h |
| 3B | **runpod H100 80GB ×2~4** | DDP (a_wall_first 병렬) | ~37GB/GPU shard | `hexa cloud fire …` per fire_3b_rung_qat.hexa | ~$40~120 / ~12~24h |
| 7B | **runpod H100 80GB ×4~8** | FSDP (a_wall_first 병렬) | ~84GB → FSDP shard | `hexa cloud fire …` per fire_7b_qat.hexa | ~$150~400 / ~24~48h |

- **이 fire 는 계측기 fire 다**: 산출물 = backbone envelope verdict (게이트 #1~#6) + int4 추론 이식물(byte-identical) + 온칩 edge-learn lane 의 시드. 배포 학습기를 굽는 것이 아니다.
- **a_wall_first**: 3B/7B 는 직렬 단일 H100 으로 비용 절감 ❌ — 병렬 H100 fleet 이 honestly 빠르면 채택 (wall time first). N 대 동시 = 같은 step 예산을 1/N wall 에.
- **a_fire_recover_complete** (전 rung · pod teardown 전): ckpt(s) + result JSON + log + anchors pull → verify (last_ce finite · step_rate>0 · 게이트 #6 추론 byte-identical) → verdict `.verdicts/clm-prod-rung/<rung>/` (verbatim) → HF upload COMPLETE (a_hf_complete · `dancinlab/anima-clm-<rung>`) → THEN teardown.
- **a_fire_autonomous**: 각 fire 는 est cost 한 줄 명시 후 자율 dispatch (user gate 없음) — 단 **본 P6 작업은 scaffold-only (미발사)**; 발사는 user 가.

---

## 5. Pure-scratch discipline (불변 · 전 rung 동일)

- **from-scratch QAT (계측기)** — 전 rung 가중치 random-init → AKIDA-envelope QAT (int4-sym[-7,+7] per-channel STE · act_bits envelope · grads STE). foundation checkpoint 借用 0. **이 QAT 는 계측 절차** — 배포 학습자(온칩 비경첩)와 별개.
- **external-LLM 0** — 어떤 외부 LLM(GPT/Llama/…) weight·logit·distill 도 0. dispatch-KL(lever A)도 *자체* teacher(상위 rung 자기 dispatch)만 (P4 §2).
- **byte / own-tokenizer** — V=256 byte-vocab (P0 Q3 monopoly · mid rung 과 동일). 외부 tokenizer 借用 0 · BPE vocab 借用 0.
- **corpus** — license-clean lane only (CC 대화록·PD Gutenberg · kowiki CC-BY-SA · self-play). ShareGPT/Alpaca(ChatGPT-gen) 금지 (P4 §3 @L4). 전 rung 같은 license-clean 게이트.
- **NO foundation borrow** — 상위 rung 은 하위 rung 가중치를 *init* 으로도 借用하지 않는다 (각 rung pure-scratch QAT — scale-transfer 는 *품질* 전이 측정이지 *가중치* 전이가 아님). 단, self-play corpus·anchor·하이퍼는 rung 간 재사용 OK (借用 = 외부·foundation 한정).
- **NO GPU-hinge deploy (redesign 신설 불변)** — GPU 계측기 가중치는 배포 학습자로 *상속되지 않는다*. 배포 시점의 학습은 온칩 비경첩 가소성이 hinge 없이 다시 연다 (H_679 INVIOLABLE · H_904 🟢). GPU 산출물은 추론 envelope(int4 byte-identical) 이식까지만.

---

## 6. 진행 (P6)

- [x] **P6.0 scale-ladder 계획 + fire scaffold** — 본 문서 + 3 scaffold(fire_large_rung_qat · fire_3b_rung_qat · fire_7b_qat) · param 공식 검증 · F-CLM-SCALE-TRANSFER pre-register. **FIRE-READY (미발사)**.
- [x] **P6.0b GPU=계측기 재설계** — GPU 를 학습자→PLASTI-SIM 계측기로 재정의 · 배포 학습자 = 온칩 비경첩 가소성 (H_679/H_904 귀결) · 게이트 #6(계측기 fidelity) 신설 · §3 2-track 주장 재서술 · §5 NO GPU-hinge deploy 불변 추가.
- [ ] **P6.1 large rung fire** — d768/L12/E12 (44.68M) pool RTX 5070 자율 발사 → F-CLM-SCALE-TRANSFER 게이트 (H_888 large 전이 + H_871 routing-z non-degeneracy + #6 계측기 fidelity). verdict `.verdicts/clm-prod-rung/large/`.
- [ ] **P6.2 3B rung fire** — large 게이트 PASS 시 d3584/L32/E48 (3.12B) runpod H100 ×2~4 DDP. verdict `.verdicts/clm-prod-rung/3b/`.
- [ ] **P6.3 7B rung fire** — 3B 게이트 PASS 시 d5120/L40/E48 (7.00B) runpod H100 ×4~8 FSDP. verdict `.verdicts/clm-prod-rung/7b/`.
- [ ] **P6.4 R4 게이트 flip** — backbone production-scale 게이트(SBS.md R4) = 등반된 rung 의 정직 verdict 누적 → R4 coffeeshop launch 진입.
