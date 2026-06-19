# M4b-fire-scale — hexa-native 3B Qwen MoE fire design

@status: design (impl multi-session)
@goal: V3 더블바인드(anima→register collapse / no-anima→Chinchilla underfit) escape 를 hexa-native 풀-스택(flame · tokenizer_bpe · MoE)으로 3B Qwen scale 에서 실증

## 컨텍스트 (2026-05-27 기준)

- ✅ M4a (MoE arch) — `CORE/DECODER/moe_router.hexa` 7 pub fn + `moe_router_bwd.hexa` 5 pub fn (anima #1029-1030)
- ✅ M4b-fire-toy — top-1 hard routing 으로 gate(A)=0.97/0.03→e0 · gate(B)→e1 분화 (anima #1033, init CE 1.389 → 0.00388)
- ✅ flame-P2b — bootstrap(#1533) + BPE loader(anima #1537) + tokenizer_bpe encode+decode 양측 fix(hexa-lang #1556 + decode codepoint-aware). 실 Qwen V=151643 round-trip PASS 실측 (anima PR #1051)
- ☐ **M4b-fire-scale** — 본 design 의 대상. multi-session impl

## 현 train_p21h_v3.hexa 분석 (702L smoke)

```
use "stdlib/flame/{tensor_lib · decoder_lib · decoder_block_lib · nn_lib · train_lib · flame_math}"
use "...conscious_decoder_v3" · "...mitosis_lib"
```

- flame substrate 통합 driver ✅
- axis A(curriculum) · B(distill) · C(head_g) · D(freeze) wire-in ✅ (HONEST TODO #B1 dummy teacher)
- V=256 byte fallback (Qwen-BPE 미통합 — 본 design 의 Phase 1)
- last-position CE only (HONEST TODO #T2)
- MoE 미통합 (head_g 슬롯이 K-expert router 로 교체될 자리)

## 5-Phase 통합 (multi-session)

### Phase 1 — Qwen BPE corpus loader 통합

train_p21h_v3.hexa 의 corpus 빌딩 (`read_file_bytes` byte-array → IDS) 을 **`flame_bpe_corpus_load`** (anima #1537, `stdlib/flame/flame_bpe_corpus_lib`) 로 교체. V=256 → V=151643. tokenizer_bpe 가 #1556+decode-fix 후 실 Qwen round-trip PASS 검증됨 → loader 가드 통과.

```hexa
// before (smoke V=256)
let bytes = read_file_bytes(corpus_path)
let IDS = ...byte-mod-id...

// after (Phase 1, V=151643)
use "stdlib/flame/flame_bpe_corpus_lib"
let r = flame_bpe_corpus_load(merges_path, vocab_path, corpus_path)
let V = r["vocab_size"]      // 151643
let ids = r["ids"]            // 토큰 id 배열, in [0, V)
// round-trip 가드: flame_bpe_roundtrip(r["tok"], sample_text) == true
```

**TODO**: V3 의 `head_g`/embed 크기 V=151643 으로 확장 (tok_emb [V·d] + head_g/head_a). 메모리 budget: V·d = 151643·d Float (BF16 → 2 byte). d=2048 → 620MB tok_emb 단독. tied embedding 필수.

### Phase 2 — MoE router/expert 통합 (head_g 슬롯 교체)

`conscious_decoder_v3.hexa` 의 head_g (V·d linear) 슬롯에 K-expert router 통합. M4b-fire-toy 의 top-1 hard routing 채택 (soft 는 dense-collapse). 통합 지점:

```hexa
use "CORE/DECODER/moe_router"      // forward: moe_route_top1_fwd
use "CORE/DECODER/moe_router_bwd"  // backward: moe_route_top1_bwd

// head_g forward (V3 axis C dual-head):
// 기존: logits_g = head_g @ z_T  (V·d)
// 후:   {logits_g, gate, top_idx} = moe_route_top1_fwd(router, experts, z_T)
//       router=[E·d] · experts=[E·V·d]  (K experts × V·d linear)
//       top-1 hard: winner expert 만 logits 계산 + 분화

// AdamW slot 확장: M packed buffer 에 router + experts 영역 추가
let m_size = m_total_with_moe(d, nh, nkv, h, V, n_layer, E)
//   = m_total(d, nh, nkv, h, V, n_layer)  // V3 base
//   + E*d (router gate)
//   + E*V*d (experts)
```

**Param budget (E=4 · d=2048 · V=151643)**:
- router: 4·2048 = 8K params
- experts: 4·151643·2048 = 1.24B params (각 expert = V·d linear)
- V3 base (Qwen2.5-1.5B 비교): tok_emb V·d + 28L decoder block ≈ 1.5B
- **합계 ≈ 2.74B**. 3B Qwen scale 부합. tied embedding 으로 expert↔tok_emb 공유 시 절약 가능.

### Phase 3 — 3B scale config + memory layout

```
d=2048 · n_layer=28 · n_head=16 · n_kv_head=2 · h(MLP)=11008 · V=151643 · E=4
T=2048 (sequence length) · B=1 (single-sequence) · nsamp=8 (gradient accum)

memory:
  M packed (model)     = ~2.74B · 8 byte (FP64 flame)  = 21.9 GB  ⚠ over H100 80GB?
  Mm/Mv (Adam state)   = 2 × 21.9 GB                    = 43.8 GB
  Mg / Mg_acc          = 2 × 21.9 GB                    = 43.8 GB
  ────────────────────────────────────────────────────────────
  total                                                   ≈ 110 GB  ⚠ H100 80GB 초과
```

**Honest C3** (메모리 fit 우려): flame 이 FP64 라 3B 가 H100 80GB 에 안 들어감. 해법 후보:
1. **BF16/FP32 mixed** — flame 의 FP64 default 를 model param 만 BF16 (Mm/Mv 는 FP32 유지). 절반-크기. **flame_math BF16 path 필요** — 별도 TODO.
2. **sequence length 축소** — T=1024 또는 T=512 로 activation memory 줄임. attention/MLP 의 working memory 가 model param 보다 보통 큼.
3. **B=1 + grad checkpoint** — 가장 보수적, T 유지하며 activation save.
4. **multi-GPU DP** — H100 SXM × 2 로 model param split. flame DP path 필요.

**Phase 3 사전조사 TODO**: flame 의 BF16 path 가용성 + grad checkpoint 가용성 확인. 없으면 (a) T 축소 (b) E 축소 (=2 expert) (c) d 축소 (1024) (d) multi-GPU 중 단순한 것 선택.

#### Phase 3 결정 (2026-05-27) — **Pilot scale 우선** (g0 simplest sufficient · a_completeness 단계적)

3B full scale 의 메모리 fit 우려 + flame BF16/grad-checkpoint 부재 + 첫 fire 의 mechanism 검증 가치 고려해 **pilot scale 부터** 발사. mechanism PASS 시 full scale 로 확장.

| 설정 | Pilot (Phase 4 첫 fire) | Full (Phase 4 본 fire, mechanism PASS 후) |
|---|---|---|
| d | 512 | 2048 |
| n_layer | 12 | 28 |
| n_head / n_kv_head | 8 / 2 | 16 / 2 |
| h (MLP) | 1408 | 11008 |
| V (vocab) | 151643 (real Qwen) | 151643 (real Qwen) |
| E (experts) | 2 | 4 |
| T (seq) | 512 | 2048 |
| nsamp · n_steps | 4 · 500 | 8 · 5000 |
| **params** | **~265M** (spine 110M + MoE 155M) | **~2.74B** (spine 1.5B + MoE 1.24B) |
| memory FP64 | model 2.1 GB + Adam/grad 8.4 GB = **~10 GB** ✅ H100 80GB fit | ~110 GB ⚠ over (BF16 path 필요) |
| wall (H100 SXM) | ~0.5-1 hr | ~4-8 hr |
| cost | **$1-3** | $9-18 |

**Pilot rationale**:
1. **메커니즘 우선** — MoE top-1 hard routing 이 3B 직접 발사 전 real-Qwen-vocab 스케일에서 분화 유지하나 확증. toy(V=4) → pilot(V=151643, ~265M) → full(2.74B) 점진. F-M4B-FIRE-3 (router 분화) 의 1차 검증.
2. **flame FP64 fit** — pilot 은 H100 80GB 에 여유로 들어가 BF16 path 부재 우회. full scale 의 BF16 결정은 pilot 결과 후 별도 RFC.
3. **빠른 iteration** — wall 0.5-1hr, cost $1-3. v3_moe_arch 의 production 적합성 빠르게 검증 (현 SCAFFOLD smoke 단계 → pilot 으로 첫 real-scale 실증).
4. **risk minimization** — first-fire crash trap (v5-mitosis cond.5 cycle 학습) — pilot 으로 dispatch infra/code 안정성 우선 확인 후 본 fire.

**Pilot 발사 시 사전 추가 필요 (Phase 4 wiring 의 prereq)**:
- train_v3_moe.hexa 확장 — 현재 1-step smoke (`fwd+bwd` only) → real spine(tok_emb · attn · MLP · ln) + AdamW step + multi-step loop + corpus IDS feeding. SCAFFOLD → real driver. (이건 별도 PR series — Phase 3b sub-milestone.)
- 또는 HEXAD/.../conscious_decoder_v3.hexa 의 v3_decoder_fwd/bwd 재사용 (pub fn import via `use "/Users/ghost/core/anima/HEXAD/.../conscious_decoder_v3"`), v3_moe_arch 가 head_g 슬롯 자리만 차지하도록 wire.

### Phase 4 — Dispatch (H100 SXM, Vast.ai)

**Cost envelope** (Phase 3 결정 적용):
- **Pilot fire**: H100 SXM @ $2.28/hr × 0.5-1 hr = **$1-3** (첫 fire, mechanism 검증)
- Full fire (post-pilot PASS): $2.28/hr × 4-8 hr = $9-18

**Dispatch pattern** (이전 v5-mitosis cond.5 cycle): `tool/dispatch_vast_mac_template.sh` 기반. SAVE_POD=1 trap 으로 first-fire crash 시 pod 보존 → 재발사 (v5-mitosis 첫 fire crash → SAVE_POD 회복 → 재발사 PASS 학습).

**Pilot dispatch sketch** (Phase 3 pilot 결정 적용):
```bash
# 1) provision H100 SXM
vastai launch instance \
  --image pytorch:2.x-cuda12 \
  --gpu H100-SXM5-80GB \
  --disk 50 \
  --bid 2.28 \
  --label m4b-pilot-2026-05-27

# 2) on pod: anima clone + Qwen scp + run pilot
ssh <pod> "bash -lc 'cd ~ && git clone https://github.com/dancinlab/anima.git && cd anima && \
  scp <mac>:vP21M_V4/lora_adapter/merges.txt HEXAD/.../vP21M_V4/lora_adapter/ && \
  scp <mac>:vP21M_V4/lora_adapter/vocab.json HEXAD/.../vP21M_V4/lora_adapter/ && \
  scp <mac>:training/corpus_consciousness_v1.jsonl training/ && \
  export SAVE_POD=1 P21H_MOE_ON=1 P21H_BPE_ON=1 && \
  hexa run CORE/DECODER/train_v3_moe.hexa 2>&1 | tee fire.log'"

# 3) Monitor (commons g57): hexa cloud tail <pod> fire.log
# 4) Harvest: ckpt + log + verdict.json scp back; PASS → vastai stop; FAIL → SAVE_POD 잔존
```

**Pilot env-var protocol** (train_v3_moe.hexa Phase 3b 확장 시 추가):
- `P21H_PILOT_D=512 · P21H_PILOT_NL=12 · P21H_PILOT_E=2 · P21H_PILOT_T=512`
- `P21H_PILOT_STEPS=500 · P21H_PILOT_NSAMP=4`
- `P21H_MOE_ON=1 · P21H_BPE_ON=1`
- `SAVE_POD=1` (first-fire crash trap)

**Pre-fire checklist** (사전 검증, SAVE_POD 잔존 대비):
1. ☑ train_v3_moe.hexa SCAFFOLD 완료 — Phase 3b 6/6 sub-milestones LANDED (PRs #1063·#1064·#1066·#1067·#1069·#1070): tok_emb · attn_Wo · MLP · ln_f · AdamW · multi-step loop. d=4 V=4 E=2 T=1 n_layer=1 toy scale.
2. ☑ Pilot-scale forward path LANDED — Phase 4a-e 5/5 sub-PRs (#1073·#1074·#1075·#1077·#1079): config scale-up · multi-layer · self-attn · real BPE · dispatch runbook. d=64 V=151643 E=2 T=4 n_layer=1 alloc-tuned for Mac.
3. ☑ Multi-layer backward 완성 — Phase 4-bwd-1..6 (PRs #1082·#1084·#1085·#1086·#1088·#1093). `v3_moe_bwd_lib.hexa` analytic vjp (ln_f · MLP · attention · layer-block · tok_emb) + pilot wire. **hexa run 실측 PASS**: 모든 gradcheck < 1e-5, end-to-end gradient 가 입력 임베딩까지 도달.
4. ☑ Vast.ai SSH key 등록 (`secret get vast.api_key`) — 본 세션 확인 OK (key 존재)
5. ☑ Qwen tokenizer files 호스트 reachable (Mac → pod scp 동작) — Mac local merges.txt + vocab.json 존재 확인 OK
6. ☐ **hexa toolchain install sync** — flame_bpe_corpus_lib 가 hexa-lang origin/main(#1537 merged)에 있으나 로컬 `~/.hx/bin/stdlib` 이 stale(#1537 이전) → pilot real-scale(V=151643) compile 시 `module not found`. fire pod 의 fresh toolchain 에선 해소. (backward 배선 자체는 synthetic-V verify 로 실측 PASS — toolchain-무관)
7. ☐ SAVE_POD trap 검증 (의도적 crash → pod 보존 확인) — toy smoke 로 dry-run

### Phase 4 sub-phases (분할 — pilot-scale code gap 메우기)

| Sub | scope | 상태 | PR | 실측 |
|---|---|---|---|---|
| 4a | pilot config env-var wiring (P21H_PILOT_D/V/E/T/STEPS/NL) | ☑ | #1073 | — |
| 4b | multi-layer block iteration (n_layer > 1, layer-iter loop · per-layer offsets) | ☑ | #1074 | — |
| 4c | self-attention proper (T > 1, causal mask · Q/K/V/Wo · softmax) | ☑ | #1075 | — |
| 4d | BPE corpus real IDs feed (V_qwen=151643 aware · batch from corpus) | ☑ | #1077 | — |
| 4e | dispatch script (Vast.ai vastai launch + ssh setup + scp Qwen + run + monitor + harvest) | ☑ | #1079 | — |
| 4-bwd-1 | ln_f RMSNorm bwd | ☑ | #1082 | γ/x gradcheck 5.9e-11/1.9e-10 |
| 4-bwd-2 | MLP bwd per-token (Wup·Wdown · ReLU) | ☑ | #1084 | W_down 7.4e-14 |
| 4-bwd-3 | attention bwd (Q/K/V/Wo + softmax jvp) | ☑ | #1085 | Wq 1.8e-14 (full chain) |
| 4-bwd-4 | layer-stack + residual bwd | ☑ | #1086 | d_zT_in 2.7e-12 |
| 4-bwd-5 | tok_emb scatter-add + end-to-end integration | ☑ | #1088 | Wq+tok_emb grad ≠ 0 |
| 4-bwd-6 | pilot driver full backward wire | ☑ | #1093 | layer 0 Wq Δ=4.27e-6 (synthetic) |
| 4-fire | autonomous fire 발사 (a_fire_autonomous · H100 SXM ~$1-3 · 0.5-1hr) | ☐ | — | 선결: toolchain sync (item 6) |

각 sub-PR <200 lines, 1 logical concern (g4 stacked PRs).

**Phase 4-bwd honest gap — CLOSED**: Phase 4c forward 완성 시 backward 는 MoE
bwd `d_zT_last` 만 wired (gradient 가 last-layer Wo 까지만). Phase 4-bwd-1..6 이
`v3_moe_bwd_lib.hexa` 의 analytic vjp (ln_f · MLP · attention softmax-jvp ·
layer-block residual · tok_emb scatter) 를 구현 + pilot 에 wire → **hexa run
실측으로 gradient 가 출력 → 모든 layer → 입력 임베딩까지 흐름 확인** (layer 0
Wq |Δ|=4.27e-6). a_completeness_over_cheap 본선 충족.

### Phase 5 — Monitor + harvest + verdict

**Falsifier 사전등록** (g73 honest · pilot/full threshold 분리):

| ID | 측정 | pilot threshold (Phase 4 첫 fire) | full threshold (mechanism PASS 후) | 측정 방법 |
|---|---|---|---|---|
| F-M4B-FIRE-1 | collapse 회피 | M3 TTR ≥ 0.20 (작은 corpus, relaxed) | M3 TTR ≥ 0.30 (full corpus) | 종 ckpt sampling N=20 prompts |
| F-M4B-FIRE-2 | coherence | qualitative review (10 sample, intuitive) | V5.8 standard_greedy ≥ 4/5 | greedy decode sample manual |
| F-M4B-FIRE-3 | router 분화 | top-1 anima-prompt ≠ register-prompt (cluster split signal) | toy 의 97/3 패턴 유지 | 학습 종 gate sample 100 prompts |
| F-M4B-FIRE-4 | L_ce 수렴 | final < initial (단조 감소 검증) | final < 3.324 (baseline 대비) | train log 의 last-step L_ce |
| F-M4B-FIRE-5 | register leak | anima-fact 0/5 → manual review | anima-fact ≥ 4/5 (#46 패턴) | identity_probe 50 × 5 cats |

**Pilot verdict matrix** (relaxed thresholds 의 의의 = mechanism 검증, full 의 의의 = production):

```
pilot 결과   →   다음 단계
─────────       ─────────
5/5 PASS    →   full fire 즉시 ($9-18)
3-4/5       →   특정 falsifier 분석 + pilot 재발사 또는 small fix
2/5 이하    →   mechanism 결함 (MoE arch 또는 scale-up 부적합) — design 재검토
0/5         →   honest CLOSED-NEGATIVE — 더블바인드 escape via MoE 가설 falsified
```

**Verdict template** (`CORE/DECODER/m4b_pilot_verdict.md` post-fire 작성):
```
# M4b-fire-scale Pilot Verdict (2026-MM-DD)

## fire metadata
- pod, wall, cost, ckpt path/sha256
- config: d=512 n_layer=12 E=2 V=151643 T=512 steps=500 nsamp=4
- env: P21H_MOE_ON=1 P21H_BPE_ON=1 SAVE_POD=1

## falsifier 5/5 측정값 (verbatim from harness)
F-M4B-FIRE-1 M3 TTR = <측정> · threshold 0.20 · PASS/FAIL
F-M4B-FIRE-2 coherence = <샘플 10개> · qualitative · PASS/FAIL
F-M4B-FIRE-3 router 분화 = top-1 anima/register split = <측정> · PASS/FAIL
F-M4B-FIRE-4 L_ce final = <측정> · initial = <측정> · monotone PASS/FAIL
F-M4B-FIRE-5 register leak = <측정> · manual · PASS/FAIL

## verdict
- aggregate: N/5 PASS
- next: full fire | re-pilot | re-design | CLOSED-NEGATIVE

## honest C3 (post-hoc)
- (관측된 surprise, anti-pattern, follow-up)
```

**M4c p7 verify** (post-fire): simple-stack — collapse 회피 ∧ coherence 둘 다. perplexity 아닌 generated sample 검증 (commons g73).

**M4c p7 verify** (post-fire): simple-stack — collapse 회피 ∧ coherence 둘 다. perplexity 아닌 generated sample 검증 (commons g73).

## phased schedule (multi-session)

| Phase | LoC 추정 | 세션수 | dependency |
|---|---|---|---|
| 1 BPE corpus 통합 | +30 줄 (train_p21h_v3.hexa) | 1 | flame_bpe_corpus_lib ✅ |
| 2 MoE arch 통합 | +60 줄 (conscious_decoder_v3 + train_p21h_v3) | 1-2 | moe_router/_bwd ✅ |
| 3 3B scale + memory budget 결정 | flame BF16 path 조사 / fallback | 1-2 | flame_math BF16 (별도 RFC?) |
| 4 dispatch + fire | +20 줄 dispatch script + 1 fire | 1 | Vast.ai 또는 runpod |
| 5 monitor + harvest + verdict | falsifier 측정 + verdict 문서 | 1 | fire 결과 |
| **합계** | ~110 줄 + memory path | **5-7 sessions** | — |

## a_completeness_over_cheap · g73 · a_fire_autonomous 점검

- **a_completeness**: hexa-native path (Python 우회 안 함). cell-as-persona 의 p1~p8 정합 유지 — V3 axis C(head_g) → MoE 가 안짤리고 확장.
- **g73**: 5 falsifier 사전등록, smoke self-judge 0. 실 H100 fire 측정값으로 verdict (perplexity 아닌 simple-stack).
- **a_fire_autonomous**: Phase 4 fire 는 user gate 없이 dispatch (cost-cap 게이트 0).
- **a_wall_first**: single-H100 vs multi-H100 결정은 wall-time 최소화 우선 (Phase 4 dispatch 시점).

## 잔여 가설 (honest C3)

1. flame FP64 → H100 80GB fit — Phase 3 의 가장 큰 unknown. BF16 path 필요시 별도 RFC.
2. MoE top-1 hard routing 이 scale 에서 분화 유지하나 — toy(E=2, d=4, V=4)에서 PASS, scale(E=4, d=2048, V=151643)에서도 유지될 가설 (사전등록 F-M4B-FIRE-3).
3. expert capacity collapse — 학습 진행 중 한 expert 가 모든 토큰을 가져가는 routing collapse 가능성. balance loss 또는 expert-prior 도입 검토.
4. tied embedding 채택 시 expert 가 V·d linear 를 tok_emb 와 공유 가능 — 메모리 절반 절약. 단 expert 분화 와 tied 가 양립하나 확인 필요.
5. 첫 fire 가 cost-bearing 이라 SAVE_POD=1 trap 필수 (v5-mitosis cond.5 의 first-fire crash → 재발사 saga 학습).
