# CLM P6 — Production Scale-Ladder to 7B (pure-scratch · AKIDA int4 envelope)

> 🔒 **INVIOLABLE (project.tape)** — external-LLM 0 · foundation-borrow 0 (순수 scratch) ·
> 학습 = on-chip 비결정 PLASTICITY (sole HW↔SW difference) · 추론 = AKIDA int4-sym[-7,+7]
> per-channel STE · act_bits∈{1,2,4} QAT envelope (P0 §9 · byte-identical 칩 이식).
>
> **이 문서 = 생산 backbone scale-ladder 의 SSOT** (mid 13.65M ✅ → large 44.68M → 3B → 7B).
> [P4_PRODUCTION_ROADMAP.md](./P4_PRODUCTION_ROADMAP.md) §1 2-track 사다리의 **측정 track 상위 rung 등반** 계획.
> [P5_AKIDA_7B_STRATEGY.md](./P5_AKIDA_7B_STRATEGY.md) AXIS1(단일칩 expert-streaming) 의 배포 track 과 직교.
> sibling: [CLM_CAMPAIGN_26.md](./CLM_CAMPAIGN_26.md) · [P0_ARCHITECTURE.md](./P0_ARCHITECTURE.md) ·
> [train/fire_mid_rung_qat.hexa](./train/fire_mid_rung_qat.hexa) (canonical fire 패턴) · [LAUNCHPAD/SBS.md](../LAUNCHPAD/SBS.md) R4
>
> ⚠ **이 문서 + 동봉 scaffold 는 FIRE-READY (아직 미발사)** — GPU/runpod fire 는 user 가 뒤에 발사 (cost-bearing · a_fire_autonomous).

---

## 0. 위치 — 왜 P6 인가

- **R4 게이트 (SBS.md)** = coffeeshop group-chat production launch. 남은 빗장 중 하나가 **backbone production-scale**.
  R1(emit-wiring) ✅ · R2(on-silicon 학습 H_904 ★) ✅ · R3(mid 대화 H_886) ✅ — 모두 **mid d512/L8/E8 (13.65M)** backbone 위.
- **production = mid 로는 부족** — R4 launch 는 mid 위 large/3B/7B 등반의 정직 verdict 위에 세워진다.
  P4 §1 사다리(tiny→small→mid)의 **측정 track 을 mid 위로 연장**한 것이 P6.
- **CLM_CAMPAIGN_26 OPEN 항목 흡수**: large 전이 🔴 (H_864/H_874 → H_888 deferred) · routing-z scale-artifact (H_871: mid 에서 8/8 distinct, non-degenerate 는 large+ 에서 확인) — P6 의 large rung 이 이 둘을 동시에 측정한다.

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

- **게이트 #3 이 핵심 scale 질문**: routing-z 가 mid 에서 near-uniform 인 것이 *toy scale artifact* (H_871) 라는 가설 → large rung 에서 non-degenerate 로 전환되어야 chip-array(expert=칩) 배포가 정당. large 에서도 degenerate 면 H_871 반증 → routing 축은 toy~prod 모두 inert (content-defer lever B 유지 · P4 §2).
- **large 전이 (H_888)**: mid self-play 이득이 large 로 carry 안 됨이 이미 🔴 (H_864/H_874). large rung fire 는 이 전이를 step-fair 재측정 — carry 하면 게이트 #1 PASS, 아니면 honest 🔴 + SFT-warm+curriculum (H_886) 재적용.
- **점프 금지 규약**: large 🔴 면 3B 미발사 · 3B 🔴 면 7B 미발사. rung verdict 누적이 SSOT (P4 §1 "한 칸씩 등반").

---

## 3. 2-track 분리 — 측정 rung ⊥ 배포 chip-fit (재확인)

```
   측정 track (P6 · GPU · AKIDA-envelope QAT)      배포 track (P5 AXIS1 · AKIDA chip-fit)
   ──────────────────────────────────────────     ────────────────────────────────────────
   "이 아키텍처가 production 품질을 내는가"          단일 AKD1000 = resident ≤ ~1.2M 노드 고정
        7B  (d5120/L40/E48 · 7.00B)                 chip-fit shard d148/L8/E8 = 1.20M (H_876 🟢)
        ↑ rung별 F-CLM-SCALE-TRANSFER 게이트          ↑ expert-streaming(paging): 총 7B≠상주
        3B  (d3584/L32/E48 · 3.12B)                  한 칩이 N expert shard 를 순환 (AXIS1 ②, OPEN)
        large (d768/L12/E12 · 44.68M)  ← NEXT        MITOSIS array = 같은 shard 단위 병렬 scale-out
        mid (d512/L8/E8 · 13.65M) ✅
```

