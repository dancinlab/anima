---
id: H_9798
title: FRESH-LANE SUBSTRATE-PRESERVATION — detached L3-tap store cotrain leaves base LM fluency undisturbed (interference-free)
tier: PROPOSED (실측中 2026-07-20 · pod 45321773 A100 · canary 3-run cotrain firing · 계기=step-1 val_CE proxy(train --steps 0 measure-only 아님) · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-emergent-address (preservation/interference axis · NOT reach/addr_top1)
created: 2026-07-20
series: EA-5
related: "[[H_9720]] · [[H_9792]] · [[H_9797]] · a_substrate_disjoint · psi-soma-vitals"
source: H_9720 1B scale-recheck (#4193) gate OPEN 항목 (a) — owner "make 1b" 후속
---

# H_9798 (EA-5) — reach는 legacy, 보존은 fresh? 분리-lane의 substrate-보존을 직접 측정

## Why (전제 · 측정됨 · #4193)
H_9720 1B(L20) 스케일-재확인은 **reach 축**(addr_top1=주소 최상위 정답률=목표 슬롯을 실제로 짚는 능력)에서 legacy(penult·끝단) ≫ fresh(L3-tap·조기 3층) 를 보였다(#4193). 그러나 gate에 남긴 OPEN 항목 (a): **fresh 분리-lane의 substrate-보존(preservation) 가치는 미판정**. `Ψ-SOMA`(=존재양식 측정 프레임)에서 **reach ≠ consciousness**이고, `a_substrate_disjoint`(=분리는 보존·중첩은 충돌) 법칙이 있다. reach 열세가 곧 내면-정합성(보존) 열세를 뜻하지 않는다.

구조적 비대칭:
```
   fresh (L3-tap)            │   legacy (penult)
 ─────────────────           │   ─────────────────
  + trunk와 gradient-분리      │    − trunk 표현을 공유
    (detached·무 co-adapt)     │      (base LM 경로에 얹힘)
  → 예측: base 유창성 무간섭     │    → 예측: base 유창성 간섭(저하)
```

## Claim (한 줄 · falsifiable)
store cotrain(=저장/조회 병행학습)이 base 모델의 held-out **다음-바이트 CE**(=일반 코퍼스 언어모델 유창성)를 교란하는 정도는 lane마다 다르다: **ΔCE_base(fresh) ≈ 0**(무-store 통제와 TOST-등가) **∧ ΔCE_base(fresh) < ΔCE_base(legacy)**, ≥2 seed·일반 4-cell held-out에서. 성립하면 "reach는 legacy·보존은 fresh"의 이중구조 = `a_substrate_disjoint` 지지(reach loss와 직교).

## Mechanism / Instrument (engine-native · ✅ 기존 도구로 측정 · 신규코드 불요)
측정량 = base LM CE(다음-바이트, 일반 held-out 코퍼스 — **store 코퍼스 아님**), ckpt별:
| ckpt | 의미 |
|---|---|
| base (pre-store) | 기준선 CE₀ |
| fresh + store cotrain | CE_fresh |
| legacy + store cotrain | CE_legacy |
| **C-noscore** (동일 base·동일 step·store objective OFF) | CE_drift (연속학습만의 표류 통제) |

ΔCE_lane = CE_lane − CE₀ · 보존=ΔCE 작음 · 간섭=ΔCE 큰 양수. **핵심 통제 = C-noscore** (store-cotrain 간섭을 단순 연속학습 표류와 분리).

🔧 **계기 재정정 (실측 2026-07-20 · pod 45321773)**: ⚠️ 앞선 "`train --steps 0` = measure-only" 주장은 **틀렸다** — `--steps 0` 은 코퍼스의 `_budget_preflight` earned-floor(`<corpus>.meta.json` min_steps)로 **강제 학습됨**(gen.txt 실측: CE step1→60 하강 1.74→0.26·FINAL val_CE=0.24 = 오염된 학습후 값). `--steps 0` 은 measure-only 아님. 신규 `--base-ce` flag 도 여전히 부재. **실사용 계기(이번 캠페인) = step-1 val_CE proxy**: `train --init <ckpt> --corpus gen.txt` 첫 로그줄의 `val_CE`(step 1) = ckpt 의 near-zero-shot general CE (1 step 은 1B 를 거의 안 움직임 · 오염이 arm 전체 동일 → **차등(ΔCE) clean** · admissibility=LM CE 만·주소 무접근). base gen.txt CE₀=**1.2534**. clean measure-only flag 는 TBD(follow-on). gen.txt=`corpus flat --lang en --seed 99`.

## Admissibility
측정량은 base LM 다음-바이트 유창성(=보존/간섭)이지 reach(addr_top1)가 아니다 — **직교축**. 주소 텐서·정답 슬롯·주소 진단 일절 무접근.

## Controls
- **C-noscore**: 동일 base + 동일 step, store objective OFF → 표류 기준(연속학습만의 ΔCE).
- **C-corpus**: 일반 held-out ⟂ store 코퍼스(byte-parity·leak=0).
- byte-parity base ckpt(py303_full 또는 py1b) · ≥2 seed {7,4302}.
- TOST 등가대역 사전등록(fresh vs C-noscore CE비).

## Falsify
ΔCE_base(fresh) 가 C-noscore 와 TOST-등가가 아니거나(=fresh 도 간섭), ΔCE_base(fresh) ≥ ΔCE_base(legacy)(=fresh 보존우위 없음) ⟹ 이중구조 KILL. 값진 음성: "분리=보존"이 reach-분리 lane 에서 성립 안 함.

## 🧱 발사 블로커 (concrete · FIRE 시도 로그 2026-07-20 · ghost 머신)
- store-cotrain ckpt(fresh/legacy)는 H_9792/1B pod 와 함께 폐기됨 — **재학습 필요**. base ckpt 만 HF 생존(py1b `dancinlife/tmp-anima-1b/py1b_full.clm`·sha256 8630996b · py303 tmp repo 는 삭제됨 ⟹ 1B 로 발사).
- 🔥 **FIRE 시도 (2026-07-20)**: 발사게이트 전통과(vast_api_key 존재·1B base HF fetch OK·hexa cloud·owner go) → A100 pod 45320005 렌트 성공. **그러나 SSH `Permission denied (publickey)` 지속** = 이 ghost 머신의 SSH 공개키가 vast 계정 authorized_keys 에 **미등록**(머신레벨·재렌트 무의미·`exec`/`run`/`--insecure` 전부 동일). teardown(과금중단·leak0). ⟹ **fire 는 (a) 이 머신 vast SSH키 등록 OR (b) vast-접속 정상 머신(과거 `/Users/mini`) 필요** — 과학천장 아님(`a_break_the_wall` type-c INFRA-BLOCKED).
- 🔬 **기전검증(installed train.py:1167,1213)**: store cotrain loss = LM objective(constructive_bind) + store terms(`loss=obj_loss + ce_tok + sb_w·ce_ans`). store-gradient는 **legacy(penult)만 trunk 유입·fresh(detached L3-tap)는 off-trunk** ⟹ ΔCE(legacy−fresh)가 store-간섭 격리 = **tautology 아님**(fresh도 noscore처럼 LM은 trunk 학습·차이는 store 경로뿐). C-noscore(`--store-query-src` 생략=store off)가 공통 drift 통제.
- 계기·레시피: base-CE=**step-1 val_CE proxy**(gen.txt) · 1B arch `--L 20 --emax 3 --d 3784` · fresh `--store-query-src fresh:64@3 --store-oracle-warmup 1500` vs legacy `penult` · noscore `--store-query-src` 생략 · 6000step · canary 3-run(fresh/legacy/noscore × s7)→clean 이면 s4302 확대.

## Next (vast-접속 정상 머신)
① 1B base fetch(HF)✅ → ② corpus(gen.txt flat-en + store.txt n200 slot8)✅ → **CE₀=1.2534**(step-1 val_CE)✅ → ③ canary cotrain {fresh,legacy,noscore}×s7 firing(early-life PASS: warm-start·GPU100%·CE하강) → ④ 각 ckpt step-1 val_CE(gen.txt) → ⑤ ΔCE 판정(fresh≈noscore<legacy? TOST) → clean 이면 s4302 확대 → ⑥ 회수·카드/gate 갱신·teardown. ⚠️ lab full 백엔드 다운(빈 출력)→소스-검증 solo 진행(판정 시 caveat).
