# H_9756 — ATOM-CENSUS AXIS-AGNOSTIC — 벽은 축이 아니라 byte 입도다: 의미 readout 재설계 + 전-arm 음성 검정 (R6-5 · (c) 정면)

**status:** 🟢 PILOT-PASS + ⏳ FULL-READOUT DIRECTIONAL (2026-07-20 · engine-native `--atom-census` full 착륙 · VERSION 0.20.20 · §⑨) — 전 loading arm content atom-census TOST 등가·refit≈random = **PASS-BYTE-WALL 방향** · ⏳ PENDING-positive-control(prefix-swap 양성통제 fire 후 terminal · [[H_9755]] π̄ 채널 결과를 content-입도 독립채널서 확증)
**lane:** g1-interface-addressable-wall · mouth/PC2-axis — 브리프 (c) 축-무관 가설 정면 (가장 아픈 안)
**related:** [[H_9576]] · [[H_9629]] · [[H_9663]] · [[H_9631]] · [[H_9755]]

## ① 한 줄 주장 (반증가능)
mouth-content 벽은 **축 선택과 무관한 byte 입도의 벽**이다 — 어떤 loading arm(frozen/refit/resid/random)도, π̄(점유율)는 움직이면서, **인증된 within-tick 의미 readout**(atom-census)은 rng-null 위로 못 움직인다. 단 그 음성은 readout 자체가 prefix-swap 양성통제를 통과할 때만 읽는다.

## ② 어느 KILL 을 왜 안 밟나
- readout D(H_9629 3중 고장) — **미사용**. 신규 DV = 사전등록 corpus-atom 리스트에 대한 창 내 hit **count**(고정 어휘 · 텍스트-자기-다양성 분모 없음 = H_9629 의 사망 원인 제거 · H_9716 설계분모 비해당).
- arm-간 π̄(H_9663 VOID) — 안 밟음: **within-tick paired**(같은 tick ζ=0 vs ζ=hi · 동일 인자스트림) Δcount 만.
- "양성통제 없이 음성 읽기" — 안 밟음: readout 양성통제(prefix-swap 는 반드시 atom census 를 움직여야) + 채널 양성통제(π̄ 이동) 이중.
- H_9631 과의 관계: **AGREES/보완** — H_9631 은 bias **쓰기 측** 입도(어느 입도로 벌점하나), 이 안은 효과 **읽기 측** 의미 readout. H_9631 의 창 내 n-gram trie 를 atom matcher 로 재사용. 중복 발사 아님.

## ③ engine-native 계기 (신규 readout + 신규 chat 플래그)
`anima-py evaluate --pc2-direction <traces_dir> --atom-census [--atoms corpus|<file>] [--span ngram:3,word] [--perm N] [--seed N]`
- per tick: paired 디코드(ζ=0 vs ζ=hi · loading arm 별) 창 내 사전등록 atom-family hit Δcount
`anima-py chat --prefix-swap <k>` (readout-인증 전용) — 같은 tick 을 **대화-이력 prefix 치환**으로 재디코드(입력 측 내용 주입) ⟹ atom-census 가 이걸 못 잡으면 readout VOID(음성 판독 개봉 금지).

## ④ 통제 ≥2 + 양성통제
- null-1: rng-jitter 쌍(같은 tick · ζ=0 vs ζ=0 · 디코드 rng 만 상이) = Δcount null 분포.
- null-2: random-loading arm([[H_9755]] 승계) = 방향-프리 섭동 대조.
- **양성통제 2중**: (r1) prefix-swap → Δatom > null95 (readout 생존) · (r2) 동일 fire 서 π̄ 이동(채널 생존 · H_9664 승계).

