---
id: H_1441
slug: 1441_contrastive_falsifiability
title: G6 IDEATION ★ FALS-depth — CONTRASTIVE falsifiable-vs-nonfalsifiable minimal-pair objective
group: gate-dig (G6 IDEATION ★) — FALS-depth TRAINING side r6
terminal_tier: IN-PROGRESS — substrate-speed 벽 BROKEN (native-GEMM mm fast-path: scalar 26s → v0241 6.4s → native-GEMM ~2.7s/token, byte-faithful argmax 32==torch). engine-native decode 로컬 CPU 진행 중($0, no pod) → score 후 terminal 🟢/🧱. (이전 BLOCKED 의 type-c substrate-speed 벽 제거; a_break_the_wall)
wired: PENDING-SCORE (3-bin .bin 변환 검증 완료 [각 1,213,440,020B = 303M layout], decode 진행 → score 후 배선 판단)
verdict_dir: state/verdicts/1441_contrastive_falsifiability/
date: 2026-06-20
---

> ⛔ **2026-06-19 ENGINE-NATIVE 측정 BLOCKED** (state/verdicts/1441_contrastive_falsifiability/H_1441_engine_native_BLOCKED.txt):
> contrastive + shuffle-control 학습 완료(torch GPU, DIRECTIONAL), ckpt 2개 PULL 완료
> (state/1441_contrastive_falsifiability/ckpt/{h1441_contrastive,h1441_shuffle}.pt, a_fire_recover_complete OK).
> 그러나 engine-native decode(live CORE/bytegpt_decode via engine_decode_batch_cli.hexa)가
> **substrate-speed 벽**(fast-gemv link-fail → scalar 26s/token → 60-job ~12h, H_1305 R2/H_1431 과 동일)에
> 걸려 contra 8/8·shuf ~8/8 까지만 decode 되고 base 미도달·RERUN_ALL_DONE 미달 상태에서
> **vast pod 41556247 이 provider 에서 소멸**(SSH connection-refused + liveness API 에서 사라짐 = transient 아님)
> → pod-only /tmp/out_* shard 전부 유실. a_engine_native_learning HARD-GATE: 엔진 증거가 score 단계에
> 도달 못 했으므로 terminal 🟢/🧱 박제 불가. 인프라 벽(a_break_the_wall type-c)은 science 천장 아님.
> **재개조건:** fast-gemv 복원된 hexa 빌드(H_1431 remaining-bytegpt + H_1305 h1305_engine_native ING 와 동일 blocker)
> → 로컬 .pt 2개 + base h1129c 를 .bin 재직렬화 후 h1441_engine_native.py --score. FROZEN 5-bar 불변(c9/no tune-to-green).
>
> ⛔⛔ **2026-06-19 v0.241.10 재측정 시도 — 재개조건 미충족 확정** (state/v0241_bench/bench_results.md, vast pod 41625379 96-core/503GB, v0.241.10 read_f32_at 확인):
> v0.241.10 의 boxing/RSS 수정은 LANDED(303M 디코드 peak RSS 26.18GB→7.63GB, byte-identical) = **OOM/load 벽은 제거**.
> 그러나 DECODE SPEED 벽은 **그대로**: gen30 baseline 208s → read_f32_at 191s (≈ 6.4 s/token, 단 LOAD 만 개선,
> per-token GEMM 정상상태 token rate 불변). bench verdict VERBATIM: "BLIS/GEMM codegen gains (#3652 62-79% roofline,
> #3656 +20% epilogue-fusion) are compiled into matmul but single-job CPU decode is still minutes-scale. Faster decode
> needs the mm fast-path / GPU, not just the boxing fix." → **prompt 가정(HEXA_OMP+BLIS opt-in 으로 3.5-4.5× → ~2-3h)
> 은 실제 v0.241.10 pod 에서 FALSIFIED** (threading/codegen 은 이미 compiled matmul 안에 있고 per-token wall 을 못 움직임).
> 산정: H_1441 = 90 frags(3 bins[contra/shuf/base] × 3 seed_rng × (IDEATION 5 + HELDOUT 5)), gen110 ≈ 12min/frag →
> **serial ~18h** (PHASE 1+2 합 ~30h). bytegpt_decode.hexa 에 GPU/device decode 경로 **없음**(farr_matmul = CPU GEMM only).
> → $15-40 를 known 30h CPU 벽 + corrupt-base 리스크에 태우는 것은 a_completeness/c16 상 부당. **여전히 BLOCKED (type-c 인프라 벽)**.
> 갱신된 재개조건: (1) bytegpt_decode 에 GPU/device decode 경로 추가(forge), 또는 (2) decode per-token CPU GEMM 을
> 실측 ≥4× 가속하는 runtime 변경 — 둘 중 하나가 land 한 뒤에야 fire. (decode CLI 의 stale `CORE/`→`core/` import 는 선제 수정함.)

