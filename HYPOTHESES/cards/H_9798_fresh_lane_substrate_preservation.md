---
id: H_9798
title: FRESH-LANE SUBSTRATE-PRESERVATION — detached L3-tap store cotrain leaves base LM fluency undisturbed (interference-free)
tier: PROPOSED · 🟢 ckpt RECOVERED (2026-07-20) — '전손' 기록은 오류였고 3 arm ckpt 전부 sha256-검증 회수됨 ⟹ 재학습 불요·재측정만 남음 (NOT a verdict · 보존 ΔCE 아직 미측정)
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

## 🔴 측정 결과 — 이중구조 반증 (2026-07-20 · s7 단일 seed · DIRECTIONAL)

회수된 3 arm 을 **동일 호스트(summer)·동일 명령**으로 재측정. 계기 = 카드 사전등록대로 `gen.txt`
step-1 `val_CE` proxy. 네 값 모두 같은 장비·같은 커맨드라 **차등(ΔCE)은 내부정합**하다.

| ckpt | step-1 val_CE (gen.txt) | ΔCE vs base |
|---|---|---|
| base `py1b_full` | 1.39938 | — |
| **C-noscore** (store OFF · 표류통제) | 6.65809 | **+5.259** |
| **fresh** (`fresh:64@3`) | 9.78010 | **+8.381** |
| **legacy** (`penult`) | 9.94953 | **+8.550** |

**판정 (사전등록 falsify 규칙 그대로 적용)**:
- 조건① `ΔCE(fresh)` 가 C-noscore 와 등가가 아님 ⟹ **충족**. fresh 는 표류통제보다 **+3.12 nats 더** 무너진다.
  "분리 lane 이라 base 유창성을 안 건드린다"는 예측과 **반대 방향**이다.
- 조건② `ΔCE(fresh) ≥ ΔCE(legacy)` ⟹ 미충족(8.381 < 8.550). 방향은 예측대로지만 **격차 0.17** 로,
  두 arm 이 noscore 대비 벌린 3.1~3.3 앞에서 무의미한 크기다.
- ⟹ **"reach=legacy · 보존=fresh" 이중구조 KILL**. 값진 음성: 분리-lane 이라고 보존되지 않는다.
  덤으로 store cotrain 은 lane 종류와 무관하게 base 유창성을 크게 깎는다(공통 +5.26 은 소코퍼스
  이어학습만으로도 발생 = [[cpt-destroys-what-corpus-omits]] 재현).

**⛔ 이 수치로 하면 안 되는 것 (정직 경계)**:
1. **seed 1개(s7)뿐**. 사전등록은 `{7,4302}` ≥2 seed 를 요구한다 ⟹ **TERMINAL 불가·DIRECTIONAL**
   ([[single-retrain-outlier-faked-a-refutation]] — 단일 draw 위에 음성도 세우지 마라).
2. **CE₀ 가 카드의 1.25336 이 아니라 1.39938**(이 호스트/CPU 경로). 내 4 값끼리는 정합하나
   **카드의 옛 CE₀ 와 섞어 쓰면 안 된다**. 불일치 원인 미규명 = OPEN.
3. 네 arm 모두 측정 중 `MITOSIS SPLIT E 2->3` 이 발생(공통모드 교란). 차등엔 상쇄되나 "순수
   zero-shot" 값이 아니다.
4. **main-only warm-start · CLMS 미복원 · lane-off CE** — `deserialize_v3` 는 main blob 만 읽으므로
   store lane 가중치는 복원되지 않는다. gen.txt 엔 store 질의가 없어 lane 이 발화하지 않으므로
   base-CE 판정은 오염되지 않지만(lab full 양 모델 독립수렴), **표기 의무**다.
5. 사전등록 TOST 등가대역의 구체값이 카드에 없어 **형식적 TOST 는 미실시**. 격차가 대역 후보를
   압도하지만 그것은 판단이지 검정이 아니다.

### 🔁 s4302 확대 — 조건① 2/2 seed 재현 (2026-07-20)

