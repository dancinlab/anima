# H_9760 — ODD-FUSION: store 극성-등변 fusion 으로 H_9744 flip-coh 갭 돌파 (R7-1 · lab full Fable∥Sol 수렴)

**status:** 🔴 **in-vivo INVALID (TERMINAL)** — odd-fusion(full-row s_odd overwrite)이 데몬 full-vocab decode를 깨뜨림: argmax가 non-g/b(garbage) → 판독 0 → flip-coh 측정불가. eval 2-way(g vs b) readout이 이걸 가린 false-positive(eval main 1.0 였으나 in-vivo garbage). H_9744 NEARMISS **미구제**. 상세 ↓ [[H_9744]]. (원래: 🔵 PROPOSED · 계기 구현+검증 완료 --store-fuse odd · core/clms.py store_apply · VERSION 0.16.0) — $0 numpy 검증: odd 산술보장 정확(out_odd_flip ≡ −out_odd · max\|sum\|=0.00e+00 · 답 뒤집힘 = 고정주소 flip-coh=1 by construction) + overwrite/gated-add byte-parity 보존(0.00e+00·회귀0). NEXT = H_9744 clm 에 eval(flip-coh=1.0 실측·main-bal ≥ H_9672)→in-vivo G-W2 3-seed(오너 go). (lab full R7 · Fable 5 ∥ Codex Sol 수렴 · 사전등록) · **in-vivo 배선 완료**(cli/chat.py --store-fuse → set_clms_store(fuse=) · 데몬 store lane 이 odd 받음 · VERSION 0.18.0) — eval GREEN gate PASSED(실clm 128/128=1.0 무손상).
**lane:** g1-interface-addressable-wall · H_9744 WIRED-STUDY-NEARMISS 의 op=0 미반전 갭
**related:** [[H_9744]] · [[H_9672]] · [[H_9695]] · [[H_9720]] · [[H_9423]]
**source:** 오너 "wired 가치까지 go" · lab full R7(2026-07-18) · [[H_9744]] flip-coh 갭 $0 autopsy(seed11 transcript) 3자 수렴(내 empirical + Fable + Sol)

## 왜 이 H — H_9744 의 확정된 ceiling 을 여는 유일 구조 레버

