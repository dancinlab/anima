---
id: H_1441
slug: 1441_contrastive_falsifiability
title: G6 IDEATION ★ FALS-depth — CONTRASTIVE falsifiable-vs-nonfalsifiable minimal-pair objective
group: gate-dig (G6 IDEATION ★) — FALS-depth TRAINING side r6
terminal_tier: 🧱 WALL=CAPACITY (ENGINE-NATIVE terminal, 2026-06-22) — form-contrastive objective(pos=full falsifiable claim, neg=blanked-leg non-falsifiable)이 live core/bytegpt_decode 90-frag 재측정에서 form 만 install: TRAINED 모든 arm FALS=5.0, B3 cross-shuffle NO-collapse(FALS_shuf 5.0 = FALS_in 5.0) + B2 DIST 4.67<5 → 🧱. 이전 BLOCKED(substrate-speed + vast pod 41556247/41790394 소멸)이 hexa PR #3745 farr noop-free + process-isolation(frag당 fresh hexa process)로 해소되어 90-frag 완주 → score 도달. sister H_1464(pairing-contrastive)와 동일 .bin/objective → 같은 engine-native frozen 5-bar(state/verdicts/1464_pairing_contrastive_bind/H_1464.txt, header="H_1441 contrastive ENGINE-NATIVE FROZEN 5-BAR")가 양 가설 동시 resolve. G6 capacity-wall 수렴 렌즈.
wired: ENGINE-NATIVE 재측정 DONE (2026-06-22) — live core/decode.hexa via state/1464_pairing_contrastive_bind/engine_decode_batch_cli.hexa, 3 trained .bin × 30 frag = 90 frag → g6_common frozen 5-bar VERBATIM 채점 → 🧱 WALL=CAPACITY. terminal 🧱 이므로 live core/ wire-in 불필요(objective 가 binding 못 깸). farr CPU path = byte-identical to forge GPU(RFC-040 seam) 이므로 engine-native. raw: state/verdicts/1464_pairing_contrastive_bind/H_1464.txt.
verdict_dir: state/verdicts/1441_contrastive_falsifiability/
terminal_verdict: state/verdicts/1464_pairing_contrastive_bind/H_1464.txt
date: 2026-06-22
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
> **serial ~18h** (PHASE 1+2 합 ~30h). decode.hexa 에 GPU/device decode 경로 **없음**(farr_matmul = CPU GEMM only).
> → $15-40 를 known 30h CPU 벽 + corrupt-base 리스크에 태우는 것은 a_completeness/c16 상 부당. **여전히 BLOCKED (type-c 인프라 벽)**.
> 갱신된 재개조건: (1) bytegpt_decode 에 GPU/device decode 경로 추가(forge), 또는 (2) decode per-token CPU GEMM 을
> 실측 ≥4× 가속하는 runtime 변경 — 둘 중 하나가 land 한 뒤에야 fire. (decode CLI 의 stale `CORE/`→`core/` import 는 선제 수정함.)

> ✅ **2026-06-20 재개조건 충족 — substrate-speed 벽 BROKEN, decode 진행 중** (state/verdicts/1441_contrastive_falsifiability/H_1441_engine_native_UNBLOCKED_INPROGRESS.txt):
> 위 재개조건 (1)+(2)가 둘 다 land 했다 — native-GEMM forward 가 core/decode.hexa 에 배선됨
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

> ✅✅ **2026-06-22 ENGINE-NATIVE TERMINAL — 🧱 WALL=CAPACITY** (state/verdicts/1464_pairing_contrastive_bind/H_1464.txt, header "H_1441 contrastive ENGINE-NATIVE FROZEN 5-BAR"):
> 이전 BLOCKED 의 OOM/누수 벽(hexa decode per-frag farr noop-free 누수)을 hexa PR #3745 + **process-isolation**
> (frag당 fresh hexa process 로 RSS 리셋 → 누수 미적층)로 해소 → 90 frag(3 bin × 30 frag) 완주 → score 도달.
> live core/decode.hexa(via engine_decode_batch_cli.hexa)로 decode → g6_common frozen 5-bar VERBATIM 채점.
> **TRAINED(contrastive): FALS_in=5.0 · DIST_in=4.6667 · FALS_shuf=5.0 · FALS_ho=5.0 · BASE FALS_in=0.0.**
> B1 FALS-FLOOR 5.0≥1 PASS · **B2 COUNT DIST 4.6667<5 FAIL** · **B3 X-SHUFFLE 5.0<5.0 NO-collapse FAIL(결정적)** ·
> B4 HELD-OUT 5.0≥1 PASS · B5 vs-BASE 5.0≥0+1 PASS · CTRL SHUF-CORP 5.0−0.0 PASS → **🧱 WALL=CAPACITY**
> (bars B2,B3 fail; form 은 install 됐으나 comparator↔measurable WELD 못 함 = 1435/36/37 와 같은 실패모드).
> sister H_1464(pairing-contrastive)는 mirror 에서 B3 COLLAPSE(🟢 LEARN-GAP)였으나 engine 에서 동일 NO-collapse 로
> 반전 = mirror bilinear collapse 는 표현공간 construction artifact. 두 가설 모두 G6 capacity-wall 에 수렴.
> substrate: aiden(RTX5070) 병행 fallback decode 는 vast pod(41921615, conc-80)이 먼저 완주하여 redundant → 정리.
> decode 가 farr CPU path 여도 RFC-040 seam 으로 forge GPU 와 byte-identical → ENGINE-NATIVE terminal(c9, no tune-to-green).
>
> ⚠️ **B3 해석 NUANCE (H_1467 follow-on, 미해소)**: 이 terminal 🧱 는 FROZEN h1305 **structural** detector 의 5-bar
> 기준이다(B3 cross-shuffle NO-collapse). 별도 가설 H_1467(PAIRING-AWARE clause-proximity detector)가 H_1464 의
> 같은 frozen fragment 를 재채점하니 PAIRING collapse 2.67(structural 0.0) 로 B3 가 reopen 되어 H_1464 를 🟠
> PARTIAL-REVISION 으로 demote(unmerged worktree commit d24c5cb63). H_1441 의 자매 재채점(h1467 clause-proximity
> .hexa)은 **BLOCKED**(자매 engine fragment out_*.txt 로컬 부재 → .bin 재decode = COST-GATE, 사용자 go 대기;
> ING g6-siblings-rescore). 따라서 H_1441 의 B3 axis 가 capacity 인지 measurement-fault(LEARN-GAP)인지의 최종
> 분류는 h1467 detector 재채점이 land 한 뒤 확정 — 현재 terminal 🧱 는 frozen h1305 5-bar 기준의 정직한 결과이며,
> H_1467 라인이 reopen 가능성을 명시(c9, a_break_the_wall: measurement-fault 가능성 미배제).

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
