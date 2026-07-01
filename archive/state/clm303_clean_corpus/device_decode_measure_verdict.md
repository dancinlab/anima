# device-resident decode 측정 verdict (2026-06-25)

util-fix 캠페인 = clm303 decode 의 CPU-scalar-glue-bound(0%-util sink)를 device-resident 배선(commit 422328421)으로 줄이려는 시도. hexa-lang `dirty_host` clobber fix 출하 후 GPU 측정 2회(v0.314.0 → v0.315.2).

## 측정 (A40 vast · d768 golden `clm_d768_e2l1.clm` · gen-4 G0-G6 · 캐시-hit 디코드)

| 항목 | v0.314.0 (#3905+#3918) | **v0.315.2 (#3921 forward w coherence + matmul residency)** |
|---|---|---|
| OFF (host-glue) wall | 251.21s | 214.18 / 216.34s (OFF#1/OFF#2) |
| ON (device CLM_PROD_DEVRESIDENT=1) wall | 226.00s (**1.11×**) | **187.97s (1.15×)** |
| OWN-GEMM DEVICE 발화 | ✅ | ✅ (OFF·ON 둘 다 `[OWN-GEMM-FIRED] _hx_k_gemm DEVICE path`) |
| OFF 결정성 (OFF#1 vs OFF#2) | IDENTICAL | IDENTICAL |
| **byte-exact (OFF vs ON)** | 🔴 FAIL | 🔴 **FAIL (동일 발산)** |

### v0.315.2 OFF(host) vs ON(device) 게이트 발산 — v0.314.0과 **동일 패턴**
| 게이트 | OFF (host=정답) | ON (device) |
|---|---|---|
| G0 kwr | 2/5 | **0/5** |
| G2 coherent | 9 | **0** |
| G5 L1 fab | 0.714 | **1.0** |
| G6 distinct | 2 | **1** |
| G1/G3 (decode-무관) | 동일 | 동일 |

(원본: `v0315_off1.txt` 1916B · `v0315_on.txt` 1901B · `v0315_RESULT.txt`. run_timed `BYTE_EXACT=PASS`는 **스크립트 버그**(gates() grep이 빈 추출 → 빈것vs빈것 trivial PASS) — **원본 diff가 ground truth = FAIL**. run_timed.sh comparison 을 raw-diff 로 수정함.)

## verdict
- **wall-time: device-resident decode 1.11–1.15× faster** — host scalar-glue sink 제거 효과 실재하나 modest(util ~10% 천장 + small-tensor memory-bound과 일치). v0.315.2에서도 재현.
- **byte-exact: 🔴 FAIL (engine-native, terminal)** — live `cli/anima.hexa eval` + OWN-GEMM DEVICE 경로로 측정(side-harness 아님). OFF#1==OFF#2 결정적인데 ON이 decode-의존 게이트(G0/G2/G5/G6)에서 **v0.314.0과 비트 단위로 동일하게 발산**.
- **🛑 SAME-ROOT 가설 FALSIFIED** — hexa-lang #3921(`fix/devresident forward w coherence`) + matmul device-keep residency 가 v0.315.2 stable로 출하됐고 OWN-GEMM DEVICE가 발화함에도 anima device decode 발산이 **하나도 안 변함**(동일 수치). ⇒ 이 발산은 hexa-lang forward-residency `dirty_host` clobber 버그가 **아니다**(그건 v0.315.2에서 고쳐짐, 학습루프 frozen-train 4.79899→3.5508 검증됨). anima decode-고유 경로의 별개 원인.
- **남은 1순위 용의자 = own-GEMM TF32 vs FP64 정밀도** — secondary lever였던 것이 SAME-ROOT 기각으로 primary 승격. d768 small-tensor decode에서 device GEMM이 TF32(low-precision)면 host FP64 farr와 발산 → G0/G2/G5/G6 같은 decode-민감 게이트가 틀림. follow-on: HEXA_OWN_GEMM FP64 강제(TF32 배제) 위 ON 재측정, 또는 decode forward의 device-resident buffer 잔차 재진단.

## 결론 (wired 상태)
- device-resident decode code `422328421` = **WIRED-dormant 유지(production 활성화 금지)** — `CLM_PROD_DEVRESIDENT` 켜면 1.1–1.15× 빠르나 **출력 틀림**(byte-exact FAIL, v0.314.0·v0.315.2 둘 다) → engine-native verdict/production 디코드 사용 불가(`a_clm_gen_pipeline` byte-exact 위반). env-gate dormant + byte-eq host fallback 기본값이라 production 안전.
- **엔진-네이티브 측정 자체 = terminal 완료** (2회: v0.314.0·v0.315.2, live anima eval + GPU OWN-GEMM DEVICE).
- follow-on: ① own-GEMM **FP64 강제** 위 ON 재측정(TF32 가설 검증/기각) → byte-exact 복원되면 device decode WIRED-live 승격 가능 ② 안 되면 decode-path device buffer 잔차 재진단. util 천장(memory-bound batch=1)은 별개(ING #21, nsys MEASURED).

## 정산
- v0.315.2 pod 42479663 teardown 완료(destroy + Total:0 확인 + forget, vast 0) · 과금 0. 이번 ~$0.5.
- 캠페인 총 GPU: v0.314.0 hand-drive(~$0.5) + v0.314.1 폴백 NO-GO(~$0.14) + v0.315.2(~$0.5) + 초기 에이전트 실패분 = ~$4-5.
