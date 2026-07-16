# H_9407 — CONSULT-TO-GENERATION: addressable crack 이 생성 표면에 존재하나 (계기 WIRED)

**status:** 🔧 WIRED (계기 · byte-identical default 검증 · 5-arm 303M 측정 follow-on) — Fable 프런티어 shortlist #1 top pick · wired: engine-native `anima-py evaluate --consult-decode`
**lane:** g1-interface-addressable-wall / consult 주소지정 (생성 표면)
**related:** [[H_9334]] (interface addressable FIXABLE · 채점표면) · [[H_9347]] (담체 DV 0.75 · 채점표면) · source: Fable 프런티어 발산 (오너 "모두 진행" 3-레버 캠페인 #1)
**ckpt:** py303_full.clm (측정 대상 · follow-on) · toy.clm (계기 micro-smoke)

## 문제 (Fable가 코드로 확인한 구조적 구멍)

`--consult`(선언 저장소 주입)는 **2AFC 채점 seed에만** 도달한다(`_consult_seed`→`_xbind_cont_nll`). 자유
디코드(evaluate.py:3446)는 `it["seed"]`(선언 없는 평문)를 쓰고, `clm_decode_topk_sampled_W`가 seed 윈도를
**24 바이트로 하드코딩**(core/decode.py:1228). ⇒ 모든 consult/담체 positive(H_9334 "addressable FIXABLE",
H_9347 DV 0.75)는 **채점 표면에서만** 얻었다. **생성 표면은 선언을 주소지정할 수 있는지 한 번도 안 물었다.**

## 계기 (WIRED · byte-identical default)

`anima-py evaluate <clm> --xbind <m> --consult <store> --consult-decode`: 렌더된 선언을 **자유 디코드
seed**로 라우팅하되 윈도를 프로덕션 24에서 **ckpt 실 RF**로 확장(선언이 생성점 receptive field 안에 들어감).

- **core/decode.py**: process-global `_CONSULT_DECODE_T` + `set_consult_decode_window(T)`(H_9200
  `set_slw_controls` 패턴). `clm_decode_topk_sampled_W`의 `T = 24 if _CONSULT_DECODE_T is None else int(...)`.
  기본값 None ⇒ T=24 byte-for-byte. 포워드 수학 무변(채점 레인은 이미 T=64).
- **evaluate.py**: `--consult-decode`/`--consult-decode-win`/`--consult-decode-filler` 3 flag · RF 계산
  `(K−1)·(1+Σmin(2^i,512)+1)+1` · 헤더에 T_dec/RF 출력 · **구조적 pre-flight gate**(선언+stem+gen > T_dec 면
  INVALID-STRUCTURAL: "deaf vs blind 구별 불가·더 넓은 윈도 ckpt 필요, addressing 음성 아님") · `_consult_decode_seed`
  composer(render(fact)+filler+stem·채점레인과 byte-동일 선언·filler≥T_dec면 empty-store와 bitwise 동일=out-window 통제).
- **채점/margin 레인 byte-untouched**(의도적): run 자체의 positive control = H_9334/9347 margin 이 이 정확한 ckpt+manifest서 재현.

## micro-smoke (toy.clm · plumbing 검증)

```
default(None)=T=24 결정적: True
window override(64) 출력 변화: True · reset(None) byte-identical 복원: True   ← 기본값 무해 증명
RF_analytic=11 (toy K=3 L=2 · 프로덕션 윈도 24보다 작음=이 toy는 window-bound 아니라 RF-bound)
```
⇒ 기본값 완전 byte-identical(reset o1==o3) · window override 실제 작동 · RF 공식 정상.

## 5-arm 측정 (follow-on 303M fire · Fable §3-4)

| arm | store | delta | 역할 |
|---|---|---|---|
| P | — | plain `--xbind` | parity: frozen baseline 과 bitwise(40/40) |
| E | — | `--consult-decode` | window-only 통제(넓은 윈도·fact 없음) |
| A | correct | `--consult s --consult-decode` | in-window 정답 fact |
| B | correct | `+ --consult-decode-filler T_dec` | out-window: E 와 bitwise 동일(계기 self-check) |
| C | scram-pol | `--consult sc --consult-decode` | 극성 통제 |
| D | wrong-atom | `--consult wa --consult-decode` | 주소지정 통제 |

- 2 seed × {E,A,B,C,D}+P = 12 eval · summer pool · **단일 device 고정**(decode-py-4 · GPU≠CPU 2.5e-14).
- 판정(Fable §4): G-parity→G-instrument(B≡E)→G-positive(margin 재현·아니면 INVALID 음성 아님)→ **SURVIVE**
  = A 가 C·D 대비 paired McNemar p<0.05(순서통계량 Δ 금지) = 최초 생성표면 다리 / **KILL** = A ≤ 모든 통제
  (paired·TOST CI<+0.10) = 생성측 deafness("addressable"를 채점표면 전용으로 강등·pointer 상류 재라벨).
- 통제 store 는 **`anima corpus consult-variants` 🔧 WIRED** (Fable spec 구현): `--manifest EVAL.json | --store
  correct.json --out-dir DIR [--seed]` → correct/scram_pol/wrong_atom.json + consult_variants.manifest.json.
  **C=flip-all** pol(이진 derangement 은 marginal 보존 시 fixed-point=A오염 → 전부 flip) · **D=Sattolo cycle**
  (codepoint-sorted atom · fact multiset A 동일·주소지정만 이동·in-distribution). 빌더-코드 감사 7/7(keyset 3-way·
  C only-pol·C all-changed·D multiset·D no-fixpt·D no-A-collision) + 오염가드(기존 out-dir REFUSE·no --force).
  스모크 $0 통과: n=32·C n_changed=32·D fixpt=0 pol_match=14/32·결정성 byte-identical(same seed)·store re-emit byte-identical.

## 반증 · scope
- 계기 반증: 기본값 run 이 frozen baseline 과 다르면 배선 결함(현 reset byte-identical 검증). 측정 반증=
  Fable §4 판정그리드. RF 가 선언+stem 못 담으면 INVALID-STRUCTURAL(음성 아님·더 넓은 윈도 ckpt 필요).
- scope: 계기 WIRED(byte-identical default 검증) + **통제 store 빌더 WIRED**(consult-variants·스모크 $0 통과) ·
  측정 미실행(303M 5-arm summer follow-on · pool-blocked=oracle 포화·aiden down 시점). 오너 "모두 진행"
  3-레버 캠페인 #1(top pick) — #2 oracle-pool·#3 H_9339(계기 landed #3762) 병행.

## 비용
$0(계기+toy smoke) · G5 VERSION bump(core/decode.py+cli/evaluate.py) · 측정 fire=summer 12 eval(follow-on).