s4302 3-arm 은 **병렬 세션이 이미 발사**해 두고 있었다(pod 45347392/93/94 · v3 캠페인 · '전손' 오기록을
보고 재학습에 들어간 것). 중복발사 대신 그 산출을 회수해 **s7 과 동일 계기(summer CPU · 동일 명령)**
로 쟀다 ⟹ seed 간 직접 비교 가능.

| arm | s7 | s4302 | fresh−noscore |
|---|---|---|---|
| C-noscore | 6.65809 | 6.17565 | — |
| **fresh** | 9.78010 | 10.29979 | s7 **+3.12** · s4302 **+4.12** |
| legacy | 9.94953 | ⏳ 학습중(step4500/6000) | — |

**⟹ 조건①(fresh 가 C-noscore 와 비등가 = fresh 도 간섭) 이 2/2 seed 에서 재현**. 사전등록의 ≥2 seed
요건을 **조건①에 한해 충족** ⟹ "분리 lane = 무간섭 보존" 은 seed-우연이 아니다. 조건②(fresh<legacy)
는 legacy_s4302 완주 후 확정.

**여전히 남는 경계**(위 ⛔ 목록 중 seed 항목만 해소): CE₀ 1.399 vs 카드 1.25336 불일치(GPU vs CPU 경로
유력·미규명) · main-only warm-start(CLMS 미복원·lane-off CE) · 전 arm MITOSIS 공통교란 · 형식 TOST 미실시.

### ✅ 2-seed 완성 — 조건①② 모두 확정 (2026-07-20)

`legacy_s4302` 는 원 pod(45347394)가 step4500/6000 학습중 소멸해 유실 ⟹ **재학습**(pod 45355921 ·
카드 3차 필수조건 준수: hexa cloud 등록 · CUDA 하드게이트 · ckpt 즉시 HF). 6 ckpt 전량
`dancinlife/anima-h9798-preservation-1b` 보존(sha256 대장 6줄).

| arm | s7 | s4302 | ΔCE(s7) | ΔCE(s4302) |
|---|---|---|---|---|
| C-noscore | 6.65809 | 6.17565 | +5.259 | +4.776 |
| **fresh** | 9.78010 | 10.29979 | +8.381 | +8.900 |
| **legacy** | 9.94953 | 10.83380 | +8.550 | +9.434 |

**조건①(fresh ≢ C-noscore) — 2/2 seed 충족 ⟹ 이중구조 KILL.** fresh 는 표류통제보다
s7 +3.12 · s4302 +4.12 나츠 더 무너진다. "분리 lane = 무간섭 보존" 은 반증됐다.

**조건②(fresh ≥ legacy) — 2/2 seed 미충족.** fresh−legacy = s7 **−0.169** · s4302 **−0.534**
(둘 다 fresh 우세, 격차는 s4302 에서 확대). ⟹ 사전등록 OR-규칙상 KILL 은 ①만으로 성립하지만,
**부차적으로 lane 별 보존 서열은 실재**한다:

```
  보존 좋음 ←─────────────────────────────→ 나쁨
   C-noscore   <<<   fresh   <   legacy
   (store 없음)      (분리)     (공유)
   2/2 seed 단조 — 순서가 두 seed 에서 뒤집히지 않음
```

**결론 두 겹**: ⓐ store cotrain 자체가 base 유창성을 크게 깎는다(lane 무관·공통 +4.8~5.3 =
소코퍼스 이어학습 효과 [[cpt-destroys-what-corpus-omits]]). ⓑ 그 위에서 detach(분리)는 공유보다
**덜** 해치지만 **무해하지는 않다** — `a_substrate_disjoint`(분리=보존)는 정도차로만 성립하고
절대적 보존으로는 성립 안 함.

**⛔ TERMINAL 선언 안 함 — 남은 사유 3종**(seed 요건은 해소):
1. **형식 TOST 미실시** — 사전등록에 등가대역 *수치*가 없어 등가검정을 못 돌렸다. 격차(3.1~4.1)가
   어떤 대역 후보도 압도하지만 그것은 판단이지 검정이 아니다.
