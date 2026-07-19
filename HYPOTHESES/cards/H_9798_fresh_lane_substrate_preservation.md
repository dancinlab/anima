---
id: H_9798
title: FRESH-LANE SUBSTRATE-PRESERVATION — detached L3-tap store cotrain leaves base LM fluency undisturbed (interference-free)
tier: PROPOSED · ⛔ 2차 캠페인 INFRA-LOST (2026-07-20) — 3 arm 6000step 학습 전부 완주했으나 측정 前 pod 3개 소멸·ckpt 전손 ⟹ 보존 ΔCE 여전히 미측정 (NOT a verdict · 과학천장 아님)
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
  🚨 **OFF 스위치 정정 (코드확인 2026-07-20 · installed train.py:1765,1996)**: store lane 은 **`--store-bridge <store.txt>` 가 있을 때만** 켜진다(`sb_cell = StoreBindCell(...) if a.store_bridge or a.freeze_trunk` → `_sb = get_store_batch() if sb_cell is not None else None` → loss 의 store 항은 `if sb is not None:` 안). ⟹ noscore = **`--store-bridge` 생략**. ⚠️ 앞서 카드가 적었던 "`--store-query-src` 생략 = store OFF" 는 **틀렸다** — 이 flag 의 **default 가 `penult`**(train.py:1369)이라 생략하면 오히려 **legacy arm 과 동일**해져 통제군이 실험군으로 붕괴한다(발사 전 포착).
- **C-corpus**: 일반 held-out ⟂ store 코퍼스(byte-parity·leak=0).
- byte-parity base ckpt(py303_full 또는 py1b) · ≥2 seed {7,4302}.
- TOST 등가대역 사전등록(fresh vs C-noscore CE비).

## Falsify
ΔCE_base(fresh) 가 C-noscore 와 TOST-등가가 아니거나(=fresh 도 간섭), ΔCE_base(fresh) ≥ ΔCE_base(legacy)(=fresh 보존우위 없음) ⟹ 이중구조 KILL. 값진 음성: "분리=보존"이 reach-분리 lane 에서 성립 안 함.

## 🧱 발사 블로커 (concrete · FIRE 시도 로그 2026-07-20 · ghost 머신)
- store-cotrain ckpt(fresh/legacy)는 H_9792/1B pod 와 함께 폐기됨 — **재학습 필요**. base ckpt 만 HF 생존(py1b `dancinlife/tmp-anima-1b/py1b_full.clm`·sha256 8630996b · py303 tmp repo 는 삭제됨 ⟹ 1B 로 발사).
- 🔥 **FIRE 시도 (2026-07-20)**: 발사게이트 전통과(vast_api_key 존재·1B base HF fetch OK·hexa cloud·owner go) → A100 pod 45320005 렌트 성공. **그러나 SSH `Permission denied (publickey)` 지속** = 이 ghost 머신의 SSH 공개키가 vast 계정 authorized_keys 에 **미등록**(머신레벨·재렌트 무의미·`exec`/`run`/`--insecure` 전부 동일). teardown(과금중단·leak0). ⟹ **fire 는 (a) 이 머신 vast SSH키 등록 OR (b) vast-접속 정상 머신(과거 `/Users/mini`) 필요** — 과학천장 아님(`a_break_the_wall` type-c INFRA-BLOCKED).
- 🔬 **기전검증(installed train.py:1167,1213)**: store cotrain loss = LM objective(constructive_bind) + store terms(`loss=obj_loss + ce_tok + sb_w·ce_ans`). store-gradient는 **legacy(penult)만 trunk 유입·fresh(detached L3-tap)는 off-trunk** ⟹ ΔCE(legacy−fresh)가 store-간섭 격리 = **tautology 아님**(fresh도 noscore처럼 LM은 trunk 학습·차이는 store 경로뿐). C-noscore(**`--store-bridge` 생략**=store lane 미생성 · 위 Controls 정정 참조)가 공통 drift 통제.
- 계기·레시피 **(2026-07-20 mini 재발사서 실측 확정)**: base-CE=**step-1 val_CE proxy**(gen.txt) · 1B arch `--L 20 --emax 3 --d 3784` · 6000step · `--ckpt-every 1500 --out <arm>.clm`(중도사망 복구지점). 세 arm 은 **`--corpus store.txt` 공통**, 차이는 store 경로뿐:
  | arm | flags |
  |---|---|
  | fresh | `--store-bridge store.txt --store-query-src fresh:64@3 --store-oracle-warmup 1500` |
  | legacy | `--store-bridge store.txt --store-query-src penult --store-oracle-warmup 1500` |
  | **C-noscore** | **`--store-bridge` 생략** (store lane 미생성 = LM-only 표류) |
  gen.txt 는 **어느 arm 도 학습하지 않는다** ⟹ held-out 자격 유지(측정 admissible). corpus: `gen.txt=corpus flat --lang en --seed 99`(798,220 B) · `store.txt=corpus storebind --n-blocks 200 --store-slots 8 --seed 7 --lang en`(leak0: `C0-a 0-shot ✅ held-out entities appear 0x`).