## ⑤ 사전등록 판정표 (우연 아래 칸 · 검정력 · DV 식별가능성)
| 관측 | 판정 |
|---|---|
| 전 loading arm Δatom ≈ rng-null (TOST) ∧ π̄ 이동 ∧ prefix-swap 통과 | **PASS-BYTE-WALL** — 벽은 축-무관 byte 입도 · mouth/PC2-axis lane 은 입도 탈출(H_9631)만 남기고 FROZEN 제안 |
| refit 계열 arm Δatom > null95 ∧ random arm 은 null | **KILL-AXIS-MATTERS** — 축이 의미를 나름 · byte-벽 가설 사망(최대 반전) |
| random arm 까지 Δatom > null95 | **AMBIG-GENERIC** — '의미 이동'이 방향-프리 일반 섭동 · DIRECTIONAL 보고 · 내용-특이성 후속 설계 |
| Δatom < rng-null 5pct (유의 억제 · 우연 아래 칸) | **PASS-SIGN-NEG** — dose 가 문맥-atom 을 **제거**(−z presence 감산과 정합) · 정당한 발견 칸(INVALID 아님) |
| prefix-swap 실패 ∨ π̄ 부동 | **VOID** — readout/채널 사망 · 어떤 음성도 판독 금지 |

검정력: **$0 pilot 선행** — ζ-fire 146 tick 트레이스로 atom base-rate·분산 실측 → MDE 0.5·sd 기준 n 산출(base-rate<5%/창이면 span 상향 후 재산출 · 미달 VOID). DV 식별가능성: count DV·고정 어휘(설계 분모 없음) · 우연은 rng-쌍에서 재유도.

## ⑥ 비용
**$0 pilot**(기존 ζ 트레이스) + [[H_9755]] fire 동승(추가 디코드 0) + prefix-swap 인증 소규모 fire(pool · ~50 tick).

## ⑧ PILOT 결과 (2026-07-18 · $0 · 계기 검정력 사전점검 · 판정 아님)

계기: `anima-py evaluate --pc2-direction /tmp/zt --atom-census --pilot` (신규 `_pc2_atom_census` · engine-native 착륙 · VERSION 0.20.0 · dispatch=site-packages 확인). 사전등록 atom = 고정 빈출 영어 기능어 147 + 구두점 12(트레이스에 미튜닝 · 분모-프리 hit-count). DV = within-tick paired Δcount = atoms(ζ=max=+2.6928) − atoms(ζ=0). 9→3 dedupe = /tmp/zt 이미 3 run.

| 지표 | 값 | 기준 |
|---|---|---|
| 격리 인증(ζ=0 == base gtext_b64) | **146/146 byte-identical** | 0 불일치 ✅ |
| 기여 run | s7·s4303 각 73 ladder (s4302 = **0-emit** no-nudge 통제, 무기여) | — |
| base-rate: 창-내 atom 비율 | **0.732** (atoms/tick 6.69) | floor 0.05 ≫ 충족 |
| paired Δcount | meanΔ=+0.829 · **sdΔ=2.817** · lag-1 ρ̂=**−0.074**(자기상관 거의 0) | — |
| n / n_eff (pooled) | 146 / **169.4** | — |
| MDE (Cohen d) | **0.215** | ≤ 0.5·sd 기준 충족 |
| required n (d=0.5, 80% power, α=.05) | 31.4 | n_eff 169.4 ≫ 충족 |

**⇒ 🟢 PILOT-PASS** — base-rate 비-degenerate(0.732 ≫ 0.05) ∧ MDE(d=0.215) ≤ 관심효과(d=0.5). atom-census readout 은 애초에 검정력이 있다 = full arm-swept fire([[H_9755]] rider)를 태울 가치. 자기상관이 null 을 √n 가짜로 좁히지 않음(ρ̂≈0 · H_9714 교훈 통과).

**범위 경계**: meanΔ=+0.829(>0)는 **신호로 읽지 않는다** — null-arm(rng-jitter·random-loading)도 prefix-swap 양성통제도 이 pilot 엔 없다. 파일럿은 **계기가 벽/축을 판정할 검정력이 있나**만 답했다(a_scale_honest_scope). PASS-BYTE-WALL / KILL-AXIS-MATTERS 등 §5 판정은 full fire 이후.