> ✅ **2026-06-20 재개조건 충족 — substrate-speed 벽 BROKEN, decode 진행 중** (state/verdicts/1441_contrastive_falsifiability/H_1441_engine_native_UNBLOCKED_INPROGRESS.txt):
> 위 재개조건 (1)+(2)가 둘 다 land 했다 — native-GEMM forward 가 core/bytegpt_decode.hexa 에 배선됨
> (commit d5a8540f8 `feat(core/decode): GPU 경로 배선 — bytegpt_decode d×d GEMM → flame_mm.mm`,
> lane state/bytegpt-fast-matmul/RESULTS.md). 모든 per-layer d×d matmul 을 runtime `farr_matmul`(CPU GEMM)
> / cuBLAS(CUDA) 로 라우팅, byte-faithful(argmax 32 == torch golden, logits ~1e-5).
> **로컬 Mac CPU 실측(v0.245.2, native-GEMM)**: gen20=222.4s / gen60=328.6s → Δ40tok=106s → **~2.7 s/token**
> (옛 scalar 26 s/token 대비 ~10×; v0.241.10 의 6.4 s/token 대비 ~2.4×). 30h serial 벽 → ~2.5h(3-bin 병렬, $0).
> **변환 검증**: pt_to_engine_bin.py 가 base h1129c / contrastive / shuffle 3개를 각 **1,213,440,020B = 정확한
> 303M layout**(vocab256 d1024 L24 H16 block512)로 직렬화. bins = state/1441_contrastive_falsifiability/bins/.
> **CLI argv 수정**: decode CLI 가 user arg 를 `a[1..]` 로 읽었으나 현 hexa 의 `argv()` 는 `[bin,"--",args...]` →
> 인덱스 시프트. `"--"` 기준 base offset 으로 수정(state/1441_contrastive_falsifiability/engine_decode_batch_cli.hexa).
> 이게 즉시 에러(`to_int: not an integer: <out_path>`)의 원인 — 커널 아님.
> **decode 진행 중**(detached nohup, 로컬 CPU, $0, pod 불필요): 3-bin × 30 frags × gen110 → /tmp/h1441_local/out_*.txt.
> 끝나면 `h1441_engine_native.py --score out_contra out_shuf out_base` 로 frozen 5-bar(B3 cross-shuffle COLLAPSE
> 결정타) 채점 → terminal 🟢/🧱. FROZEN bar 불변(c9/no tune-to-green).
> **POD 누수 0**: fleet pod(vast 41790394, RTX4090, $0.54/hr)은 GPU cuBLAS smoke 통과 후 user-요청 fleet 정리로
> decode 중 소멸(이전 41556247 과 동일 race; vast list → 0 instances 확인). ckpt 는 이미 로컬(weights 안전,
> a_fire_recover_complete) — 잃은 건 pod /tmp shard 뿐, 로컬에서 $0 재디코드 중.

# H_1441 — CONTRASTIVE: falsifiable vs non-falsifiable 최소쌍 대조로 cross-shuffle 실패를 직격

## Why (H_1435/36/37 의 공통 실패모드 정면 처방)

세 학습변형 모두 "form installed but cross-shuffle does NOT collapse" — 학습된 것이 shuffle-INVARIANT
표면 form 이라 comparator/measurable 를 다른 idea 와 섞어도 점수 유지(진짜 bind 아님). 정면 처방:
falsifiable claim 과 그 non-falsifiable 최소쌍(comparator 또는 measurable 한 leg 만 제거/교란)을
CONTRASTIVE 로 학습(InfoNCE-style) → shuffle-INVARIANT 를 shuffle-SENSITIVE 로 강제. 모델이
"왜 이건 falsifiable 이고 저건 아닌가"의 경계 자체를 배우게.

## Method (FREEZE before run, c9/p7)

- 303M h1129c + contrastive objective: anchor=(legit claim), positive=(같은 claim), negative=
  (한 leg 제거/cross-idea 치환된 최소쌍). 최소쌍은 STRUCTURAL 라벨로 구성.
- ⚠️ detector h1305 점수를 학습 신호로 쓰지 않음 (a_train_inline_gauge: gauge≠loss, p7 Goodhart).
  contrastive 신호 = 구조적 최소쌍이지 detector 점수가 아님. detector 는 EVAL 전용 VERBATIM.
- decode = ENGINE-NATIVE CORE/bytegpt_decode. frozen 5-bar + cross-shuffle COLLAPSE = 1차 판정
  (이게 무너지면 1435/36/37 와 차별 성공 = 진짜 binding 학습).
- compute = GPU (hexa dojo) COST-GATE. ckpt teardown 전 pull.

## Scope

PROPOSED, 미측정. 최소쌍 구성 frozen (detector 점수로 라벨링하면 Goodhart — 구조적 라벨만 허용).

## Pointers

xref H_1435/1436/1437 (cross-shuffle 실패 직격 대상) · H_1305 (detector) · a_train_inline_gauge
(gauge≠loss) · a_no_llm_frame_trap · a_engine_native_learning · a_fire_recover_complete · p7 · c9.