- ✅ **CE₀ 독립 재현 (계기 검증)**: 별 머신·별 pod(mini→vast 45328766 A100-40GB)서 base gen.txt step-1 `val_CE=1.25336` — ghost 측정 **1.2534 와 일치**. 기준점이 머신을 건너 재현되므로 ΔCE 판정의 기준선 성립.
- 🕳️ **인프라 함정 (발사 前 포착)**: `pip install "anima-python[train]"` 기본 torch=**2.12.1+cu130** vs vast pod 드라이버 **12080(CUDA 12.8)** → `torch.cuda.is_available()==False` 로 **예외 없이 CPU 폴백**(1B CPU 학습=사실상 무한·GPU 요금만 소모). 대응 = `pip install --force-reinstall --index-url https://download.pytorch.org/whl/cu128 "torch<2.13"`(→2.11.0+cu128 CUDA True) + bootstrap 에 **CUDA boolean 하드게이트**(False 면 학습 발사 자체 차단).

## Next (vast-접속 정상 머신)
① 1B base fetch(HF)✅ → ② corpus(gen.txt flat-en + store.txt n200 slot8)✅ → **CE₀=1.2534**(step-1 val_CE)✅ → ③ canary cotrain {fresh,legacy,noscore}×s7 firing(early-life PASS: warm-start·GPU100%·CE하강) → ④ 각 ckpt step-1 val_CE(gen.txt) → ⑤ ΔCE 판정(fresh≈noscore<legacy? TOST) → clean 이면 s4302 확대 → ⑥ 회수·카드/gate 갱신·teardown. ⚠️ lab full 백엔드 다운(빈 출력)→소스-검증 solo 진행(판정 시 caveat).

## ⛔ 2차 캠페인 INFRA-LOST — 결과 0, 원인 2겹 (2026-07-20 mini · 정직 기록)

3 arm(fresh·legacy·noscore) × 1B × 6000step **학습은 전부 정상 완주**(각 `step 6000` + FINAL 집계 + ckpt 524/523/521 MB).
그러나 base-CE 측정 前에 **pod 3개(45328766·45331827·45331828)가 동시 소멸**(`GHOST — absent from
authoritative provider set`) ⟹ **ckpt 3개 전손 · 보존 ΔCE 미도출**.

**원인 ① 도구 오사용 (재발방지 핵심)**: 학습을 `hexa cloud fire` 가 아니라 **raw `ssh … nohup anima-py train &`**
로 띄웠다 ⟹ `./pods.json` 에 **PENDING job 행이 생기지 않음** ⟹ `cloud idle-reap`("활성 job 없는 과금 pod")
이 **GPU 100% 로 학습 중인 pod 를 유휴로 판정**. ⚠️ 앞 세션이 세운 방어(mini 레지스트리 등록)는
`cloud reap`(ORPHAN=레지스트리 멤버십) 용이라 **`idle-reap`(=job 존재) 에는 무력** — 두 게이트는 별개다.

**원인 ② 치명상 (`a_fire_recover_complete` 위반)**: fresh 21:17 · legacy 21:31 완주 시점에 ckpt 를
**영구 저장소로 빼지 않고 측정으로 직행**. 백업만 했으면 pod 사망은 *재학습* 이 아니라 *재측정* 으로 끝났다.

**❗판정에 쓰면 안 되는 수치**: 학습런의 `FINAL val_CE(pooled)` = fresh 0.8113 / legacy 0.9065 는
**store 코퍼스 held-out** 값이지 `gen.txt`(일반 held-out) 가 아니다 — **보존 지표가 아니며 판정 근거 금지**
(noscore 는 그마저 미수집). 그럴듯하지만 다른 양이다.

**참고(판정 아님·reach 축)**: 최종 store 지표 fresh `addr_acc 1.0 / store_acc 1.0` vs legacy `0.75 / 0.875`.
보존축과 직교하므로 이번 claim 에 쓰지 않는다.

### 3차 발사 필수조건 (이 실패가 특정해준 것)
1. 학습은 **`hexa cloud fire <host> --port N -- <argv>`** 로 띄워 PENDING job 등록 (idle-reap 회피).
2. ckpt 가 생기는 즉시(중간 저장 `--ckpt-every` 포함) **HF 등 영구 저장소 업로드** — pod 사망을 재측정으로 강등.
3. 백업 완료 **후에** 측정(`--init <ckpt>` 은 학습과 **동일 구조 flag** 필수 — 엔진이 round-trip
   byte-identical 을 강제해 불일치 시 거부한다: 조용한 오독 방지).

### 재사용 가능한 생존 자산 (3차는 재설계 0)
CE₀=**1.25336**(독립 재현) · corpus 레시피(`gen.txt` flat-en s99 798,220 B / `store.txt` storebind n200 slot8 s7, leak0) ·
arm flag 표(위 Controls 정정) · FROZEN 판정규칙 · bootstrap(CUDA boolean 하드게이트 = cu130↔드라이버12.8 조용한 CPU 폴백 차단).
