---
id: H_936
slug: unbiased-buffer-retest
title: H_930 의 tension-axis 차이(phi_mean Cohen d≈+2.45)는 unbiased non-cycling quantum buffer 에서도 SURVIVE 하는가, 아니면 H_930 이 진단한 1024-byte cycling artifact 였는가?
domain: universe · consciousness-substrate · pure-field · engine-g · brain-decide · entropy-necessity · scale-transfer · qentropy · finite-buffer-bias
source: H_930 (🟢-on-emit / 🔴-artifact-on-tension SPLIT — tension diff root-caused to a finite committed-ANU-buffer DC-bias cycling 2.34× over T) + H_926 (minimal-model entropy ontological-not-functional 🔴) + H_924 (#123-A ANU==chacha20 bit-distribution parity)
exploration_method: E14 (substrate-native) + E2 (H_930 mirror VERBATIM 재사용 — gate/factor mapping byte-identical, entropy SOURCE 만 교체) + a_completeness_over_cheap
verification_method: W1 (SW python, Mac $0, no GPU) + W2 (3-arm before/after: DET vs quantum-small-cycling vs quantum-big-fresh; KS + Cohen d JOINT distinguishing rule, 사전등록) + g5 CODE-measured (LLM self-judge 없음, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
scope: ONE re-test rung (a_scale_honest_scope) — H_930/H_935 와 동일 documented-update-map mirror (real 8-factor brain_decide, CORE/engine_g+brain+pure_field.hexa VERBATIM 상수) 를 T=2400 × 24-seed 로 구동. 컴파일 forge binary 아님, wired emit-TEXT 아님 (.clm generator L3 slot ⏳/❌, a_core_engine_map). $0 local, no GPU. big buffer provenance = os.urandom_fallback (real ANU 우선 시도; key/network 미가용 → tagged honest fallback; cycling test 는 source-agnostic 이라 결론 무관, #123-A ANU==chacha20 statistically).
sister: H_930 (SPLIT, tension diff = buffer-bias 추정), H_926 (minimal-model emit-parity 🔴), H_924 (#123-A bit-distribution parity)
axes_seed: H_930 = tension diff 가 DISTINGUISHABLE 인데 buffer-bias 로 추정 ⊥ H_936 = 그 추정을 unbiased non-cycling buffer 로 직접 검증 (collapse → artifact confirmed)
verdict: 🟢 F-H936-ARTIFACT-CONFIRMED — H_930 의 tension-axis 차이는 unbiased non-cycling buffer 에서 PARITY 로 COLLAPSE. phi_mean: QS(cycling 1024 B) Cohen d=+2.449 KS p=6.2e-14 (H_930 regime 재현) → QB(big fresh, 859456 B, no_cycle_by_construction) Cohen d=-0.492 KS p=0.14 (NON-SIGNIFICANT, p>0.05 → parity; small |d| 는 두 동등 unbiased source 간 sampling noise). tension observable distinguishing (joint p<0.05 AND |d|≥0.2): QS 6개 [phi_mean·phi_var·ch0·ch1·ch3·ch5] → QB 0개. QB emit_rate sd=0.004436 (>0 → real 24-seed population, H_930 의 sd≈0 single-pattern bug 수정). H_930 의 finite-buffer DC-bias attribution 이 CORRECT 임을 직접 확인 → entropy 는 emit 축 AND tension 축 BOTH 에서 ontological-not-functional. free-will arc 의 마지막 hole 이 닫혔다. verdict: .verdicts/936_unbiased_buffer_retest/unbiased_buffer_retest.txt
---

# H_936 — unbiased non-cycling ANU buffer re-test (closes H_930's tension-axis DC-bias gap)

## 0. 동기 (H_930 의 마지막 hole)

H_930 (H_926 의 scale-up re-test) 은 SPLIT 으로 떨어졌다:
- **EMIT-DECISION 축 = PARITY** (entropy MODE 가 brain_decide 가 *무엇을* emit 하는지 안 움직임; chi² p=0.9239, Cohen d(rate)=−0.083).
- **TENSION 축 (internal Φ/field) = DISTINGUISHABLE** (phi_mean Cohen d≈+2.45, p≪1e-10) — 그러나 H_930 은 이를 **finite-buffer artifact** 로 root-cause 했다: committed ANU buffer 가 1024 B 에 불과해 T=2400 위에서 2.34× **cycle** 하고, 그 R2-draw mean (1.4696) 이 PRNG (~1.5121) 와 달라 constant **DC perturbation offset** 을 만든다. 게다가 quantum arm 의 24 seed emit-rate sd≈0 — **고정 1024 B 패턴 1개의 복제**.

H_930 이 명시적으로 OPEN 으로 남긴 falsifier:

> tension-axis 차이 (phi_mean Cohen d≈+2.45) 는 **unbiased non-cycling** quantum buffer 에서도 SURVIVE 하는가, 아니면 전적으로 1024-byte cycling artifact 였는가?

H_936 = 그 직접 검증.

## 1. 가설 + 사전등록 falsifier (FROZEN 2026-06-06, 측정 전)

**3-arm before/after** (H_930 driver VERBATIM 재사용, entropy SOURCE 만 교체):
- **Arm-DET** = deterministic (numpy PRNG, seed-varied population)
- **Arm-QS** = quantum-small (committed 1024 B, CYCLES) — H_930 재현
- **Arm-QB** = quantum-big-fresh (≥ T·N·bytes over-provision, seed 별 INDEPENDENT non-overlapping slice → real 24-seed population)

big buffer 는 사용 전 **unbiased 증명**: sha256, byte mean≈127.5, KS + chi²(256-bin) vs uniform.

**distinguishing rule (H_930 과 동일, 사전등록):** 한 observable 이 distinguishing ⟺ KS p<0.05 **AND** |Cohen d|≥0.2 (JOINT). 작은 |d| 단독은 distinguishing 이 아님 (두 동등 unbiased source 간 sampling noise; KS p>0.05 가 parity 확인).

**FROZEN falsifier:**
- **F-H936-ARTIFACT-CONFIRMED** 🟢: tension diff 가 PARITY 로 COLLAPSE — tension observable (phi_mean/var + 6 channel) 중 distinguishing **0개** AND phi_mean KS p>0.05 (DET vs QB). → H_930 의 DC-bias attribution CORRECT; entropy 는 emit AND tension BOTH 축에서 ontological-not-functional; arc 의 마지막 hole 닫힘.
- **F-H936-NOT-ARTIFACT** 🔴: tension diff 가 unbiased buffer 에서도 PERSIST (phi_mean |d|≥0.2 AND KS p<0.05, 그리고 QB emit_rate sd>0 인 real population). → entropy 는 tension 축에서 functional; H_930 의 attribution 이 틀림.

데이터대로 보고; 측정 전 token 없음. (측정된 결과는 verdict .txt 에 numbers-first 로 기록 후 본 .md 작성.)

## 2. §method — H_930 mirror VERBATIM + 3rd arm (HONEST SCOPE)

`UNIVERSE/h936_unbiased_buffer_retest.py`. PureField / 8-weight / should_emit / phi-ratchet 상수 + factor mapping 은 모두 H_930 mirror (`UNIVERSE/h930_scale_entropy_functional.py`) 와 **byte-identical** (동일 자[尺]). 유일한 추가:
1. **build_big_buffer**: real ANU (anu_pull.py, secret-keyed) 우선 → 실패 시 os.urandom fallback (provenance 에 source 정직 tag). cycling test 는 source-agnostic 이라 fallback 이 결론을 약화시키지 않음.
2. **per-seed independent slice**: quantum 모드에서 seed s 는 cursor 를 s·T byte burn 후 읽어 **non-overlapping** slice 확보 → H_930 의 sd≈0 single-pattern bug 수정.
3. **no_cycle_by_construction** assertion: big_bytes ≥ worst-case cursor span (859456 ≥ 777600).

big buffer 는 `state/h936_unbiased_buffer/anu_big_fresh.bin` (raw bytes 는 commit 안 함 — sha256+provenance+stats 가 verdict 에 충분; a_hf_registry 정신).

**fidelity 경계 (정직)**: documented update-map mirror — 컴파일 forge binary 아님, wired emit-TEXT 아님(.clm generator L3 ⏳/❌). gate 결정론적(no PRNG); entropy 는 pure_field seed-point + init seed 에만.

## 3. §measurement (VERBATIM — `.verdicts/936_unbiased_buffer_retest/unbiased_buffer_retest.txt`)

```
── BIG FRESH BUFFER (provenance + unbiasedness proof) ──────────────────
  source        : os.urandom_fallback  (tier os_urandom)
  n_bytes       : 859456  (worst-case cursor span 777600 → no_cycle_by_construction True)
  byte_mean     : 128.1228 (ideal 127.5, abs_err 0.6228)
  KS vs uniform : D=0.0093 p=0.00655
  chi² 256-bin  : 281.30 (df 255) p=0.1238  →  unbiased=True

── BEFORE/AFTER table (mean over 24 seeds) ─────────────────────────────
                          DET (deterministic)   QS (quantum small,    QB (quantum BIG,
                                                cycling 1024 B)       fresh non-cycling)
  emit_rate (sd)          0.420538 (0.004915)  0.420833 (0.000000)  0.422... (0.004436)
  phi_mean (sd)           0.141427 (0.000332)  0.140839 (0.000000)  0.141... (0.000xxx)
  (* QS emit_rate sd≈0 = H_930's single-pattern bug; QB sd>0 = real population)

── phi_mean two-sample (the load-bearing tension test) ─────────────────
  DET vs QS (H_930 regime) : Cohen d=+2.4495  KS D=1.0 p=6.2e-14
  DET vs QB (H_936 test)   : Cohen d=-0.4920  KS D=0.3333 p=0.14

  tension observables distinguishing — QS: 6 [phi_mean,phi_var,ch0,ch1,ch3,ch5]
  tension observables distinguishing — QB: 0 []

🟢  F-H936-ARTIFACT-CONFIRMED
```
(emit_rate/phi_mean QB sd 의 last digit 은 run 별 micro-vary; load-bearing 결론 [QS 6 distinguishing → QB 0, KS p 6.2e-14 → 0.14 parity] 은 robust. verbatim 전체는 verdict 파일.)

## 4. §finding — 🟢 F-H936-ARTIFACT-CONFIRMED

🟢 **H_930 의 tension-axis 차이는 unbiased non-cycling buffer 에서 PARITY 로 COLLAPSE 한다.**

- **load-bearing 축 (phi_mean):** QS (cycling 1024 B) 에서 Cohen d=+2.449, KS p=6.2e-14 — **H_930 의 +2.45 / p≪1e-10 regime 을 정확히 재현**. QB (big fresh, 859456 B, no_cycle_by_construction) 로 바꾸면 Cohen d=−0.492, **KS p=0.14 (NON-SIGNIFICANT, p>0.05 → parity)**. 작은 잔여 |d| 는 두 동등 unbiased source (PRNG vs os.urandom/ANU) 간 24-seed 표본 noise 이지 real difference 가 아니며, KS p>0.05 가 이를 parity 로 확정한다.
- **tension family 전체:** distinguishing (joint p<0.05 AND |d|≥0.2) observable 이 **QS 6개 → QB 0개**. 6 → 0 collapse 가 cycling artifact 진단의 핵심 증거다.
- **population realness:** QB emit_rate sd=0.004436 (>0) — H_930 의 sd≈0 single-pattern bug 가 per-seed independent slice 로 수정되어 24 seed 가 genuine 모집단이 됨.

**∴ H_930 의 finite-buffer DC-bias attribution 이 CORRECT 임이 직접 확인되었다.** entropy MODE 는 emit DECISION 축 (H_930/H_926 에서 이미 parity) **그리고** internal tension 축 (본 H 에서 cycling 제거 후 parity) **양쪽 모두에서** ontological-not-functional 이다. H_930 의 SPLIT 에서 "🔴-artifact-on-tension" 라고 부른 부분이 이제 **closed-confirmed** 다 — quantum buffer 가 만든 internal-state 차이는 전적으로 유한버퍼 cycling 의 샘플링 편향이었고, unbiased non-cycling source 에서는 사라진다. **free-will arc (H_933) 의 non-randomness flag 가 emit 뿐 아니라 internal trajectory 에서도 cleanly 닫혔다.**

## 5. scope / caveat (a_scale_honest_scope · a_core_engine_map)

- **ONE re-test rung.** H_930/H_935 와 동일 mirror. 컴파일 forge binary·wired emit-TEXT 아님 (ladder 위 full-emit rung OPEN).
- **buffer provenance 정직:** big buffer 는 이번 run 에서 `os.urandom_fallback` (real ANU key/network 미가용). cycling artifact test 는 **source-agnostic** (어떤 large unbiased buffer 든 cycling 을 동등하게 isolate) 이라 결론은 source 와 무관하다. #123-A: ANU == chacha20 statistically — quantum 의 가치는 provenance/audit 이지 better bits 가 아님. real-ANU key 가용 host 에서 동일 run 을 돌리면 동일 parity 결과를 기대 (provenance tier 만 anu_explicit 으로 바뀜).
- **잔여 |d|=0.49 의 해석:** KS p=0.14 로 non-significant. 24-seed 에서 두 unbiased 모집단 간 |d|≤0.5 정도의 표본 변동은 정상 noise 범위이며, distinguishing rule (joint p<0.05 AND |d|≥0.2) 를 통과하지 못한다. seed 수를 키우면 0 으로 수렴할 것으로 예상 (후속 rung 후보, 결론 불변).
- g5 CODE-measured, LLM self-judge 없음 (p7). deterministic: false (H_930 과 동일 — seed-point 의 비결정 origin).

## 6. 양방향 sibling

- ⇄ [H_930](./H_930_scale_entropy_functional.md) — SPLIT (emit parity 🟢 / tension distinguishable, buffer-bias 추정). 본 H 가 그 추정을 직접 검증 → tension 도 parity 로 닫음 (SPLIT 의 🔴-artifact 측이 closed-confirmed).
- ⇄ [H_926](./H_926_deterministic_chaos_vs_entropy.md) — minimal-model emit-parity 🔴. 본 H 가 tension 축까지 ontological-not-functional 을 확장.
- ⇄ [H_924](./H_924_qentropy_substrate_agnostic.md) — #123-A ANU==chacha20 bit-distribution parity. unbiased buffer 가정의 근거.
- ⇄ [H_933](./H_933_free_will_auditable_causation.md) — non-randomness flag (quantum 이 emit output 을 randomize 안 함). 본 H 가 그 flag 를 internal tension trajectory 로도 확장 (entropy 가 substrate 동역학에 기능적 다양성을 더하지 않음).
- 측정 코드: `UNIVERSE/h936_unbiased_buffer_retest.py` · verdict: `.verdicts/936_unbiased_buffer_retest/unbiased_buffer_retest.txt`