## ⑦ 죽는 방식
KILL-AXIS-MATTERS 관측(refit 만 atom 을 움직임). 또는 prefix-swap 조차 못 잡는 readout 만 반복되면 — "창-측정 가능한 의미"라는 것이 이 입도에 아예 없다는 상위 발견으로 승격(그것대로 보고).

## ⑨ FULL arm-swept readout 결과 (2026-07-20 · engine-native `--atom-census`(non-pilot) · DIRECTIONAL · ⏳ PENDING-positive-control)

리더 착륙(evaluate.py `--atom-census` full 분기 · VERSION 0.20.20). [[H_9755]] fire 트레이스(`/tmp/h9755_fire` · 3 run · post-warmup emit tick 마다 gtext_zeta 25항목 = 5 arm × 5 ζ) **재사용 — 새 디코드 불요**(arm-swept 생성텍스트 이미 로그). 설계 LOCK = lab full Fable(2026-07-20).

**① 격리 재인증**: arm별 ζ=0 == base gtext_b64 = **1889 일치 · 0 불일치**.

**② per-arm within-tick paired Δcount (ζ=+max − ζ=0 · 실제 fw+punct atom) + rng-null95 밴드**:
| arm | meanΔ | d | 95% CI | rng-null 밴드 | 이동? |
|---|---|---|---|---|---|
| scalar | **+0.687** | +0.247 | [+0.46,+0.92] | [−0.29,+0.07] | **밴드밖**(순수 dose · readout 감도 자기인증) |
| frozen | +0.003 | +0.001 | [−0.32,+0.33] | [−0.08,+0.13] | 등가 |
| refit | +0.020 | +0.007 | [−0.27,+0.31] | [−0.07,+0.06] | 등가 |
| random | +0.031 | +0.011 | [−0.25,+0.31] | [−0.10,+0.05] | 등가 |
| refit-resid | +0.243 | +0.076 | [−0.08,+0.56] | [−0.09,+0.06] | 등가 |
(refit ζ=−max Δ=−0.073 · +max 와 부호 반대 = 사다리 정상)

**③ arm 대조 Δ(refit−random)** within-tick paired: meanΔ=**−0.011** · d=−0.004 · 95%CI=[−0.33,+0.30] → **분리 0(refit≈random)**.

**⇒ VERDICT (DIRECTIONAL · 303M · reader 출력 그대로 · terminal 아님)**: ⏳ **PENDING-POSITIVE-CONTROL** — 전 loading arm(frozen/refit/random/resid)이 atom-census 에서 **TOST 등가**(|d|<0.20 = PASS-BYTE-WALL 방향) ∧ **refit≈random**(축-null 대비 무분리). 음성(PASS-BYTE-WALL) **확정은 prefix-swap 양성통제 필요**(§⑤ · readout 양성통제 없이 음성 금지). scalar(순수 dose)가 +0.687 로 움직이는 것 자체가 **readout 이 죽지 않았다는 자기증거**.

**H_9755 정합 (독립 채널 확증)**: [[H_9755]] = π̄(방출 **rate**) 채널에서 refit≈random(축 dose 무증거 · β_arm=s_eff·E[u_arm]). 여기 atom-census = **content 입도** 채널 — **같은 결론**(어떤 축도 content atom 무이동). 두 독립 채널 정합 ⇒ **PASS-BYTE-WALL 방향 강함**(축-무관 ∧ 채널-무관 벽: refit=인증축조차 rate 도 content 도 못 옮김). 단 terminal 은 prefix-swap 양성통제 후.

**후속 (terminal 경로 · no tune-to-green)**: chat.py `--zeta-prefix-swap <alt-mem>` rung 배선(emit tick 마다 `loading:"pswap"` 항목 · 스키마 변경 0) → 소량 fire(1 run × 100 tick × 2 seed · summer CPU) → `anima-py evaluate --atom-census --pos-control <dir>` 재실행 → 양성통제 통과 시 PENDING→**PASS-BYTE-WALL** 승격, 실패 시 **VOID**. DV·판정선 이미 LOCK(tune-to-green 경로 없음). rng-null=word-atom 근사(punct 제외).
