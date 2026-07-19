# H_9800 — EPHEMERAL-DECLARATION GROUNDING — 캐시를 CE-손해로 만들어 런타임 조회를 유일 최소화점으로 강제

**tier:** 🔵 PROPOSED · INSTRUMENT-BUILT (계기 구현+toy e2e 통과 · 측정 0 · DIRECTIONAL · NOT a verdict)
**group:** R11-grounding-channel
**source:** lab full 2026-07-19 — Fable A2 ≡ Sol #1 독립수렴(양 모델 1순위)
**wired:** instrument-wired (엔진 네이티브 플래그 2개 착륙 · 학습/측정 미발사)
**verdict:** PENDING (설계+계기만 · 기질 측정 0 · cement 는 engine-native `anima-py` 로만)

## claim
H_9359 언-캐시(frozen cache)가 사는 이유는 능력부재가 아니라 경제성 — 지금까지 전 코퍼스에서 사실의 극성이 전역 고정이라 암기가 조회보다 CE 상 싸다. episode 마다 stem/operator 의미를 무작위 재할당하면(비정상 non-stationary) parametric cache·stem prior 로 CE 를 줄일 수 없고 런타임 조회가 CE 유일 최소화점이 된다 ⟹ next-byte CE 자체가 다리 값을 지불. held-out 어간에서 declaration-flip 추종률이 오르면 그것이 접지(grounding) 채널.

## instrument (2026-07-20 구현 착륙 · v0.20.26)

카드가 적어둔 `corpus xbind --counterfactual-decl` 는 **독립 포맷** `counterfactual-decl` 로 착륙했다
(xbind 의 하위 플래그가 아님 — xbind 는 held-out 재조합 매니페스트라 episode 구조가 없다).

```
anima-py corpus counterfactual-decl --lang en --out c.txt [--seed 7] [--held-out 32,8]
                                    [--n-blocks 4000] [--stems-per-episode 4] [--eval-episodes 16]
anima-py evaluate <clm> --decl-flip c.txt.decl.json [--arms live,declaration-drop,value-shuffle]
                                    [--strata seen,...] [--win 256] [--out decl_flip.json]
```

**문법(EN 전용).** episode 마다 `<stem> means good|harm .` / `<op> acts same|flip .` 를 **새로 뽑고**,
질의는 `<op> <stem> => aye|nay`. 정답 = `sense_bit XOR role_bit` 뿐이다.

- **재할당이 핵심**: rotating 풀의 어간·연산자는 **에피소드마다 의미가 다시 뽑힌다** ⟹ 어간 prior 로는
  realized 우연 정확히 그대로. 캐시가 CE 손해가 된다.
- **carrier 무-접지**: 질의 담체 `<op> <stem> => ` 에는 정답 토큰(aye|nay)도 라벨명(good|harm|same|flip)도
  **0회**. 코퍼스 감사 + eval preflight **양쪽에서** 재검사(평가자가 연산자→정답 지도를 심지 못함).
- **분할은 어간이 아니라 MAPPING 까지**: 5 지층 — `seen` · `heldout-stem`(0-shot 바이트) ·
  `heldout-op`(0-shot 연산자 바이트) · `heldout-map-stem`(**바이트는 전부 학습됐지만 그 어간이 코퍼스에서
  가진 적 없는 ANTI sense**) · `heldout-map-op`(frozen 연산자의 ANTI role). 캐시-vs-조회는 map 지층에 산다.
- **극성 EXACT 균형 + 디스크 재파싱 검증**: 각 어간이 same/flip 연산자를 정확히 한 번씩 만나 답이 {aye,nay}
  → 구조적 균형. 그러나 구조적 논증은 증거가 아니므로 **쓰여진 파일을 다시 읽어** 계수하고, 우연은 realized
  분할의 다수 클래스 비율로 **재유도**한다(0.5 가정 금지 · `chance-level-must-be-derived-per-metric`).
  불균형이면 build 가 **abort**.
- **store 표면**: `<out>.storelines.txt`(+ lockstep `.store.jsonl`) = 질의줄만의 표면 —
  선언 바이트가 store 의 key/value 를 charge 하고(entities=선언 어간·pols=선언 sense·target_slot=질의 키),
  연산자 선언은 프롬프트가 싣는다(storebind 의 "store=사실·text=연산자" 계약 그대로) ⟹ `--store-fuse pairodd`
  co-train 이 그대로 소비. 에피소드 코퍼스는 1:1 lockstep 이 불가능하므로 **두 표면을 분리**한 것.