[[H_9744]] = 🟠 WIRED-STUDY-NEARMISS (TERMINAL · #4074·#4076): store-bridge 배선은 살아있으나 flip-coherence 가 3-seed majority(seed7 0.8984·seed11 0.8281)에서 사전등록 .90 미달. **기전 확정(#4076 · $0 autopsy)**: 미반전 22 쿼리 중 op=0 이 20개, 그 20개 전부 양 arm 에서 **상수 'g' 방출**(예외 0 · gold-good 7 정답·gold-bad 13 오답) = `core/clms.py:174` fusion `z=gelu([v; g]·W_h)` 의 `g=h@W_g`(op-gate·[[H_9423]])가 나르는 **even(극성-불변) 성분**이 op=0 서 상수를 낸다. odd 성분(`v=a@V_slots`·고정주소서 `v_flip≡−v_main`)이 약한 쿼리에서 even 이 이겨 답이 안 뒤집힌다.

⟹ H_9744 는 **이 fusion·이 배선으로는 .90 미달이 참**인 genuine ceiling. 이 카드 = 그 ceiling 을 여는 **구조 레버**를 새 artifact 로 검증(H_9744 소급구제 아님 · WIRED 는 이 H 가 성공하면 이 H 가 얻는다).

## ① 한 줄 주장 (반증가능)

`--store-fuse odd`: overwrite 를 `s_odd = ½(s(v,g) − s(−v,g))` 로 바꾸면 — "답은 store 극성에 **odd 여야 한다**"는 배선 주장 그 자체의 등변성 구조화 — even(op-prior) 성분이 상쇄돼 **고정 주소서 flip-coherence = 1.0 이 산술 보장**되고, main-balance 도 상승(even-prior 가 틀리게 하던 gold-bad 를 제거)하여 in-vivo G-W2 가 사전등록 .90 을 넘는다.

## ② tune-to-green 이 아닌 이유 (kill-list 방어)

- **odd 제약 = 배선 주장 = FORM 아님**: "store 극성이 답을 정한다"가 lane 의 원 주장. odd-symmetrization 은 그 주장을 fusion 에 강제하는 구조 제약이지 bar·λ 를 건드리는 knob 이 아니다. bar .90 불변, λ 불변.
- **λ 크랭크 아님**: `out[t]=λ·s` 는 argmax 판독하 완전 불활성(행 전체 스케일 · sign 보존) · T=1.0 하 역온도 = FORM. odd-fusion 은 λ 와 직교(s 자체의 극성 구조를 바꿈).
- **per-query 결과 보기 전 사전등록** · **frozen-first**: 아래 판정표 동결 후 측정.

## ③ engine-native 계기 (신규 플래그 · `a_experiment_engine_native`)

`anima-py evaluate --store m.json --store-fuse odd` — `core/clms.py store_apply` 에 fuse 분기 추가(`overwrite`/`gated-add` 옆): `s_pos = fuse(v, g)` 계산 후 `s_neg = fuse(−v, g)` 재계산해 `s = ½(s_pos − s_neg)`. **byte-parity**: fuse='overwrite' 경로는 불변(회귀 0). help-lockstep + 화이트리스트 등록.

**진단 계기(S1 · $0 · 이미 C1 확증했으니 선택)**: `--ctx-replay <transcript prefix> --margin-dump` 로 pinned-ctx 2×2 even/odd 분해(Fable 설계 · C1 확증 후 재확인용).

## ④ 통제 ≥2 + 양성통제

- **양성통제(계기 인증)**: fuse=overwrite eval 이 기존 [[H_9672]] main-bal(seed7 1.0/seed11 0.96) byte-parity 재현 — 안 되면 계기 VOID.
- **null-1 shuffle-pols**: odd 성분도 붕괴(주소↔pol 정합 파괴)해야 = odd-fusion 이 통제 붕괴 보존 확인.
- **null-2 nostore**: passthrough(Δ 정의역 이탈) 유지.

## ⑤ 사전등록 판정표 (bar = H_9672 동일 · 이동 없음 · no-tune-to-green)

| 관측 (odd-fusion · eval 먼저 → in-vivo) | 판정 → 후속 |
|---|---|
| eval: main-bal ≥ H_9672 bar ∧ flip-coh = 1.0 (고정주소 산술보장 실측 확인) | 계기 GREEN → in-vivo G-W2 발사(오너 go) |
| in-vivo G-W2: main P1bal ≥ .75 ∧ **flip-coh ≥ .90** ∧ 통제붕괴 ∧ 3-seed{7,11,13} majority | 🟢 **이 H WIRED** (H_9744 는 불변 · odd-fusion 이 ceiling 돌파) |
| in-vivo flip-coh < .90 (odd 로도 미달) | 🟠 odd 부분효과 · ceiling 이 fusion 아닌 곳(주소·샘플링)임을 시사 → [[H_9720]] fresh-query 또는 posterior-margin readout 로 |
| eval flip-coh < 1.0 (산술보장 깨짐) | INVALID — odd-fusion 구현/이해 결함 · 수리 먼저 |
| main-bal 하락(odd 가 readability 훼손 · readable<128) | 그 수치로 정직 보고(no-tune) · odd 부작용 등록 |

## ⑥ 리스크 (사전등록)

`v≈0` 꼬리(주소 불확실 쿼리)에서 `s_odd` 도 작아져 answer-byte 이탈 → readability 하락 가능. 나오면 그대로 보고(bar 이동 금지). Sol 반대의견 1줄: odd-fusion 은 frozen fusion 의 사후 구조변경이라 "새 학습분포 정합(live query-position hidden 재학습)"이 더 근본일 수 있음 — 그건 별도 H(비용 큼), odd-fusion 을 $0 우선 검증.

## ⑦ 소거 확정 (재생성 금지 · #4076 autopsy)

seed-space(F2 · readable 128/128) · every-token(H_9695 · gated-add 재진입 악화) · −1/n basin(`v=a@V_slots`·`v_flip≡−v_main` 항등) · λ 크랭크(argmax 불활성) — **전부 이 갭의 레버 아님**(autopsy 확증). slot/key-collision 상관분석도 지면배제(고른분산 실측).

## ⑧ 비용

S(구현) $0 · eval $0(로컬/pool CPU) · in-vivo G-W2 3-seed = summer GPU ~8h×seed(오너 go · fleet rent 아님 = 자율가능하나 seed11 컨트롤 종료 후).

---
**AGREES/CONFLICTS/NOVEL** (a_parallel_session_compare · origin/main max=9751 확인 후 등록): Fable∥Sol 수렴 = A(seed-space)·B(λ) 기각 · even/odd 분해 진단 · odd-fusion 레버. 내 $0 empirical 이 C1(even-지배) **확증**(op=0 상수-g 20/20). Sol 반대의견 = 재학습이 더 근본(위 ⑥ 기록). ⚠️ 로컬 untracked `H_9758_flip_evenodd_oddfuse.md`(Fable auto-write)가 다른 `H_9758_window_prefix_confound_dose.md` 와 G6 충돌 — 이 H_9760 이 origin/main-정합 클린 등록(그 untracked 카드들은 소유세션 dedup).

## 🔴 in-vivo G-W2 판정 — odd-fusion이 데몬 판독을 깨뜨린다 (2026-07-18 · 렌트 GPU 팟 RTX5090 · seed7 4-arm · 오너 "rent pod" go)

렌트 팟(45204319·$0.31/hr)서 `--store-fuse odd` 로 in-vivo gw2 4-arm(1152 tick) 발사·완료. 채점 = **전 arm P1-bal ≈ 0.0000 · flip-coh 0/0 (판독불가)**.

**아티팩트 아님(verify-done · transcript 직접 inspection)**: 데몬이 g/b 답 대신 garbage 방출 — `"is lumer =>"` → `" @ ... is mesur => @knowl"`(첫 non-space=`@`) · `"not dusat =>"` → `" \udcefnother thanks..."`(첫 non-space=surrogate).

**기전(중대 발견)**: odd `s_odd=½(s(v,g)−s(−v,g))` 는 overwrite row를 odd로 만들지만(negation 보장) **g/b를 global argmax로 보존하지 않는다**. even 성분 제거가 g/b logit을 키우던 걸 없애 → 실 256-vocab서 argmax=non-g/b. 내 $0 numpy 검증은 **negation만** 확인했지 argmax=g/b는 확인 안 함(toy V=6서 argmax 5→2=임의바이트). 데몬 full-vocab mouth는 global argmax를 뽑으므로 garbage.

**eval GREEN gate = false-positive**: `evaluate --store --store-fuse odd` main 128/128=1.0 였던 건 eval readout이 **2-way(g vs b logit 비교)**라 odd의 g/b **순서**만 보존됐기 때문. in-vivo full-vocab decode는 2-way를 안 함 → garbage. ⟹ **eval 2-way readout은 in-vivo full-vocab decode를 예측 못 한다**(측정 교훈).

### 최종 등급 (정직)
- **H_9760 = 🔴 in-vivo INVALID (TERMINAL)** — odd-fusion(full-row overwrite)은 데몬 답 방출을 깨뜨려 flip-coh 측정불가. WIRED 미획득. 배선(#4082·#4084)·arithmetic negation은 유효하나 **full-vocab decode 비호환**.
- **H_9744 = WIRED-STUDY-NEARMISS 불변** — odd가 ceiling 못 열음(구제 실패). NEARMISS 종결 유지.
- **⚠️ a_fire_recover_complete 위반**: scp glob 문법오류로 transcript 회수 실패했는데 teardown 진행돼 raw transcript 유실. 판정근거(garbage emit)는 teardown 전 직접 inspection으로 확보(결론 견고)·raw 아카이브만 소실.
- **follow-on(새 설계)**: full-row overwrite 대신 **g/b logit 쌍에만 odd 적용**(answer 2바이트만 odd-symmetrize·나머지 row는 overwrite s 유지) → argmax 보존+flip 획득. 또는 posterior-margin readout을 in-vivo 계기로 재사전등록. 별도 H.