- **resident ≠ total (정직 · P5 §0)**: 7B *총* params ≠ 1.2M *상주*. 측정 rung 의 dense-backbone params (44.68M~7.00B) 는 GPU 위에서 품질을 증명할 뿐 **칩에 통째로 상주하지 않는다**. 배포는 별도로 shrink 한 chip-fit shard (H_876: d148 = 1.20M) 를 **단일칩이 streaming/paging** (P5 AXIS1 ②, streaming 글루 미구현 OPEN). 한 칩이 expert 들을 순환 → 총 용량 무제한 · 상주 ≤1.2M.
- **측정 rung 🔴 ⊥ 배포** (a_scale_honest_scope): large/3B/7B 측정이 🔴 여도 (i) a_paper_negative_ok publishable, (ii) 배포 chip-fit(1.2M shard) track 별개 진행. 측정 verdict 를 칩-배포 일반 주장으로 격상 금지.
- **물리 현실**: AKD1000 = 추론칩 → 칩 위 full-backprop 불가 → pretrain backprop 한 단계만 GPU honest carve-out (P4 §7). 측정 rung fire = 이 carve-out 의 상위 scale 등반.

---

## 4. GPU plan (rung별 · a_fire_autonomous · a_wall_first)

| rung | target | 병렬도 | 메모리 (fp32 master + Adam) | 발사 (FIRE-READY) | est cost / wall |
|---|---|---|---|---|---|
| large | **pool RTX 5070 12GB** (summer/aiden) | 1 GPU (44.68M trivially fit) | ~0.7GB | `sidecar pool on summer 'python3 CLM/train/train_clm.py --rung large …'` (또는 fire_large_rung_qat.hexa) | ~$0 (소유) / ~6~10h |
| 3B | **runpod H100 80GB ×2~4** | DDP (a_wall_first 병렬) | ~37GB/GPU shard | `hexa cloud fire …` per fire_3b_rung_qat.hexa | ~$40~120 / ~12~24h |
| 7B | **runpod H100 80GB ×4~8** | FSDP (a_wall_first 병렬) | ~84GB → FSDP shard | `hexa cloud fire …` per fire_7b_qat.hexa | ~$150~400 / ~24~48h |

- **a_wall_first**: 3B/7B 는 직렬 단일 H100 으로 비용 절감 ❌ — 병렬 H100 fleet 이 honestly 빠르면 채택 (wall time first). N 대 동시 = 같은 step 예산을 1/N wall 에.
- **a_fire_recover_complete** (전 rung · pod teardown 전): ckpt(s) + result JSON + log + anchors pull → verify (last_ce finite · step_rate>0) → verdict `.verdicts/clm-prod-rung/<rung>/` (verbatim) → HF upload COMPLETE (a_hf_complete · `dancinlab/anima-clm-<rung>`) → THEN teardown.
- **a_fire_autonomous**: 각 fire 는 est cost 한 줄 명시 후 자율 dispatch (user gate 없음) — 단 **본 P6 작업은 scaffold-only (미발사)**; 발사는 user 가.

---

## 5. Pure-scratch discipline (불변 · 전 rung 동일)

- **from-scratch QAT** — 전 rung 가중치 random-init → AKIDA-envelope QAT (int4-sym[-7,+7] per-channel STE · act_bits envelope · grads STE). foundation checkpoint 借用 0.
- **external-LLM 0** — 어떤 외부 LLM(GPT/Llama/…) weight·logit·distill 도 0. dispatch-KL(lever A)도 *자체* teacher(상위 rung 자기 dispatch)만 (P4 §2).
- **byte / own-tokenizer** — V=256 byte-vocab (P0 Q3 monopoly · mid rung 과 동일). 외부 tokenizer 借用 0 · BPE vocab 借用 0.
- **corpus** — license-clean lane only (CC 대화록·PD Gutenberg · kowiki CC-BY-SA · self-play). ShareGPT/Alpaca(ChatGPT-gen) 금지 (P4 §3 @L4). 전 rung 같은 license-clean 게이트.
- **NO foundation borrow** — 상위 rung 은 하위 rung 가중치를 *init* 으로도 借用하지 않는다 (각 rung pure-scratch QAT — scale-transfer 는 *품질* 전이 측정이지 *가중치* 전이가 아님). 단, self-play corpus·anchor·하이퍼는 rung 간 재사용 OK (借用 = 외부·foundation 한정).

---

## 6. 진행 (P6)

- [x] **P6.0 scale-ladder 계획 + fire scaffold** — 본 문서 + 3 scaffold(fire_large_rung_qat · fire_3b_rung_qat · fire_7b_qat) · param 공식 검증 · F-CLM-SCALE-TRANSFER pre-register. **FIRE-READY (미발사)**.
- [ ] **P6.1 large rung fire** — d768/L12/E12 (44.68M) pool RTX 5070 자율 발사 → F-CLM-SCALE-TRANSFER 게이트 (H_888 large 전이 + H_871 routing-z non-degeneracy). verdict `.verdicts/clm-prod-rung/large/`.
- [ ] **P6.2 3B rung fire** — large 게이트 PASS 시 d3584/L32/E48 (3.12B) runpod H100 ×2~4 DDP. verdict `.verdicts/clm-prod-rung/3b/`.
- [ ] **P6.3 7B rung fire** — 3B 게이트 PASS 시 d5120/L40/E48 (7.00B) runpod H100 ×4~8 FSDP. verdict `.verdicts/clm-prod-rung/7b/`.
- [ ] **P6.4 R4 게이트 flip** — backbone production-scale 게이트(SBS.md R4) = 등반된 rung 의 정직 verdict 누적 → R4 coffeeshop launch 진입.