**eval DV = FLIP-SENSITIVITY**(선언을 뒤집을 때 답이 바뀐 항목 비율). 정확도는 병기하되 우연은 realized
분할서 재유도. **arm 3개 전부 동일 항목**에서 도는 within-item collapse-Δ:

| arm | 성격 |
|---|---|
| `live` | 두 world 가 참 선언을 싣고, flip 은 질의 어간의 value 4바이트만 움직인다. 담체는 flip 전후 **byte-identical** ⟹ 선언-무관 결정론적 정책의 flip 은 **구조적으로 정확히 0** = 이 DV 의 우연 수준 |
| `declaration-drop` | 질의 어간 선언을 **양쪽 world 에서** 제거 ⟹ 두 문맥이 byte-identical ⟹ flip 0 이 **기계적**. 계기 자신의 null — 0 이 아니면 하네스 버그이므로 run 을 INSTRUMENT-DEAD 로 **중단**(결과로 발표 금지) |
| `value-shuffle` | 같은 key·같은 value multiset, 대응만 derange(`shuf[i]=values[pi[i]]`, pi=derangement). `pi[q]≠q` 이므로 **질의 어간의 선언은 world-불변**이고 대신 다른 어간 선언이 같은 바이트 수만큼 움직인다 = 표면통계가 맞춰진 통계적 바닥 |

**ORACLE PREFLIGHT(포워드 이전)**: gold 재합성(`sense_bit XOR role_bit`) 불일치 0 · carrier 정답/라벨 히트 0
· flip 이 질의 선언만 같은 바이트 길이로 움직임 · oracle flip-sens **정확히 1.0**. 하나라도 어긋나면
⛔ INSTRUMENT-DEAD 로 종료하고 **held-out 수치를 읽지 않는다**(`positive-control-before-reading-a-negative`).

**판독 telemetry**: realized 답 분포 + 2AFC margin sd 를 찍는다 — `flip 0 · acc=우연` 은 **정직한 상수
예측기**와 **죽은 판독**이 둘 다 만들 수 있는데 그 둘은 서로 다른 발견이기 때문(sd=0 ⟹ ⚠️ DEGENERATE 표기).

**ADDITIVE only**: 동결 bar 를 하나도 움직이지 않았고 기존 패널은 byte-identical(회귀 0 실측).

## controls (사전등록)
양성: SEEN 어간 flip-sensitivity ≥0.90 + oracle arm ≥0.90(미달=INSTRUMENT-DEAD, held-out 판독금지·positive-control-before-reading-a-negative) · 음성: declaration token-shuffle → realized 분할서 재유도한 우연으로 붕괴 · declaration-drop ≤0.60 · value-shuffle(동일 key/multiset, 대응만 derange) ≤0.60 · 극성 클래스별 분할 후 판독(polarity-split-before-headline) · ≥3 seed 중 2 · 음성종결은 TOST ±0.05

## falsify
oracle ≥0.90 인데 live ≈ value-shuffle ⟹ 배선은 살아있으나 CE 가 접지 정책을 학습시키지 못함(벽이 DATA 보다 깊음·중대 결과). oracle <0.90 ⟹ INVALID, substrate 음성으로 읽지 말 것.

## toy e2e (2026-07-20 · exit 0 · CPU · 실측 로그)

`state/9257_lane23b/toy.clm`(48KB 미학습 토이)로 계기를 **1회 완주**시켰다. 이 코퍼스로 학습한 ckpt 가
아직 없으므로 이것은 **배선/통제 검증**이지 기질 측정이 아니다.

```
anima-py corpus counterfactual-decl --lang en --out e2e.txt --n-blocks 40 --held-out 32,8 \
                                    --eval-episodes 2 --seed 7
  POLARITY (re-parsed from disk): {'aye': 160, 'nay': 160} · balanced_exact=True · chance_majority=0.5000
  CARRIER ✅ 0 query carriers contain an answer token (aye|nay) or a label (good|harm|same|flip)
  0-SHOT  ✅ held-out stem/operator names appear 0x in the corpus

anima-py evaluate toy.clm --decl-flip e2e.txt.decl.json --win 256
  ORACLE preflight: gold-recompose mismatches 0/80 · flip_sens 1.0000 · carrier answer/label hits 0
                    · context-shape violations 0
  arm                    flip    acc_A    acc_B   chance   n
  live                 0.0000   0.5000   0.5000   0.5000   80
  declaration-drop     0.0000   0.5000   0.5000   0.5000   80
  value-shuffle        0.0000   0.5000   0.5000   0.5000   80
    live               answers_A={'nay': 80} · margin mean -0.2005 sd 0.0186 [-0.2264, -0.1611]
    declaration-drop   answers_A={'nay': 80} · margin mean -0.2007 sd 0.0186 [-0.2266, -0.1612]
    value-shuffle      answers_A={'nay': 80} · margin mean -0.2005 sd 0.0186 [-0.2264, -0.1612]
  COLLAPSE-Δ(flip) = live 0.0000 − max(control) 0.0000 = +0.0000
```

