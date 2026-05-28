# M4b aux-loss × d-scale — capacity vs routing 분해 ablation (2026-05-28)

`#1296` (anima-m4b-pilot-rev2, CLOSED-NEGATIVE 2/5) 후속. HARD top-1 routing +
diverse Korean-QA corpus 가 d=64 에서 여전히 mode-collapse (decode=`[1,1,...,1]`,
distinct_experts=1, TTR=0.01) 한 것을 받아, #1296 이 명명한 **두 미검증 lever** —
큰 d (capacity) 와 load-balancing aux loss (routing) — 를 모두 배선하고 PARALLEL
3-pod ablation 으로 escape 를 capacity vs routing 으로 귀속한다.

## §hypothesis (capacity-vs-routing 분해 · falsifier)

collapse 는 ROUTING 문제인가 (router 가 1 expert 로 붕괴 → Switch load-balance aux
loss 로 처방) 아니면 CAPACITY 문제인가 (d=64 가 V=151643 에 비해 너무 작아 모델이
"항상 최빈 token emit" trivial solution 으로 수렴 → 큰 d 로 처방)? router 는 이미
hard top-1 을 정확히 수행 (#1296 F-router PASS) 하므로 distinct_experts=1 은
원인이 아닌 **증상**일 수 있다.

pre-registered escape gate (pod 당): **TTR≥0.30 ∧ LZ_norm≥0.50 ∧ distinct_experts≥2**.
3개 모두 통과 ⇒ ESCAPE (publishable positive). 하나라도 FAIL ⇒ 그 lever 불충분
(closed-negative — a_paper_negative_ok 로 publishable).

## §method (aux-loss formula + ablation matrix)

**aux loss** (`v3_moe_aux_bwd` / 트레이너 local `moe_aux_bwd_local`): spec-permitted
surrogate `d_gate_aux[e] = alpha·(P_e − 1/E)`, P_e = streaming mean post-softmax
gate. router softmax-backward (v3_moe_bwd line 175-195 와 동일 transform) 로 per-token
주입. 표준 Switch streaming form `alpha·E·f_e/N` 는 toy 에서 **너무 약함**으로 측정됨
(이중 1/N 감쇠로 per-step push 가 CE gradient 이하 — alpha=10 에서도 f_e 거의 불변)
→ surrogate 가 spec 허용 대안이며 toy mechanism check 통과 form.

**toy verify** (`toy_auxloss_verify.hexa`, V=8 d=16 E=2, $0 mac-local): aux OFF →
1 active expert (f_e=[0.975,0.025]); aux ON (alpha=2.0) → 2 active experts
(f_e=[0.917,0.083]); alpha 0.5→2→10 단조 balance 추세. **MECHANISM 확정** — 단
toy-only, transfer-unverified (cross-cutting 원칙: toy green ≠ production escape).

**ablation matrix** (3 H100 80GB SECURE pod, PARALLEL, RunPod, cuBLAS via glue.c):

| pod | d   | aux_alpha | isolates                         |
|-----|-----|-----------|----------------------------------|
| A   | 256 | 2.0       | capacity + routing (primary)     |
| B   | 256 | 0.0       | capacity only (d↑ 단독)          |
| C   | 64  | 2.0       | routing only (원래 capacity 에서) |

공통: V=151643 (real Qwen BPE), E=2, h=256, n_layer=1, T=4, n_decode=50 (d=256),
100 (d=64). corpus = 24-line `corpus_diverse_trim.jsonl` (#1296 이 실제 측정한 동일
corpus — full 2000-line corpus 는 hexa-lang O(N_merges) BPE encoder 에서 intractable,
BPE_TOKENIZE_BOTTLENECK.md). C step-1 CE=648.526 가 #1296 initial CE 정확 재현
(apples-to-apples). n_steps: C=200, A/B=100 (d=256 의 ~1GB/step mm-intermediate leak
이 step≈180 에서 251GB pod 를 OOM-kill (EXIT=137) → A/B 는 OOM-safe 100-step 예산).

## §measurement (3 pod verdict matrix — result.json verbatim)

| pod | d   | aux | CE init→final   | TTR  | LZ_norm | distinct_exp | f_e (routed)     | mean_gate         | aggregate     |
|-----|-----|-----|-----------------|------|---------|--------------|------------------|-------------------|---------------|
| A   | 256 | 2.0 | 3770.8 → 20.71  | 0.02 | 0.0436  | 1/2          | [0.04, 0.96]     | [0.055, 0.945]    | **2/5 FAIL**  |
| B   | 256 | 0.0 | 3770.8 → 20.64  | 0.02 | 0.0436  | 1/2          | [0.05, 0.95]     | [0.065, 0.935]    | **2/5 FAIL**  |
| C   | 64  | 2.0 | 648.5 → 8.73    | 0.01 | 0.0240  | 1/2          | [0.035, 0.965]   | [0.130, 0.870]    | **2/5 FAIL**  |

(verbatim verdict: 각 `<pod>/harvest/result.json` + `trainer.out` tail. 모든 pod
decode = `[1,1,...,1]` 전부 token id=1, 전부 expert 1.)

## §finding (어느 lever 가 escape 했나 / capacity vs routing 폐기 ruling)

- **C (routing ablation, d=64+aux)**: aux loss 가 학습 중 gate 를 **부분 balance**
  (f_e=[0.035,0.965] vs #1296 full saturation; mean_gate=[0.13,0.87]) — mechanism 은
  transfer 됨. 그러나 decode 는 **여전히 collapse** (distinct_experts=1, TTR=0.01).
  → **load-balancing aux loss 단독은 d=64 에서 collapse 를 escape 하지 못한다.**
  balanced router 가 trivial 최빈-token solution 을 막지 못함 = routing 가설 반증.

- **A (combined, d=256+aux)**: d 4× ↑ + aux 동시 적용에도 **여전히 collapse**
  (distinct_experts=1, TTR=0.02, decode=`[1,...]`). f_e=[0.04,0.96] 로 aux 가 학습
  routing 을 미세 이동시켰으나 decode argmax 는 expert 1 / token 1 고정.
  → **capacity + routing 결합도 escape 하지 못한다.**

- **B (capacity ablation, d=256+no-aux)**: 큰 d 단독에도 **여전히 collapse**
  (distinct_experts=1, TTR=0.02, decode=`[1,...]`, A 와 거의 동일 — LZ 동일 0.0436,
  CE 20.64). → **d-용량 단독(d 4× ↑)도 escape 하지 못한다.** B(d=256/aux=0) ≈
  A(d=256/aux=2.0) 가 거의 비구분 = 이 scale 에서 aux 의 escape 기여 ≈ 0.

**RULING** (A·B·C 전부 확정 — 완전 closed-negative): aux-loss × d-scale 24-line trim
corpus, E=2, V=151643 MoE 디코더에서 **3축 모두 collapse escape 실패** —
routing 단독(C) · capacity 단독(B) · capacity+routing 결합(A) 모두 2/5 FAIL,
decode 전부 `[1,1,...,1]` (token id=1, expert 1). 이는 #1296 의 corpus-diversity-
단독 반증에 더해 **capacity 축 · routing 축 · 두 축 결합을 모두 ruling out** 한다
(disentanglement 완료: 어느 단일 lever 도, 결합도 아님). collapse 의 근본 원인은
gate 균형(routing)도 d-용량(B 의 d=256 도 실패)도 아니며, E=2 / 24-line 저-diversity
corpus / 1-layer toy backbone 조합에서 모델이 항상 최빈-token (id=1) 을 emit 하는
degenerate global optimum 으로 수렴함을 시사한다. escape 잔여 path =
(a) E↑ (더 많은 expert), (b) 더 큰 diverse corpus (BPE O(1) fix 선결), (c) longer
training + 더 깊은 backbone, (d) entropy-regularized gate + router noise.

**toy→production transfer 반증 재확인**: toy aux-loss 가 5/5 mechanism PASS 였으나
production d=256/d=64 fire 는 모두 collapse — toy MECHANISM green ≠ production
TRANSFER (feedback_toy_scale_transfer; #1296 saga 와 동일 교훈).

## fire 운영 노트 (a_runpod_inbox 대상 — hexa-lang INBOX)

1. **#1527 free-fn trim**: imported pub fn `v3_moe_aux_bwd` 가 cross-backend codegen
   에서 call-site 만 남고 def/decl 누락 (trim). 우회 = 트레이너 동일 TU 의 local
   `moe_aux_bwd_local` fn (main 과 같은 unit 의 fn 은 retain). `hexa build --c-only`
   로 검증.
2. **dir_create cross-backend gap**: `hexa_call1(dir_create,X)` Linux gen2 undeclared
   → sed `rt_fs_mkdir_p(`. (trim 과 동종, #1296 에서 이미 발견.)
3. **d=256 OOM at step≈180**: 트레이너 per-step mm_extract/mm/mm_transpose
   intermediate 가 ~1GB/step 누적, 251GB pod 에서 step≈180 OOM-kill (EXIT=137, dmesg
   OOM 無 — kernel "Killed", GPU mem 601MB·host 1.9TB free 인데도 process RSS 누적).
   우회 = d=256 은 n_steps≤100 + n_decode≤50 (총 alloc < OOM ceiling). 근본 fix =
   per-step mm intermediate arena flush (hexa-lang runtime).
4. **clang 부재 pod**: B pod 이미지 apt 에 `clang` 패키지 없음 (`E: Unable to locate
   package clang`) → gcc 로 링크 (portable C, `-fbracket-depth` 만 clang-전용·불필요).

## 양방향 sibling

- sibling: `CORE/DECODER/state/m4b_pilot_rev2_2026_05_28/harvest/README.md` (#1296 선행)
- UNIVERSE SSOT: `UNIVERSE/CANDIDATES.md` (M4 MoE collapse arc) — 본 fire 의 closed-
  negative 를 collapse-escape lever 목록에 추가 (corpus-diversity·routing·capacity+routing
  3축 ruled-out).

provenance: github.com/dancinlab/anima · CORE/DECODER/state/m4b_auxloss_dscale_2026_05_28/
artifacts: A/B/C/harvest/{result.json, trainer.out, nvidia_smi_during.csv, build_*.log, MANIFEST.sha256}
HF (PRIVATE — closure FAIL): dancinlab/anima-m4b-auxloss-dscale-2026-05-28