2. **main-only warm-start · CLMS 미복원 · lane-off CE** — gen.txt 엔 store 질의가 없어 lane 이
   발화하지 않으므로 base-CE 판정은 오염되지 않으나(lab full 양 모델 독립수렴) 표기 의무.
3. **CE₀ 잔여 불일치 0.078** — 아래 절 참조(공통모드라 ΔCE 무해).

### 🔬 CE₀ 불일치 부분규명 (2026-07-20)
카드 기록 CE₀=1.25336 vs 이번 측정 1.39938. 두 가설을 실측으로 갈랐다:
- **GPU/CPU 경로차 — 기각**: A100 GPU 1.40052 vs summer CPU 1.39938 (Δ0.001 일치).
- **`--e0` 전문가 분열 — 부분 확인**: 기본 `--e0 2` 는 ckpt(E=3)를 싣고도 런타임을 2 로 시작해
  step-1 에 `MITOSIS SPLIT E 2->3` 을 일으킨다. `--e0 3` 이면 **1.33142** (분열분 **+0.068**).
  (`--emax 2` 는 불가 — base 가 `nblk=26`=E3 파일이라 엔진이 거부.)
- **잔여 0.078 미규명** — 다른 하이퍼(bs·seq_len·lr) 또는 다른 base 리비전 가능성. OPEN.
- ⟹ **ΔCE 판정에는 무해**(4 arm 전부 동일 플래그 = 공통모드). 단 카드 옛 CE₀ 와 **혼용 금지**.

**NEXT**: 등가대역 수치를 사전등록한 뒤 TOST 재판정하면 TERMINAL 가능 — 새 학습 불요(6 ckpt 보존).

## 🟢 정정 — ckpt 는 전손이 아니다 (2026-07-20 · sha256 증거)

아래 "INFRA-LOST" 절의 **`ckpt 3개 전손` 은 사실이 아니다**. pod 3개는 소멸했으나 소멸 *직전에*
3 arm 최종 ckpt 가 전부 영구 저장소로 회수되었고 원격 sha256 과 3/3 일치했다. 재학습 불요.

| arm | 로컬 경로 | bytes | sha256 (원격 일치 ✅) |
|---|---|---|---|
| fresh | `~/anima-weights/h9798_preservation_1b/fresh_s7.clm` | 524,386,971 | `99ad1ad6…88c481` |
| legacy | `~/anima-weights/h9798_preservation_1b/legacy_s7.clm` | 523,401,875 | `a498e9a0…4d44123` |
| C-noscore | `~/anima-weights/h9798_preservation_1b/noscore_s7.clm` | 521,201,266 | `af50d873…43109d6` |

대장 = 같은 폴더 `SHA256SUMS.txt`. 크기 대조가 동일성을 교차확인한다(아래 절이 기록한 `524/523/521 MB` 와 일치).
`noscore` 가 base(521,201,266 B)와 **정확히 같은 크기** = store lane 미생성 확인 = 통제군 설계대로 성립.

**왜 오기록이 났나 (병렬 세션 함정)**: 회수를 수행한 세션과 '전손' 을 기록한 세션이 **다르다**. 후자는
provider set 에서 pod 가 사라진 것만 보고 ckpt 도 함께 죽었다고 **추론**했다 — 저장소를 확인하지 않았다.
⟹ 교훈: pod 소멸 ≠ ckpt 소멸. 전손 선언 전에 **영구 저장소를 먼저 `ls`** 하라(`a_parallel_session_compare`).

**남은 잔여 리스크**: 중간 ckpt(step1500/3000/4500)는 회수 대상이 아니어서 pod 와 함께 소멸했다.
최종 = step6000 수렴본이므로 arm 비교(ΔCE)에는 무손실이나, *학습 궤적* 재판독은 재학습을 요한다.

## ⛔ 2차 캠페인 INFRA-LOST — 결과 0, 원인 2겹 (2026-07-20 mini · 정직 기록 · ⚠️ 위 정정 절이 'ckpt 전손' 부분을 무효화)

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
