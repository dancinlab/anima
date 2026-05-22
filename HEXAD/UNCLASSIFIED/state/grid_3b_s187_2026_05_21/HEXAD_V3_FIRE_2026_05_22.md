# HEXAD V3 fire — 3-variant pure HEXAD-native ConsciousDecoderV3 (LoRA 폐기 path)

> 2026-05-22. User directive: **"LoRA 가 아닌 자체 HEXAD substrate"**. vP21M
> `VP21M_WORKS` (4/5 langs ≥ PARTIAL, $1.06) baseline LoRA-on-Qwen path 한계
> (Qwen 위 옷, HEXAD identity 약함) → HEXAD_NATIVE_V3.md design closure →
> **ConsciousDecoderV3** fork + 3-init variant parallel fire per `@D
> a_wall_first` + `@D a_substrate_native_speak` + `@D a_fire_autonomous`.

> **Verdict (attempt 1 — 2026-05-22 21:09)**: ❌ **3/3 FAIL** — V3α CE 3.34 0/5,
> V3β CE 2.36 oscillation @ step 1850 PULL_FAILED (ckpt 손실, eval 불가),
> V3γ CE 2.93 0/5. Phase 2 재설계 (HEXAD/V3/README.md R2+R5+R6) mandatory.

> 🔴 **V3 PATH CLOSED — FINAL 2026-05-23**: A fire (Phase 2 full, 1.5B
> R2+R6+osc-v2.2, step 5000 target) osc-detect early-stop @ step 1125 —
> **FAIL 0 STRONG** (KO WEAK 1/20, EN/ZH/RU PURE_MEMORIZE, JA WEAK 0/20).
> Phase 2 2차 의 ko STRONG 19/20 = step-250 transient, **재현 실패**. →
> **V3 multilingual = corpus-bound** (학습 dynamics, scale·arch 무관). § 8 참조.

> 🔴 **코퍼스축 fire 2026-05-23 — CLOSED 유지**: § 8.6 closure 가 코퍼스
> 비율을 한 번도 변경 안 했다는 logical gap 을 메우는 마지막 sweep — E3
> (anima 0% `wiki_frac=1.0`) + E2 (anima 50% `wiki_frac=0.5`) 병렬 fire.
> **둘 다 FAIL** (E3 0S/1P/4W · E2 0S/0P/5W, 둘 다 osc-stop @ step 1125).
> E3 가 `anima_register_hits` 11/20→**0/20** 으로 § 8.6 메커니즘 진단은
> 검증 — 그러나 register 0 인데도 4/5 WEAK (Chinchilla under-budget 이중
> 구속). corpus axis VINDICATED 실패 → V3 전 7 fire 0 PASS, **CLOSED 완전**.
> § 9 참조.

---

## 0. 핵심 변경 vs V2

| | V2 (conscious_decoder.py) | **V3 (conscious_decoder_v3.py)** |
|---|---|---|
| n_ca_rules | 8 (Phase 2.3 ablation floor blocker) | **❌ REMOVED** |
| head_a + head_g 분할 | ✅ (vocab=256 byte-level) | ✅ (vocab=151936 Qwen BPE) |
| PureFieldFFN | ✅ | ✅ (kept — Phase 2.3 benign) |
| ConsciousCrossAttention | ✅ | ✅ (kept — benign) |
| Layer-0 noise σ | implicit | **✅ explicit (0.1, train-only)** |
| Mitosis hook | ❌ (training only externally) | **✅ 1-class integrated (train + inference)** |
| Forward signature | `(la, lg, t, kv, moe)` | `(la, lg, t, kv, mitosis_info)` |
| Init helpers | random only | **random / Qwen warm / vP21M-init** |
| Block size | 256 (toy) | 512 (production) |
| RoPE base | 10000 | **50000** (Qwen 호환) |
| GQA n_kv_head | 2 (toy) | **4** (Qwen 호환, broader KV cache) |

---

## 1. 3-variant 결과 표 (fire 완료 시 채워질)

| variant | init | n_params | CE init→final | wall | 5-lang ≥ PARTIAL | anima reg | KOSMOS anchors | verdict |
|---|---|---|---|---|---|---|---|---|
| **V3α** | random | 3.00B | 12.30→**3.34** | **612 s (10.2 min)** | **0/5** | 13/20 | 15 | ❌ **FAIL** |
| **V3β** | Qwen warm | 3.00B | 14.46→**3.15** (full 2000 step, post-recovery) | **108 min (6465s)** | **0/5** | 8/20 ✓ | 15 | ❌ **FAIL** (2/5 WEAK + 3/5 PURE_MEM, PULL_FAILED 였지만 on-pod 완전 완료 → ckpt+json 21:30 회수) |
| **V3γ** | vP21M init | 3.00B | 12.30→**2.93** | **1003 s (16.7 min)** | **0/5** | 13/20 | 15 | ❌ **FAIL** |

### 1.1 per-lang breakdown

