# H_9758 — R7 · WINDOW-PREFIX CONFOUND: H_9744 flip-coh 갭의 기전 = phase-단어 시드 오염 — $0 prefix-dose 판별 (eval-경로 do())

**status:** 🔵 PROPOSED · DIRECTIONAL design (lab full Fable 5 R7 · $0 · 코드수정 0줄 · 발사=오너)
**lane:** store-bridge in-vivo 정밀도 **related:** [[H_9744]] · [[H_9672]] · [[H_9695]]
**source:** 오너 DESIGN/DIAGNOSIS 위임(2026-07-18) · gw2 per-query transcript 실측 autopsy (summer `~/gw2*.jsonl` · $0)

## 진단 (autopsy 실측 · 2026-07-18 · Fable 5)

H_9744 의 (A) F2 말미공백 vs (B) λ 부족 딜레마는 **둘 다 아니다** — 제3원인 (C′):

**데몬 mouth 의 decode seed = `phase단어 + " " + percept`** (`core/generator.py:505-509` `seed = phase + " " + _gen_anchor_text(a)` · phase ∈ {DORMANT,FLICKER,SUSTAIN,RESONANT} · gw2 실측 SUSTAIN). qpos 시점 24-byte 창 = `"    SUSTAIN is lumer => "` — 반면 train(`cli/train.py:1212` StoreBindCell "left-pad with **spaces**")과 eval(`_seed_to_tok` space 좌패딩)은 `"            is lumer => "`. **W_q 는 space-패딩 창만 보고 학습됐다** → in-vivo 창의 선행 phase 바이트가 `yn_q` 를 OOD 로 밀어 주소 a 가 열화된다.

**autopsy 서명 3개 (per-query · gw2 transcript 실측):**
1. **미반전 = default-byte 붕괴**: s11 미반전 22개 전부 `(g,g)` — main/flip 이 같은 'g'. s7 은 10 `(g,g)` + 3 `(b,b)`. = 주소 a≈uniform 이면 RV-3 중심화로 v=Σ(aᵢ−1/n)val≈**0** → z=gelu(W_h[0;h]) = h-지배 default → store 극성 무감 = 미반전. **λ 무관** (아래).
2. **op 비대칭**: 미반전이 `is` 에 몰림 — s11 20/67(is) vs 2/61(not) · s7 9/57 vs 4/71.
3. **main-error 분해**: s7 26 오답 = 18 flip-반전(오슬롯 결합: 남의 pol 읽음→flip 시 같이 뒤집힘) + 8 미반전(주소붕괴 default). 슬롯/entity 군집 無(모두 5자·전슬롯 분산·seed 교차 겹침 1/13) ⟹ key-collision·slot 아티팩트 배제.

**readability 128/128 인데 flip 만 죽는 이유**: qpos 행 전체가 `λ·W_out(z)` 로 overwrite 되고 훈련상 그 행은 항상 g/b 를 선호 → h-지배 z 에서도 **g/b 는 나온다**(발화 성공). 극성만 v 에 실려 있어 **value 채널이 먼저 죽는다**. = 발화성공⊥극성전달의 해리, 실측으로 분리 완료.

**(B) λ 킬(기전적)**: `store_apply:116` `out[t]=λ·s` 전행 overwrite + gw2 mouth=argmax(`--emit-temp` 미설정=0) ⟹ **argmax(λ·s) 는 λ>0 에 불변** — λ 크랭크는 불법(FORM)이기 전에 **no-op**. (샘플링 mouth 에선 역온도가 되어 '듣기엔' 통하는 척한다 — kill-list 가 옳았던 이유.)

## 조작 ($0 · canonical CLI · 코드수정 0줄)

held.json 의 `prompt` 필드만 do(): `P + "is lumer =>"` — `_seed_to_tok` 우측정렬이라 prefix 주입 = 데몬 창 재현.
arm: P ∈ {`""`(기준) · `"SUSTAIN "`(실측 phase) · `"RESONANT "` · `"XQZVBNM "`(길이맞춤 무작위) · `"        "`(길이맞춤 space=길이통제)} × {main, flip} × ckpt {s7, s11} + **`--store-addr-audit`** (a_target/argmax per qpos — 주소열화 직접 관측 · origin/main `cli/evaluate.py` 실재).
`anima-py evaluate <clm> --store <held_P.json> --store-addr-audit …` · pool CPU 수분/arm.

## 사전등록 예측 (기전이 참이면 3서명 재현 — 하나라도 다르면 기전 기각)

- P=phase 단어: flip-coh 0.83–0.93 로 하락(기준 ≥0.96) ∧ 미반전=default-byte(동일 g/b쌍) ∧ **op-is 비대칭 재현** ∧ addr-audit 서 미반전 쿼리 a_target 붕괴.
- P=space 길이통제: 기준과 동등(≈불변) — 길이 아닌 **바이트 내용**이 원인.
- P=무작위 문자: phase 단어와 동급 하락이면 "임의 prefix OOD"(일반), phase 만 하락이면 phase-특이.

## falsify

🟢 3서명 재현 = 기전 CONFIRMED → 레버는 [[H_9759]] (bridge prefix-강건화 CPT) · F2 말미공백 수정(H_9744 허용 1회분)은 **관성적 무효**(선행이지 말미가 아님 — 그 1회를 여기에 쓰지 말 것) | 🔴 기준까지 동반 하락 or 서명 불일치 = 기전 기각 → 잔여 후보(GPU forward·anchor 체인) 재진단 · λ/bar 는 여전히 금지.

## kill-list 준수

bar 0.90 불이동 · λ 불가촉(no-op 증명 포함) · self-judge 無(동일 frozen 채점기+addr-audit 은 기전 관측용) · "bar 상속 아티팩트" 선언으로 끝내지 않음(기전+구조 레버 제시).