**정직한 판독**: 미학습 토이는 **상수 예측기**다 — 항상 `nay`, margin 이 전 구간 음수(최대 −0.161)라
어떤 항목도 경계 근처에 없다. 따라서 live flip 0 은 **기질에 대한 음성이 아니다**(읽으면 안 됨).
sd=0.0186≠0 이라 판독 자체는 살아 있고(비-degenerate) 문맥에 반응은 한다.
`declaration-drop` 이 기계적 0 을 낸 것 = 하네스가 계약대로 동작함.

**한 번도 실행 안 된 계기가 버그를 숨긴다는 법칙이 이번에도 맞았다**: 첫 실행에서
`_decl_flip_cell` 의 `collections` 미import(evaluate.py 는 collections 를 import 하지 않음)로 즉사 →
수정 후 통과. e2e 없이 착륙했으면 GPU fire 첫 판에서 터졌을 자리다.

**고의 파손 3종으로 게이트가 정말 FAIL 할 수 있음을 실증**(가드가 실패 못 하면 아무것도 검사 안 하는 것):

| 주입 결함 | 계기 반응 |
|---|---|
| gold 1개 뒤집기 | `gold-recompose mismatches 1/80 · flip_sens 0.9875` → ⛔ INSTRUMENT-DEAD (rc=2) |
| carrier 에 `aye ` 삽입 | `carrier answer/label hits 1` → ⛔ INSTRUMENT-DEAD (rc=2) |
| live_b := live_a (flip 무효화) | `context-shape violations 1` → ⛔ INSTRUMENT-DEAD (rc=2) |

기타 실측: `--lang ko` 거부 · `--stems-per-episode 6` 거부 · 미지 flag/arm 거부 ·
같은 seed 2회 빌드 **byte-identical**(sha 일치) · 4000-episode 전체 빌드도 균형 16000:16000·leak 0 ·
기존 포맷(derivtrace/flat/storebind)과 G0-G6 패널 **byte-identical = 회귀 0**.

## cost
303M train 1발 ~$8–15 (계기 구현은 $0 로 완료)

## 정직 caveat (c9)
이 카드는 **방향성 설계**이지 검증된 결과가 아니다. lab-full 발산 산출 = DIRECTIONAL, 절대 verdict 아님
(`a_lab_full_diverge`). frozen bar 사후 이동 금지(tune-to-green 금지 · p7). 발사 전 **toy e2e 1회**
(exit 0 + 산출물 + 통제) 필수 — 한 번도 실행 안 된 계기는 버그 여럿 겹쳐 숨긴다
(`instrument-never-run-hides-multiple-bugs`). 음성도 결과다.

## 미종결 (정직하게 열어둠)

1. **기질 측정 0** — 이 코퍼스로 학습한 ckpt 가 없다. live flip 이 실제로 오르는지는 **미측정**이며
   토이의 0 은 음성 증거가 **아니다**.
2. **포워드 경로 양성통제 부재** — oracle preflight 는 매니페스트/flip 배선이 양성을 표현할 수 있음을
   증명하지만, **2AFC 판독이 실제로 flip 을 낼 수 있는지**는 학습된 ckpt 없이 보일 수 없다. 카드의
   `SEEN flip ≥0.90` 양성 게이트가 그 역할이며 **held-out 판독 전에 반드시 먼저** 통과해야 한다.
3. **예산 floor 미측정** — `.meta.json` 의 min_steps/min_lr = null. 다른 포맷 floor 이식 금지.
4. **CPT 망각 게이트 미배선** — `forget_strata` 에 map 지층을 적어뒀으나(corpus-py-1 ⑦), CPT 로 쓸 경우
   base 사전측정(pre/post Δ) 은 발사 쪽 의무로 남아 있다.
5. **store 표면 미검증** — `.storelines.txt`/`.store.jsonl` 은 storebind 스키마를 맞췄지만
   `--store-fuse pairodd` 실주행으로 소비시켜 본 적은 없다(형식 일치만 확인).

## related
H_9359 · H_9267 · H_9775 · H_9304