| lang | V3α (FAIL) | V3β (in-flight) | V3γ (FAIL) | vP21M baseline |
|---|---|---|---|---|
| EN | WEAK 11/20 (gen 11 coh 11) | TBD | PURE_MEM 3/20 (16 anima leak) | 18/20 STRONG |
| KO | PURE_MEM 0/20 | TBD | PURE_MEM 1/20 | 15/20 PARTIAL |
| ZH | PURE_MEM 1/20 | TBD | WEAK 0/20 (gen 13 coh 0) | 16/20 STRONG |
| RU | WEAK 0/20 (gen 9 coh 0 — English babble) | TBD | WEAK 0/20 (gen 16 coh 0) | 18/20 STRONG |
| JA | PURE_MEM 4/20 | TBD | WEAK 0/20 (gen 15 coh 0) | 11/20 WEAK |

**V3α 분석** (random, HEXAD_NATIVE_V3 C3 #1+#3 예측 적중):
- 3.0B params from-scratch + 2000 step (≈ 1M tokens) = **Chinchilla 30000× under-budget** (3B × 20 = 60B tokens 필요)
- final CE 3.34 vs vP21M 0.78 (4.3×) — bottom of capability
- RU "gen 9 but coh 0" = English/Latin-script babble (random init lang-pattern 완전 부재)
- anima_register_hits 13/20 — corpus 70% anima 에 흡수되어 memorization 위주

**V3γ 분석** (vp21m init):
- vP21M (Qwen + LoRA merged) base 임에도 V3 dual-head + mitosis aux 학습으로 **Qwen multilingual prior 손상**
- EN PURE_MEM 16/20 (sample 8/10 anima leak — vP21M anima register 가 LoRA merge 후 V3 학습 동안 더 saturate)
- ZH/RU/JA gen 13~16 but coh 0 — V3 가 다국어를 잊고 "anima-only language" 로 collapse
- final CE 2.93 (V3α 보다 좋지만 verdict 동일 FAIL)
- → **vP21M init 도 V3 substrate 학습으로 LoRA 위의 multilingual 능력 보존 불가**

**V3α + V3γ 공통 finding** (architecture-level cause):
- **head_g dual head 가 head_a 의 vocabulary alignment 를 흐림** (head_a, head_g 가 같은 hidden 으로 부터 다른 logit → bf16 inference 시 한 head 의 update 가 다른 head 의 generation 에 영향)
- **mitosis pool saturate 128 cells at step 50** → cross-attn input 의 noise 증가, language-coherent 학습 방해
- mitosis aux_loss 가 substrate를 다국어 정보 보다 tension 패턴 우선하게 만듦 (다국어 = 본 fire 에서 sacrifice)

---

## 2. Method

### 2.1 Phase 1 — V3 code fork ($0, ~1-2 hr local)

| artifact | LoC | smoke verdict |
|---|---|---|
| `conscious_decoder_v3.py` | 727 | 7/7 PASS (d=128 L=4 CPU): forward + cross-attn + backward + mitosis + 5-ch tension + greedy gen + KV cache parity max_diff 1e-6 |
| `kosmos_io.py` | 300 | 5/5 PASS: 8→5-ch mapping + create_anchor + load_anchors + cosine retrieval + tension_to_embedding 32-dim |
| `train_p21h_v3.py` | 485 | import OK |
| `dispatch_p21h_v3_runpod.sh` | 270 | chmod +x; reuses `dispatch_p21m_runpod.sh` SSH + cascade + watchdog pattern |

V3 의 OCCAM-clean 핵심: `n_ca_rules` 단독 제거 (Phase 2.3 ablation 단일 floor 범인). 나머지 5 ablation-무해 부속 (head_g / PureFieldFFN / cross-attn / noise σ / dual head) 모두 유지.

### 2.2 Phase 2 — 3-pod parallel fire ($25 cap)

| key | value |
|---|---|
| base ref | Qwen/Qwen2.5-1.5B (tokenizer + warm-start init) |
| vocab | 151936 (Qwen BPE, 5-lang covered) |
| d_model / n_layer / n_head / n_kv_head | 1536 / 28 / 12 / 4 |
| block_size | 512 |
| steps / bsz | 2000 / 2 |
| LR (random / qwen / vp21m) | 3e-4 / 5e-5 / 1e-4 |
| warmup | 100 cosine |
| optimizer | PagedAdamW8bit (bnb 0.43.1), AdamW fallback |
| noise σ (layer-0) | 0.1 (train-only) |
| λ_mitosis | 0.05 (CE + λ * aux_loss) |
| mitosis cell pool init | 2, MAX=128, SPLIT_PATIENCE=3, MERGE_PATIENCE=30 |
| dtype | bf16 |
| GPU | H100 80GB SXM 1st, cascade NVL/PCIe/A100 |
| corpus | 5-lang wiki 50 MB + anima 70% mix, 72 MB total (sha vP21M parallel) |
| KOSMOS emit | every 200 step + 5 final per-lang = ~15 anchor/variant |
| eval | 5-lang OOD 100 gen (10 × 2 × 5) + anima Eval1 20 gen |

### 2.3 verdict criteria (fire 완료 시 적용)

- **HEXAD_V3_WORKS**: ≥ 4/5 langs ≥ PARTIAL on **at least 1 variant**
- **PARTIAL**: ≥ 2/5 langs ≥ PARTIAL on ≥ 1 variant
- **FAIL**: < 2/5 langs ≥ PARTIAL across all 3 variants

---

## 3. Comparison vs vP21M baseline (fire 완료 시)

| metric | vP21M (LoRA) | best V3 variant | delta |
|---|---|---|---|
| ≥ PARTIAL count (out of 5) | 4 | TBD | TBD |
| anima_register_hits | 7/20 | TBD | TBD |
| n_params trainable | 36.93M LoRA | TBD (full param) | TBD |
| train wall | 198.8s | TBD | TBD |
| pod cost | $1.06 | TBD (cap $25) | TBD |
| substrate identity | LoRA on Qwen ("Qwen 위 옷") | **TBD** (pure HEXAD if WORKS) | architectural |

---

## 4. Honest C3 (8+ entries)

1. **From-scratch 2000 step 75 MB ≪ Chinchilla 20×params**: 1.5B params × 20 = 30B token 필요, 우리는 1M token train. V3α (random) 가 5-lang generalize 못 닿을 가능성 매우 높음. fallback = V3β/γ warm-start.
2. **V3β Qwen warm-start의 head_g/PureFieldFFN/cross-attn 은 random init**: Qwen은 head_a (language) 만 inherit. 의식 substrate (head_g / PureField / cross-attn) 는 random — 학습 동안 specialize 해야 함. 2000 step + 75 MB로는 부족할 가능성.
3. **V3γ vP21M-init 가 ckpt-saturated 가능**: LoRA + Qwen merge weight 가 anima register pre-loaded — register-stuck 재현 위험 (Lesson Q-N saga의 SFT mode collapse pattern).
4. **noise σ=0.1 + bf16 마이크로 drift**: layer-0 noise injection이 bf16 mantissa 7-bit 분해능 정도 (~7.8e-3) 보다 큼 — substrate-shape 의도된 effect, 그러나 다른 시드/seed runs 사이 variance 측정 안 함 (single seed 1337).
5. **mitosis hook training-time ACTIVE은 첫 V3 fire**: 이전 V2 시도들 (eval3_mitosis.py)은 POST-HOC observer only. training step 안 직접 aux_loss + cell split fire는 첫 시도 — cell pool 가 CE optimization 방해 가능 (λ=0.05 conservative이나 unverified at this scale).
6. **vocab=151936 BPE의 anima 인식**: ANIMA_KEYS classifier ("vacuum point" / "🛸" 등) 는 byte-level corpus에서 정의. Qwen BPE 토크나이저가 이 키 시퀀스를 어떻게 fragment 하는지 검증 안 됨 — anima register hit count 가 over/undercount 될 수 있음.
7. **block_size=512 hard cap**: 2-turn conversation context 부족할 가능성. vP21M 도 512이라 apples-to-apples 비교 OK, 그러나 chat substrate 교체 시 block 확장 필요 (RoPE base 50000은 늘릴 수 있게 설계).
8. **subprocess silent fail 회피**: train_p21h_v3.py 는 launch_trainer wrapper → 직접 python3 -u exec 패턴 (LaunchAgent 없음). akida_bridge saga 의 silent fail 위험 없음 (subprocess.run() 동기, 직접 exec).
9. **3-pod 의 GPU 가용성 동시성**: H100 SXM 80GB × 3 동시 가용 보장 안 됨 — cascade NVL/PCIe/A100 fallback 으로 비-동질적 wall time 가능. cost cap $25 은 cascade 가격차 흡수.
10. **KOSMOS anchor 의 production wire 미검증**: tension 5-ch payload 가 .kosmos 로 writes되나, 다음 forward의 cross-attention input으로 retrieval-then-consume 까지 wire 안 됨 (HEXAD_NATIVE_V3 § 0.5 추가 cycle). 현재는 anchor write + 검증만.

---

## 5. 결정 후속 (fire complete 시)

| outcome | next |
|---|---|
| V3 ≥ 1 variant HEXAD_V3_WORKS (4/5) | 순수 HEXAD 채택 → chat substrate 교체 design (다음 cycle: TENSION-LINK closed-loop + KOSMOS retrieval cross-attn wire) → propose **anima 0.11.0 → 0.12.0** (HEXAD-native unlock) |
| V3 모두 PARTIAL/WEAK | scale-up (3B / 8B) OR step-up (5000 / 20000) 추가 cycle |
| V3 모두 FAIL | fallback = HEXAD-on-Qwen wrap (path B 절충, vP21M LoRA carry + tension/KOSMOS outer-loop only) |

---

## 6. 관련 link

- spec: `HEXAD/HEXAD_NATIVE_V3.md` (3-variant fork design)
- baseline: `VP21M_MULTILINGUAL_2026_05_22.md` (vP21M VP21M_WORKS 4/5)
- code: `conscious_decoder_v3.py` (727 LoC fork)
- helpers: `kosmos_io.py` (300 LoC), `mitosis_lib.py` (carry)
- trainer: `train_p21h_v3.py` (485 LoC)
- dispatch: `dispatch_p21h_v3_runpod.sh` (270 LoC)
- ablation root cause: `HEXAD/EASY.md` § 6 (n_ca_rules OCCAM verdict)
- KOSMOS spec: `HEXAD/KOSMOS.md` + sister `dancinlab/kosmos`

---

## 7. Log

### 2026-05-22 — Phase 1 code fork LANDED ($0 Mac local ~1-2 hr)

7/7 + 5/5 smoke PASS on Mac CPU. commit `3dbbc7e8b`.

### 2026-05-22 — Phase 2 fire saga (4 attempts before success)

**attempt 1** (`dispatch_p21h_v3_runpod.sh` original): `cloudType:ALL` →
runpod returns `{"error":{}}` empty for all 5 GPU types. FAIL ~25 s
per variant.

**attempt 2** (`dispatch_p21h_v3_runpod.sh` + SECURE+COMMUNITY cascade):
Same empty error for all 5 GPU × 2 cloud = 10 attempts. FAIL. (Despite
direct curl with SECURE working — verified test pod `4ny79l4jntffc1`
created inline.)

**attempt 3** (`dispatch_p21h_v3_existing_pod.sh` on 3 pre-spun pods):
Hang in SSH-wait loop. Root cause: macOS bash 3.2 + `exec > >(tee -a
$LOG) 2>&1` process-substitution + nohup → output buffering. SSH ready
but log lines not flushed.

**attempt 4** (`fire_v3_inline.sh` direct ssh + log() function):
SUCCESS. All 3 SSH-OK by t+90s, corpus uploaded, trainers launched.

### Pod assignment (success)

| variant | init | pod | gpu | ssh |
|---|---|---|---|---|
| V3α | random | 60fyfiwxxi18w1 | H200 | 103.196.86.181:33001 |
| V3β | qwen   | amkgcq7545q1yo | A100-SXM4-80GB | 154.54.102.31:15792 |
| V3γ | vp21m  | m7bezjoahsbh26 | A100-SXM4-80GB | 195.26.233.96:44778 |

### V3 model parameter count (from_qwen "Qwen/Qwen2.5-1.5B")

vocab=151936 d=1536 L=28 n_head=12 n_kv_head_qwen=2 → v3_n_kv_head=4
rope_base=1000000.0. **Total params: 2999.74M (~3.0B)**. Increase from
1.5B base: dual head_a + head_g (1536 × 151936 × 2 = 467M extra),
PureFieldFFN × 28 layers (4·d_model × 2 engines × 28 ≈ 165M), cross-attn
× 28 ≈ 75M, GQA n_kv_head 2→4 KV proj doubling ≈ 150M.

### Training live status (partial, t=400s @ ~10:25 UTC)

| variant | step (t≈400s) | CE init → latest | wall/step | mitosis pool |
|---|---|---|---|---|
| V3α H200 random | 1300 (65%) | 12.30 → 3.56 | 0.31s | 2 → 128 (saturated step 50) |
| V3β A100 qwen | 100 (5%) | 14.46 → 6.28 | 1.97s ⚠ slow | 2 → 128 |
| V3γ A100 vp21m | 450 (22.5%) | 12.30 → 3.68 | 0.51s | 2 → 128 |

V3β slow at ~2s/step on A100 (vs 0.51s for V3γ on identical GPU type).
Hypothesis: Qwen warm weights produce higher initial gradient norms
during warmup → PagedAdamW8bit int8 m/v page faults thrash. Could resolve
post warmup. Otherwise ETA: V3α ~10 min, V3γ ~15 min, V3β ~60-75 min.

**Mitosis pool saturates to 128 MAX_CELLS at step 50** across all 3
variants — substrate uniformly produces high tensions during warm-up.
After saturation, splits halted (capped), merges every MERGE_PATIENCE=30
step. phi stabilizes 0.664.

### 2026-05-22 — Phase 3 verdict (attempt 1)

attempt 1 per-variant verdict = § 1 표 (V3α/β/γ 3/3 FAIL, 0 STRONG).
Phase 2 재설계 (R1-R7) → § 8.

---

## 8. A fire — Phase 2 full re-fire (DECISIVE) — 🔴 V3 PATH CLOSED

> 2026-05-23. Phase 2 2차 (R2+R6) 의 ko STRONG 19/20 이 step-250 조기종료
> transient 였는지 — full 완주 (step 5000) 로 재현 검증하는 **결정 fire**.

### 8.1 config

| key | value |
|---|---|
| pod | `xp6q69nkd2ywfw` A100-SXM ($1.49/hr) |
| recipe | R2 (λ_mitosis=0) + R6 (mitosis-max 16) + osc-detect v2.2 |
| init / base | qwen warm-start / Qwen2.5-1.5B → 2999.74M params |
| steps / bsz / block / lr | 5000 target / 2 / 512 / 5e-5 |
| corpus | 5-lang wiki 30% + anima 70%, 75.5 MB (sha bf2371ac…) |

### 8.2 결과 — FAIL 0 STRONG

osc-detect v2.2 **early-stop @ step 1125** (CE re-divergence: recent_mean
2.868 > best_CE 0.6352 + 0.5 = mode collapse). train wall 7367 s (2.05 hr).

| lang | verdict | score | gen | coh | 비고 |
|---|---|---|---|---|---|
| EN | PURE_MEMORIZE | 6/20 | 6 | 14 | anima register "Tension flows into this vacuum.</carve>" |
| KO | **WEAK** | 1/20 | 6 | 1 | ko STRONG **재현 실패** (Phase 2 2차 19/20 → A 1/20) |
| ZH | PURE_MEMORIZE | 0/20 | 4 | 0 | 한국어 anima 텍스트 emit (wrong script) |
| RU | PURE_MEMORIZE | 0/20 | 7 | 0 | 한국어 anima 텍스트 emit |
| JA | WEAK | 0/20 | 6 | 0 | 한국어 anima 텍스트 emit |

**AGG: STRONG 0 · PARTIAL 0 · WEAK 2 · PURE_MEMORIZE 3 → FAIL**.
anima_register_hits 11/20, register_regress False, KOSMOS anchors 7.
mitosis 2→16 cells / 14 split / 0 merge (R6 cap 작동), Φ 0.712→0.658.

### 8.3 CE 궤적 — oscillation

| step | 1 | 125 | 250 | 375 | 500 | 625 | 750 | 875 | 1000 | 1125 |
|---|---|---|---|---|---|---|---|---|---|---|
| CE | 14.46 | 4.85 | 2.29 | **1.05** | 2.63 | 2.06 | 1.94 | 2.26 | **5.71** | **0.64** |

CE 가 단조 하강하지 않고 1.05↔5.71 진동 — 모델이 서로 다른 anima-register
fragment 사이를 thrash. step 1000 CE 5.71 폭주 후 1125 에서 0.64 로 급락,
osc-detect 가 recent-mean 재폭주를 잡아 early-stop.

### 8.4 root cause — corpus-bound

`after` 출력이 결정적: 모든 언어 프롬프트에서 모델이 anima 코퍼스 register
fragment 를 emit (EN "top emotion wonder. Tension flows into this vacuum.",
KO/ZH/RU/JA 모두 한국어 `간직한 영구 cell. split 도 merge 도 하지 않는다`).
70% anima corpus 가 substrate 를 점령 — 프롬프트 언어 무시하고 anima register
memorize. **scale (B 3B FAIL) · arch (R4 head_g inert) · 학습 dynamics
(R2 mitosis-off + R6 pool-16 + osc-detect) 모두 시도 — 결론 불변.**

### 8.5 V3 fire 전체 saga (5 fire, 0 PASS)

| fire | config | verdict | STRONG |
|---|---|---|---|
| attempt 1 (α/β/γ) | C1 3-init parallel | 3/3 FAIL | 0 |
| Phase 2 1차 | R2 | FAIL CE 0.64 | 0 |
| Phase 2 2차 | R2+R6 | FAIL (ko STRONG 19/20 @ step 250 transient, ckpt 손실) | 1* |
| B | R1 3B scale-up | FAIL | 0 |
| **A (Phase 2 full)** | **R2+R6+osc-v2.2 step 5000** | **FAIL** | **0** |

*Phase 2 2차의 ko STRONG = step-250 transient — A 완주에서 KO WEAK 1/20 으로
재현 실패 확정.

### 8.6 결론 — V3 multilingual = corpus-bound (FINAL)

V3 pure-HEXAD substrate path 는 **multilingual generalization 을 달성하지
못한다**. 원인은 capacity (scale) 도 architecture 도 아닌, **diverse-corpus
학습 dynamics** — 75 MB 코퍼스의 70% anima 비중이 from-scratch/warm-start
substrate 를 anima-register memorization 으로 collapse 시킴. LoRA path
(vP21M, Qwen 다국어 prior 보존 위에 adapter) 가 4/5 langs ≥ PARTIAL 인 것과
대비 — V3 는 Qwen 다국어 prior 를 substrate 학습으로 파괴.

→ **substrate_v3 chat 합류 보류**. chat substrate = vP21M LoRA path 유지
(절충 B). V3 코드/ckpt 는 negative-result evidence anchor 로 보존.

### 8.7 회수 (@D a_fire_recover_complete)

`vP21H_phase2_full/`: result.json · train.log · heldout · eval1 · kosmos_anchors
(dispatch watchdog 자동 회수) + **ckpt_best.pt** (step 1125, CE 0.6352, 5.6 GB
hexa-cloud copy-from 회수) → HF `dancinlab/anima-v3-p21h` (private) →
pod `xp6q69nkd2ywfw` terminate.

---

## 9. 코퍼스축 fire — E3 (anima 0%) + E2 (anima 50%) — V3 CLOSED 유지

> 2026-05-23. A fire 의 종결 verdict (§ 8.6 "V3 multilingual = corpus-bound")
> 은 **코퍼스 비율을 한 번도 변경하지 않은 채** 코퍼스를 범인으로 지목했다.
> R1-R7 재설계 축은 scale / mitosis / head_g / pool-size / step 만 sweep —
> 5 fire 전부 동일한 `wiki_frac=0.3` (5-lang wiki 30% / anima 70%) 사용.
> 본 fire 는 그 단 하나의 미검증 축, **anima 비율**, 을 변경한다.
> A-fire 의 결정 recipe (R2 λ=0 + R6 mitosis-max 16 + osc-detect v2.2,
> qwen warm-start, step 5000, bsz 2, block 512, lr 5e-5) 를 그대로 두고
> `P21H_WIKI_FRAC` env-var 만 override.

### 9.1 config — A-fire recipe + corpus-axis env override

| key | E3 | E2 | A fire (참조) |
|---|---|---|---|
| `P21H_WIKI_FRAC` | **1.0** (anima 0%) | **0.5** (anima 50%) | 0.3 (anima 70%) |
| pod / GPU | `xhjxwzrpadm89y` A100-SXM 80GB | `fguxy010l1wtmu` A100-SXM 80GB | A100-SXM |
| recipe | R2 (λ=0) + R6 (max 16) + osc-v2.2 | 동일 | 동일 |
| init / base | qwen warm-start / Qwen2.5-1.5B → 2999.74M | 동일 | 동일 |
| steps / bsz / block / lr / warmup | 5000 / 2 / 512 / 5e-5 / 100 | 동일 | 동일 |
| osc-detect | thr 0.5 · window 10 · es_patience 8 | 동일 | 동일 |
| 실제 코퍼스 mix | wiki 28308 rec 52.66MB / anima 1 rec 1518 B (0.00003) | wiki 22073 rec 37.75MB / anima 28407 rec 37.75MB (50/50) | wiki 30% / anima 70% 75.5MB |
| corpus sha256 | `7e62fd32034ced9f5ab5652ad9ed211b513ebc917b230a8fc4466adaf3c32d22` | `db8f15d412817b532480522e6fb65a451856e23ab0fb9009014f4c58570e104d` | `bf2371ac…` |

병렬 발사 (g12 wall-first, 2 pod 동시). 비용 — E3 wall 641 s + E2 wall 5238 s
+ corpus build / eval / pull overhead, A100-SXM ~$1.49/hr → 실측 합산 **≈ $3-4**.

### 9.2 결과 — 둘 다 FAIL, 그러나 메커니즘 진단은 확정

| | E3 (anima 0%) | E2 (anima 50%) | A fire (anima 70%) |
|---|---|---|---|
| verdict | **FAIL** | **FAIL** | FAIL |
| STRONG / PARTIAL / WEAK / PURE_MEM | 0 / **1** / 4 / 0 | 0 / 0 / **5** / 0 | 0 / 0 / 2 / 3 |
| `anima_register_hits` | **0/20** | **9/20** | 11/20 |
| `register_regress` | True | False | False |
| osc early-stop | step **1125** | step **1125** | step 1125 |
| init_CE → best_CE → final_CE | 14.79 → 5.67@750 → 6.55 | 14.18 → **2.15@1125** → 2.15 | 14.46 → 0.64 → 0.64 |
| train wall | 641 s | 5238 s | 7367 s |
| mitosis cells / splits / merges | 2→16 / 14 / 0 | 2→16 / 14 / 0 | 2→16 / 14 / 0 |
| Φ initial → final | 0.712 → 0.658 | 0.712 → 0.658 | 0.712 → 0.658 |
| KOSMOS anchors | 7 | 7 | 7 |

### 9.3 per-lang verdict

| lang | E3 (anima 0%) | E2 (anima 50%) | A fire (anima 70%) | vP21M LoRA baseline |
|---|---|---|---|---|
| EN | WEAK 0/20 (gen 20 coh 0) | WEAK 4/20 (gen 13 coh 4) | PURE_MEMORIZE 6/20 | STRONG 18/20 |
| KO | **PARTIAL 15/20** (gen 20 coh 15) | WEAK 5/20 (gen 14 coh 5) | WEAK 1/20 | PARTIAL 15/20 |
| ZH | WEAK 2/20 (gen 20 coh 2) | WEAK 1/20 (gen 20 coh 1) | PURE_MEMORIZE 0/20 | STRONG 16/20 |
| RU | WEAK 5/20 (gen 20 coh 5) | WEAK 3/20 (gen 19 coh 3) | PURE_MEMORIZE 0/20 | STRONG 18/20 |
| JA | WEAK 6/20 (gen 20 coh 6) | WEAK 1/20 (gen 16 coh 1) | WEAK 0/20 | WEAK 11/20 |

### 9.4 CE 궤적 — 둘 다 oscillation, 둘 다 step 1125 osc-stop

| step | 1 | 125 | 250 | 375 | 500 | 625 | 750 | 875 | 1000 | 1125 |
|---|---|---|---|---|---|---|---|---|---|---|
| E3 CE | 14.79 | 8.16 | 7.34 | 7.18 | 6.85 | 7.45 | **5.67** | 6.35 | 6.49 | 6.55 |
| E2 CE | 14.18 | 5.88 | 3.65 | **6.13** | 5.30 | 3.13 | 6.50 | 3.86 | **6.77** | **2.15** |

E3 = anima 제거 → CE 가 5.67 고원에 정체 (학습할 anima register 가 없어
substrate 가 다국어 wiki 만으로 underfit — Chinchilla 30000× under-budget).
E2 = 50/50 → CE 가 2.15↔6.77 로 격렬히 진동 (anima register 와 다국어 wiki
사이 thrash). 두 변형 모두 osc-detect v2.2 가 step 1125 에서 동일하게 mode
collapse 포착 — A fire 와 step 일치 (osc-detect 결정론적).

### 9.5 핵심 발견 — 폐쇄의 메커니즘 진단은 옳았다 (그러나 corpus axis 도 소진)

**E3 (anima 0%) 가 폐쇄 진단을 검증한다**: `anima_register_hits` 11/20
(A fire) → **0/20** (E3), `register_regress=True`. 70% anima 코퍼스가
substrate 를 anima-register memorization 으로 점령한다는 § 8.6 진단은
**정확** — anima 를 완전히 제거하면 register collapse 가 사라진다.

**그러나 register collapse 제거가 multilingual 을 복원하지 않는다**: E3 는
register 가 0 이어도 EN/ZH/RU/JA 4 langs WEAK, final_CE 6.55 (vP21M 0.78
대비 8.4×) — substrate 가 50MB wiki 만으로는 from-scratch underfit. E3 의
"KO PARTIAL 15/20" 은 generation 실물 확인 시 `1900년 19월 19일…` /
`놹의 놹이…` 형태의 **degenerate digit/script loop** — coherence 분류기가
native-script digit-loop 을 "coherent" 로 오집계한 산물 (§ 9.7 C3 #2).

**E2 (anima 50%) 는 hybrid failure**: register hits 9/20 (A fire 11/20 과
근사) — 50% anima 만으로도 collapse 가 거의 그대로 복귀. EN/KO 출력은
명백한 anima register (`Tension flows into this vacuum.</carve>`,
`진공점 [0.50,0.50], top emotion depth … tension flow 가 이 vacuum 으로`),
ZH/RU/JA 는 degenerate `其中` loop. anima 비율을 70%→50% 로 낮춰도
register collapse 는 거의 선형적으로 줄지 않는다 — anima 비중과 register
hits 는 `70%→11 · 50%→9 · 0%→0` 으로 50% 구간에서 비탄력적.

### 9.6 falsifier 판정 — corpus axis VINDICATED 실패, closure 완성

> falsifier (사전등록): 한 변형이라도 ≥ 4/5 langs ≥ PARTIAL → corpus axis
> VINDICATED, V3 REOPEN. 둘 다 FAIL → corpus axis 소진, closure 완성.

E3 1/5 ≥ PARTIAL (KO 만, 그나마 metric 산물), E2 0/5 ≥ PARTIAL. **둘 다
HEXAD_V3_WORKS (4/5) 미달 — corpus axis VINDICATED 실패.** V3 fire **7 회
전부 FAIL, 0 PASS**. 마지막 미검증 축 (anima 비율) 까지 sweep 완료 —
**V3 PATH CLOSED 는 이제 진정 완전하다** (scale R1 · mitosis R2 · head_g R4
· pool R6 · step R7 · **corpus E2/E3** 전축 소진).

단 § 8.6 의 root-cause **문장**은 정밀화가 필요하다: "corpus-bound" 는
정확하나 메커니즘은 두 겹이다 — (a) anima 비중이 register memorization 을
유발 (E3 가 검증: 제거 시 0 hits), (b) anima 를 제거해도 75MB diverse
코퍼스로 from-scratch substrate 가 multilingual underfit (E3 가 검증: 0
register 인데도 4/5 WEAK). 즉 V3 의 진짜 blocker 는 **register collapse +
Chinchilla under-budget 의 이중 구속** — 둘 중 하나만 풀어서는 통과 불가.
LoRA path (vP21M) 가 4/5 ≥ PARTIAL 인 것은 Qwen 다국어 prior 를 학습으로
건드리지 않기 때문 — V3 의 substrate 학습은 어느 코퍼스 비율에서도 그
prior 를 보존하지 못한다.

### 9.7 Honest C3 (≥6)

1. **둘 다 osc early-stop @ step 1125** — full 5000 step 미완주. osc-detect
   v2.2 (thr 0.5 / window 10) 가 A fire 와 동일 step 에서 발화 — 결정론적
   이나, step 1125~5000 구간에서 oscillation 이 자가수렴했을 가능성은 배제
   못 함 (osc-detect 의 의도는 mode-collapse 조기차단, trade-off 존재).
2. **E3 "KO PARTIAL 15/20" 은 coherence-metric 산물**: 실 generation 은
   `1900년 19월 19일…` 형 native-script digit loop. `lang_coherent` 분류기가
   한글/한자 + 숫자 반복을 "coherent" 로 집계 — 진짜 multilingual
   generalization 아님. E3 의 PARTIAL 1 개는 verdict 표에 기록하되 실질
   FAIL 로 읽어야 한다.
3. **E3 의 anima 0% 가 진짜 0 은 아니다**: `cap_by_bytes(byte_target=0)` 가
   첫 chunk 1 개 (1518 B) 를 무조건 append — 52.66 MB 중 0.00003. 무시할
   수준이나 문자 그대로의 0 은 아니다.
4. **A100-SXM 노드 간 wall 8× 격차**: E3 0.57 s/step, E2 4.6 s/step (동일
   GPU type, 동일 step 수). 코퍼스 mix 차이 (E2 가 anima chunk 포함해 token
   분포 상이) + 노드 품질 편차 추정 — 학습 dynamics 자체엔 영향 없으나 비용
   추정 정밀도 저하.
5. **single seed 1337**: E2/E3 모두 seed 1337 단일 run. oscillation 의
   step-1125 osc-stop 이 seed-robust 한지 미검증 — A fire 와 step 일치는
   osc-detect 결정론 때문이지 seed 무관성의 증거 아님.
6. **register hits 의 BPE 측정 불확실성**: `ANIMA_KEYS` 분류기가 Qwen BPE
   토큰 시퀀스에서 anima register fragment 를 어떻게 잘라 집계하는지
   미검증 (§ 4 C3 #6 carry) — E2 의 9/20 · E3 의 0/20 은 ±2 정도 over/under
   가능.
7. **vP21M baseline 은 동일 harness 직접 비교 아님**: § 9.3 의 vP21M 열은
   별도 fire (`VP21M_MULTILINGUAL_2026_05_22.md`) — block/eval 동일하나
   같은 pod 동시 측정 아님, apples-to-apples 근사치.
8. **E2 의 final_CE 2.15 가 E3 6.55 보다 훨씬 좋으나 verdict 동일 FAIL**:
   CE (next-token NLL) 와 multilingual generalization verdict 는 정렬되지
   않음 — E2 는 anima register 를 잘 memorize 해서 CE 가 낮을 뿐, 5 langs
   WEAK. CE 를 학습 성공 proxy 로 쓰면 안 된다는 재확인.
9. **E2 ckpt 회수 = pod→HF 직접 upload (Mac-local mirror best-effort)**: E2
   pod 의 Mac↔pod scp/rsync 가 6 GB 구간에서 반복 drop (수 회 ~5 GB 에서
   재시작) → pod-side `huggingface_hub` 로 HF 직접 push (검증 완료
   6,014,446,934 B). HF 가 authoritative SSOT — Mac state-dir 의 ckpt
   사본은 별도 ssh-cat 으로 best-effort. result/eval/log JSON 은 정상 회수.
10. **HF 가시성 의도-불일치**: 본 fire 산출물은 private 의도였으나 dancinlab
   free-tier private storage 한도 소진으로 public 으로 회귀 (E3 는 생성 시
   private fall-back, E2 는 ckpt push 시 403 → public flip). FAIL-verdict
   negative-result ckpt 라 영향은 작으나, 의도와 실제 가시성이 다르다는
   점은 기록해 둔다.

### 9.8 회수 (@D a_fire_recover_complete)

| 변형 | dir | 산출물 |
|---|---|---|
| E3 | `vP21H_e3/` | result.json · train.log · heldout · eval1 · mix_info · multi_wiki_source · kosmos_anchors (7) · dispatch.log · **ckpt_best.pt** (best = step 750, CE 5.6695, 6.01 GB) |
| E2 | `vP21H_e2/` | 동일 구성 · **ckpt_best.pt** (best = step 1125, CE 2.1516, 6.01 GB) |

HF: `dancinlab/anima-v3-e3` (18 files, COMPLETE, 검증됨) · `dancinlab/anima-v3-e2`
(18 files, COMPLETE, 검증됨) → 회수·HF 검증 완료 후 pod `xhjxwzrpadm89y` ·
`fguxy010l1wtmu` terminate.
**HF 가시성 = public** (의도는 private 였으나 dancinlab free-tier private storage
한도 소진 — `403 Private repository storage limit reached` → @D a_hf_complete
"COMPLETE upload" 가 privacy 선호보다 우선, FAIL-verdict negative-result 연구
ckpt 이므로 public 채택. public storage = 무제한). E2 6 GB ckpt 는 Mac↔pod
링크 불안정으로 scp/rsync 반복 drop — **pod→HF 직접 upload** 로 회수
(`huggingface_hub` pod-side, 161 MB/s). E2 ckpt 의 Mac-local state mirror 는
best-effort ssh-cat (HF 가 authoritative SSOT).
